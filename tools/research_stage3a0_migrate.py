#!/usr/bin/env python3
"""Validate a narrow pre-3A-0 legacy compatibility repair."""
import argparse,csv,json,hashlib
from pathlib import Path
def read(p):
    with open(p,newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def pick(r,*ns):
    for n in ns:
        if str(r.get(n,"")).strip():return str(r[n]).strip()
    return ""
def rid(r):return pick(r,"research_game_id","source_game_id","game_id","id")
def main():
    ap=argparse.ArgumentParser();ap.add_argument("base",type=Path);ap.add_argument("repaired",type=Path);ap.add_argument("--output",type=Path);a=ap.parse_args()
    b=read(a.base);r=read(a.repaired);errors=[]
    if len(b)!=len(r):errors.append(f"row_count changed: {len(b)} -> {len(r)}")
    bi={rid(x):x for x in b};ri={rid(x):x for x in r}
    if "" in bi or "" in ri:errors.append("missing stable row ID")
    if len(bi)!=len(b) or len(ri)!=len(r):errors.append("duplicate stable row ID")
    if set(bi)!=set(ri):errors.append("row ID population changed")
    allowed={"game_type","season_type","competition_type"};changed=[]
    for k in sorted(set(bi)&set(ri)):
        keys=set(bi[k])|set(ri[k]);bad=[f for f in keys if f not in allowed and str(bi[k].get(f,""))!=str(ri[k].get(f,""))]
        if bad:errors.append(f"{k}: non-game-type fields changed: {','.join(sorted(bad))}")
        if any(str(bi[k].get(f,""))!=str(ri[k].get(f,"")) for f in allowed):changed.append(k)
        if not pick(ri[k],"game_type","season_type","competition_type"):errors.append(f"{k}: repaired game_type still blank")
    result={"status":"PASS" if not errors else "FAIL","declared_intent":"MISSING_GAME_TYPE_ONLY","base_rows":len(b),"repaired_rows":len(r),"game_type_rows_changed":len(changed),"errors":errors,"base_sha256":hashlib.sha256(a.base.read_bytes()).hexdigest(),"repaired_sha256":hashlib.sha256(a.repaired.read_bytes()).hexdigest()}
    if a.output:a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,indent=2));return 0 if not errors else 2
if __name__=="__main__":raise SystemExit(main())
