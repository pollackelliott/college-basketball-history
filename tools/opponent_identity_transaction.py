#!/usr/bin/env python3
"""Sealed transactional apply for evidence-backed opponent-identity reconciliation."""
from __future__ import annotations
import argparse,csv,hashlib,json,subprocess,sys
from pathlib import Path
from typing import Any
import opponent_identity_remediation as remediation
import opponent_identity_collision_audit as collision_audit

class TransactionError(RuntimeError): pass
OpponentIdentityTransactionError=TransactionError

DISC_FIELDS=['discrepancy_id','canonical_game_id','field_name','source_a_program_key','source_a_value','source_b_program_key','source_b_value','canonical_value','status','resolution_basis','notes']
MERGE_FIELDS=['season_label','game_date','date_precision','team_a_score','team_b_score','result_winner_team_key','overtime_periods','site_type','designated_home_team_key','venue_key','venue_id','site_city','site_state','game_type','postseason_round','administrative_status','administrative_note','canonical_status']
DISCREPANCY_FIELDS=DISC_FIELDS
KEY_FIELDS={'result_winner_team_key','designated_home_team_key'}

def clean(v): return '' if v is None else str(v).strip()
def stable(v): return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def htext(v): return hashlib.sha256(v.encode()).hexdigest()
def hfile(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()
def read_csv(p):
    with p.open(encoding='utf-8-sig',newline='') as f:
        r=csv.DictReader(f); return list(r.fieldnames or []),list(r)
def write_csv(p,fields,rows):
    raw=p.read_bytes(); bom=raw.startswith(b'\xef\xbb\xbf'); nl='\r\n' if b'\r\n' in raw else '\n'; enc='utf-8-sig' if bom else 'utf-8'
    q=p.with_suffix(p.suffix+'.tmp')
    with q.open('w',encoding=enc,newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator=nl); w.writeheader(); w.writerows({k:r.get(k,'') for k in fields} for r in rows)
    q.replace(p)
def git_head(repo):
    x=subprocess.run(['git','rev-parse','HEAD'],cwd=repo,text=True,capture_output=True); return x.stdout.strip() if x.returncode==0 else ''

def load_resolutions(path):
    doc=json.loads(path.read_text())
    if doc.get('schema_version')!=1 or not isinstance(doc.get('resolutions'),list): raise TransactionError('resolution schema must be version 1 with resolutions list')
    out=[]; ids=set(); pairs=set()
    for raw in doc['resolutions']:
        r={k:raw.get(k) for k in raw}; rid=clean(r.get('resolution_id')); s=clean(r.get('survivor_canonical_game_id')); a=clean(r.get('absorbed_canonical_game_id')); basis=clean(r.get('resolution_basis'))
        if not all((rid,s,a,basis)) or s==a: raise TransactionError('each resolution requires unique id, survivor, absorbed, basis')
        if rid in ids or (s,a) in pairs: raise TransactionError(f'duplicate resolution {rid}')
        ids.add(rid); pairs.add((s,a)); vals={clean(k):clean(v) for k,v in (r.get('canonical_values') or {}).items()}
        bad=set(vals)-set(MERGE_FIELDS)
        if bad or any(not v for v in vals.values()): raise TransactionError(f'{rid}: invalid canonical_values')
        ds=[]
        for d in r.get('discrepancies') or []:
            d={k:clean(d.get(k)) for k in DISC_FIELDS if k not in {'discrepancy_id','canonical_game_id'}}
            if d.get('status')!='RESOLVED' or not all(d.get(k) for k in ['field_name','source_a_program_key','source_a_value','canonical_value','resolution_basis']): raise TransactionError(f'{rid}: invalid discrepancy')
            ds.append(d)
        out.append({'resolution_id':rid,'kind':clean(r.get('kind')) or 'EXPLICIT_RECONCILIATION','survivor':s,'absorbed':a,'canonical_values':vals,'resolution_basis':basis,'evidence_urls':sorted(clean(x) for x in (r.get('evidence_urls') or []) if clean(x)),'discrepancies':ds})
    return sorted(out,key=lambda x:x['resolution_id'])

def maprow(row,keymap):
    r=dict(row); a=keymap.get(clean(row.get('team_a_key')),clean(row.get('team_a_key'))); b=keymap.get(clean(row.get('team_b_key')),clean(row.get('team_b_key'))); sa=clean(row.get('team_a_score')); sb=clean(row.get('team_b_score')); site=clean(row.get('site_type'))
    if a<=b: r['team_a_key'],r['team_b_key']=a,b
    else:
        r['team_a_key'],r['team_b_key']=b,a; r['team_a_score'],r['team_b_score']=sb,sa
        if site=='TEAM_A_HOME': r['site_type']='TEAM_B_HOME'
        elif site=='TEAM_B_HOME': r['site_type']='TEAM_A_HOME'
    for k in KEY_FIELDS:
        if k in r: r[k]=keymap.get(clean(r.get(k)),clean(r.get(k)))
    return r

def mergefield(field,left,right,explicit,label):
    if field in explicit: return explicit[field],None
    l,r=clean(left),clean(right)
    if l==r: return l,None
    lu=l in ({'','UNKNOWN'} if field=='site_type' else {''}); ru=r in ({'','UNKNOWN'} if field=='site_type' else {''})
    if lu and not ru: return r,None
    if ru and not lu: return l,None
    return l,f'{label}: conflicting populated {field}: {l!r} vs {r!r}'

def next_disc_ids(rows,n):
    high=max([int(clean(r.get('discrepancy_id'))[5:]) for r in rows if clean(r.get('discrepancy_id')).startswith('DISC-') and clean(r.get('discrepancy_id'))[5:].isdigit()] or [0])
    return [f'DISC-{i:06d}' for i in range(high+1,high+n+1)]

def build_plan(repo,decisions,resolutions):
    repo=repo.resolve(); decisions=decisions.resolve(); resolutions=resolutions.resolve(); base=remediation.build_plan(repo,decisions)
    cfields,crows=read_csv(repo/'data/canonical/games.csv'); _,drows=read_csv(repo/'data/reconciliation/discrepancies.csv'); audit=collision_audit.audit_rows(base,crows); rs=load_resolutions(resolutions)
    rpair={(r['survivor'],r['absorbed']):r for r in rs}; affected={g for vals in base.get('affected_canonical_game_ids',{}).values() for g in vals}; keymap=dict(base.get('global_key_map') or {}); blockers=[b for b in base.get('blockers',[]) if 'exact-date canonical collision candidate(s); these require one-real-game reconciliation' not in b]; warnings=list(base.get('warnings',[]))
    byid={clean(r.get('canonical_game_id')):r for r in crows}; pairs=[]; useda=set(); usedb=set(); usedr=set()
    def pair(sid,aid,kind,res):
        label=f'{sid}->{aid}'; s=byid.get(sid); a=byid.get(aid)
        if not s or not a: blockers.append(f'{label}: missing canonical row'); return
        if sid not in affected or aid in affected: blockers.append(f'{label}: survivor/absorbed roles violate stale-row preservation rule')
        if sid in useda or aid in usedb: blockers.append(f'{label}: canonical row paired twice')
        useda.add(sid); usedb.add(aid); sm,am=maprow(s,keymap),maprow(a,keymap)
        if (sm.get('team_a_key'),sm.get('team_b_key'))!=(am.get('team_a_key'),am.get('team_b_key')) or clean(s.get('season_label'))!=clean(a.get('season_label')): blockers.append(f'{label}: participants/season mismatch')
        explicit=dict((res or {}).get('canonical_values') or {}); final={'team_a_key':clean(sm.get('team_a_key')),'team_b_key':clean(sm.get('team_b_key'))}
        for f in [x for x in MERGE_FIELDS if x in cfields]:
            v,e=mergefield(f,sm.get(f,''),am.get(f,''),explicit,label); final[f]=v
            if e: blockers.append(e)
        notes=[]
        for x in [clean(sm.get('notes')),clean(am.get('notes')),f'[OPPONENT_IDENTITY_RECONCILIATION absorbed={aid}; preserved survivor={sid}; one real game / one canonical game]']:
            if x and x not in notes: notes.append(x)
        if 'notes' in cfields: final['notes']=' | '.join(notes)
        pairs.append({'kind':kind,'survivor_canonical_game_id':sid,'absorbed_canonical_game_id':aid,'resolution_id':(res or {}).get('resolution_id',''),'final_canonical_values':final,'discrepancies':(res or {}).get('discrepancies',[])})
        if res: usedr.add(res['resolution_id'])
    for g in audit.get('collision_groups',[]):
        ids=list(g.get('canonical_game_ids') or []); aa=[x for x in ids if x in affected]; bb=[x for x in ids if x not in affected]
        if len(ids)!=2 or len(aa)!=1 or len(bb)!=1: blockers.append('collision group is not exactly one stale row plus one counterpart: '+','.join(ids)); continue
        s,a=aa[0],bb[0]; res=rpair.get((s,a)); kind=clean(g.get('kind'))
        if kind=='SAME_DATE_IDENTITY_CONFLICT' and not res: blockers.append(f'{s}->{a}: material conflict requires explicit resolution')
        if res and res['kind'] not in {kind,'EXPLICIT_RECONCILIATION'}: blockers.append(f'{s}->{a}: resolution kind mismatch')
        pair(s,a,kind,res)
    for s in audit.get('unpaired_affected_game_ids',[]):
        cand=[r for r in rs if r['survivor']==s]
        if len(cand)!=1: blockers.append(f'{s}: unpaired row requires exactly one explicit counterpart'); continue
        r=cand[0]
        if r['kind'] not in {'EXPLICIT_COUNTERPART','EXPLICIT_RECONCILIATION'}: blockers.append(f'{s}: unpaired resolution kind mismatch')
        pair(s,r['absorbed'],'EXPLICIT_COUNTERPART',r)
    if affected-useda: blockers.append('affected canonical rows not fully paired: '+','.join(sorted(affected-useda)[:25]))
    unused=[r['resolution_id'] for r in rs if r['resolution_id'] not in usedr]
    if unused: blockers.append('unused resolutions: '+','.join(unused))
    specs=[]
    for p in sorted(pairs,key=lambda x:x['survivor_canonical_game_id']):
        for d in p['discrepancies']: specs.append({**d,'canonical_game_id':p['survivor_canonical_game_id']})
    for did,spec in zip(next_disc_ids(drows,len(specs)),specs): spec['discrepancy_id']=did
    programs,_,_=remediation.load_programs(repo); packages=[]; source_programs=[]
    for d in base.get('decisions',[]):
        if clean(d.get('decision'))!='MERGE_TO_PROGRAM': continue
        target=clean(d.get('to_program_key')); preg=programs.get(target,{})
        packages.append({'decision_id':d['decision_id'],'source_program_key':clean(d.get('source_program_key')),'source_opponent_label':clean(d.get('source_opponent_label')),'from_program_key':clean(d.get('from_program_key')),'to_program_key':target,'to_program_name':clean(preg.get('display_name')) or clean(preg.get('program_name')) or target,'expected_source_game_ids':list(d.get('source_game_ids') or [])}); source_programs.append(clean(d.get('source_program_key')))
    fps={'programs.csv':hfile(repo/'data/reference/programs.csv'),'program-names.csv':hfile(repo/'data/reference/program-names.csv'),'canonical-games.csv':hfile(repo/'data/canonical/games.csv'),'game-assertions.csv':hfile(repo/'data/evidence/game-assertions.csv'),'discrepancies.csv':hfile(repo/'data/reconciliation/discrepancies.csv'),'decisions.csv':hfile(decisions),'resolutions.json':hfile(resolutions)}
    for p in sorted(set(source_programs)):
        fps[p+'/opponents.csv']=hfile(repo/'schools'/p/'opponents.csv'); fps[p+'/source-games.csv']=hfile(repo/'schools'/p/'source-games.csv')
    core={'schema_version':1,'git_head':git_head(repo),'base_plan_sha256':base.get('plan_sha256',''),'collision_audit_sha256':audit.get('audit_sha256',''),'global_key_map':keymap,'affected_canonical_game_count':len(affected),'canonical_pair_count':len(pairs),'canonical_pairs':sorted(pairs,key=lambda x:x['survivor_canonical_game_id']),'package_changes':sorted(packages,key=lambda x:x['decision_id']),'new_discrepancies':sorted(specs,key=lambda x:x['discrepancy_id']),'absorbed_canonical_game_ids':sorted(usedb),'survivor_canonical_game_ids':sorted(useda),'blockers':sorted(set(blockers)),'warnings':sorted(set(warnings)),'fingerprints':fps}
    core['plan_sha256']=htext(stable(core)); return core

def assert_ready(p):
    if p['blockers']: raise TransactionError('plan blockers: '+' | '.join(p['blockers'][:8]))
    if p['affected_canonical_game_count']!=p['canonical_pair_count']: raise TransactionError('affected/pair accounting mismatch')

def _run_validation(repo):
    if subprocess.run([sys.executable,'tools/validate_data.py'],cwd=repo).returncode: raise TransactionError('validate_data failed')

def apply(repo,decisions,resolutions,expected,run_validation=True):
    repo=repo.resolve(); p=build_plan(repo,decisions,resolutions); assert_ready(p)
    if clean(expected)!=p['plan_sha256']: raise TransactionError(f'sealed plan hash mismatch: expected {expected}, actual {p["plan_sha256"]}')
    paths=[repo/'data/canonical/games.csv',repo/'data/evidence/game-assertions.csv',repo/'data/reconciliation/discrepancies.csv']
    for c in p['package_changes']: paths += [repo/'schools'/c['source_program_key']/'opponents.csv',repo/'schools'/c['source_program_key']/'source-games.csv']
    paths=list(dict.fromkeys(paths)); originals={x:x.read_bytes() for x in paths}
    try:
        loaded={}; opp_changes=src_changes=0
        for c in p['package_changes']:
            op=repo/'schools'/c['source_program_key']/'opponents.csv'; sp=repo/'schools'/c['source_program_key']/'source-games.csv'
            loaded.setdefault(op,read_csv(op)); loaded.setdefault(sp,read_csv(sp)); of,ors=loaded[op]; sf,srs=loaded[sp]
            oms=[r for r in ors if clean(r.get('source_opponent_label'))==c['source_opponent_label'] and clean(r.get('canonical_opponent_key'))==c['from_program_key']]
            if not oms: raise TransactionError(c['decision_id']+': opponents row changed')
            for r in oms: r['canonical_opponent_key']=c['to_program_key']; r['canonical_opponent_name']=c['to_program_name']; r['current_d1']='Yes'; opp_changes+=1
            ids=set(c['expected_source_game_ids']); sms=[r for r in srs if clean(r.get('source_game_id')) in ids]
            if {clean(r.get('source_game_id')) for r in sms}!=ids: raise TransactionError(c['decision_id']+': source game set changed')
            for r in sms:
                if clean(r.get('normalized_opponent_key'))!=c['from_program_key']: raise TransactionError(c['decision_id']+': source opponent key changed')
                r['normalized_opponent_key']=c['to_program_key']; r['opponent_current_d1']='Yes'; src_changes+=1
        cf,cr=read_csv(repo/'data/canonical/games.csv'); af,ar=read_csv(repo/'data/evidence/game-assertions.csv'); df,dr=read_csv(repo/'data/reconciliation/discrepancies.csv')
        if df!=DISC_FIELDS: raise TransactionError('discrepancy schema changed')
        byid={clean(r.get('canonical_game_id')):r for r in cr}; redirect={q['absorbed_canonical_game_id']:q['survivor_canonical_game_id'] for q in p['canonical_pairs']}; keymap=p['global_key_map']
        for q in p['canonical_pairs']:
            s=byid.get(q['survivor_canonical_game_id']); a=byid.get(q['absorbed_canonical_game_id'])
            if not s or not a: raise TransactionError('canonical pair disappeared')
            for f,v in q['final_canonical_values'].items():
                if f not in cf: raise TransactionError('canonical schema changed: '+f)
                s[f]=clean(v)
        cr=[r for r in cr if clean(r.get('canonical_game_id')) not in redirect]; redirected=0
        for r in ar:
            gid=clean(r.get('canonical_game_id'))
            if gid in redirect: r['canonical_game_id']=redirect[gid]; redirected+=1
            k=clean(r.get('normalized_opponent_key'))
            if k in keymap: r['normalized_opponent_key']=keymap[k]
        for r in dr:
            if clean(r.get('canonical_game_id')) in redirect: r['canonical_game_id']=redirect[clean(r.get('canonical_game_id'))]
        existing={clean(r.get('discrepancy_id')) for r in dr}
        for d in p['new_discrepancies']:
            if d['discrepancy_id'] in existing: raise TransactionError('discrepancy id collision')
            dr.append({f:clean(d.get(f)) for f in DISC_FIELDS})
        for path,(fields,rows) in loaded.items(): write_csv(path,fields,rows)
        write_csv(repo/'data/canonical/games.csv',cf,cr); write_csv(repo/'data/evidence/game-assertions.csv',af,ar); write_csv(repo/'data/reconciliation/discrepancies.csv',df,dr)
        _,cr2=read_csv(repo/'data/canonical/games.csv'); _,ar2=read_csv(repo/'data/evidence/game-assertions.csv'); absorbed=set(p['absorbed_canonical_game_ids']); old=set(keymap)
        if any(clean(r.get('canonical_game_id')) in absorbed or clean(r.get('team_a_key')) in old or clean(r.get('team_b_key')) in old for r in cr2): raise TransactionError('postcondition: stale canonical row/key remains')
        if any(clean(r.get('canonical_game_id')) in absorbed or clean(r.get('normalized_opponent_key')) in old for r in ar2): raise TransactionError('postcondition: stale assertion mapping remains')
        if run_validation: _run_validation(repo)
    except Exception:
        for path,data in originals.items(): path.write_bytes(data)
        raise
    return {'plan_sha256':p['plan_sha256'],'canonical_games_absorbed':len(p['absorbed_canonical_game_ids']),'assertions_redirected':redirected,'opponents_rows_updated':opp_changes,'source_game_rows_updated':src_changes,'discrepancies_added':len(p['new_discrepancies'])}

build_transaction_plan=build_plan
apply_transaction=apply

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]); sub=ap.add_subparsers(dest='cmd',required=True)
    q=sub.add_parser('plan'); q.add_argument('decisions',type=Path); q.add_argument('resolutions',type=Path); q.add_argument('--output',type=Path); q.add_argument('--json',action='store_true')
    q=sub.add_parser('apply'); q.add_argument('decisions',type=Path); q.add_argument('resolutions',type=Path); q.add_argument('--expected-plan-sha256',required=True); q.add_argument('--apply',action='store_true')
    a=ap.parse_args(); repo=a.repo.resolve()
    try:
        if a.cmd=='plan':
            p=build_plan(repo,a.decisions,a.resolutions)
            if a.output: a.output.write_text(json.dumps(p,indent=2,sort_keys=True)+'\n')
            if a.json: print(json.dumps(p,indent=2,sort_keys=True))
            else: print(f"OPPONENT IDENTITY TRANSACTION PLAN\naffected={p['affected_canonical_game_count']} pairs={p['canonical_pair_count']} discrepancies={len(p['new_discrepancies'])} blockers={len(p['blockers'])}\nplan sha256: {p['plan_sha256']}")
            return 2 if p['blockers'] else 0
        if not a.apply: raise TransactionError('apply command requires explicit --apply')
        r=apply(repo,a.decisions,a.resolutions,a.expected_plan_sha256); print('PASS: '+stable(r)); return 0
    except (TransactionError,FileNotFoundError,ValueError,KeyError,json.JSONDecodeError) as e:
        print('FAIL:',e); return 1
if __name__=='__main__': raise SystemExit(main())
