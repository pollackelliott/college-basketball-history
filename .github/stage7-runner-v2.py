#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] if '.github' in str(Path(__file__).resolve()) else Path.cwd()
TOOLS = ROOT / 'tools'
sys.path.insert(0, str(TOOLS))

import all_history_expansion_freeze as fr  # noqa: E402
import all_history_expansion_research as er  # noqa: E402

SCHOOL = 'miami'
MAIN_SHA = '7b8287e79b6bd4a8ee2b028b5b8d777f7f5c7cec'
BASE_SHA = '33af595fcae2a17664379638f89ce64c2e63be08'
STAGE6_ZIP_SHA = '56bf810b7879ce077e7d77091f876674d28df5ed8df088b5df5d2c1555e11978'
STAGE6_PACKAGE_SHA = 'abe4026bf182eb1f6f178a06b906ccac35fed479bdecf53fbf5edcbfb8e4eeec'
STAGE3B_SHA = '86cb728dc442f4534160f27ea5379161242a6b4b7a273d0876078dfdf422523e'
INCEPTION = '1927-1928'
CAPSULE_SHA = 'b22c1ce1c3c284a52e79ddbc739b2733f07ac29eb056aec6672550e020ef960e'


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def read_csv(path: Path):
    with path.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def csv_bytes(fields, rows):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    for row in rows:
        writer.writerow({field: str(row.get(field, '')) for field in fields})
    return stream.getvalue().encode('utf-8')


def write_csv(path: Path, fields, rows):
    path.write_bytes(csv_bytes(fields, rows))


def current_d1_false(value: str) -> bool:
    return value.strip().casefold() in {'no', 'false', '0', 'n'}


def verify_capsule(capsule: Path):
    manifest = read_json(capsule / 'stage7-input-manifest.json')
    assert manifest['kind'] == 'MIAMI_STAGE7_INPUT_CAPSULE'
    assert manifest['source_stage6_zip_sha256'] == STAGE6_ZIP_SHA
    for item in manifest['files']:
        path = capsule / item['path']
        data = path.read_bytes()
        assert len(data) == item['bytes'], item['path']
        assert sha256_bytes(data) == item['sha256'], item['path']

    checkpoint = read_json(capsule / 'checkpoint-manifest.json')
    assert checkpoint['school_key'] == SCHOOL
    assert checkpoint['research_base_sha'] == BASE_SHA
    assert checkpoint['state'] == 'COMPLETE_PRE_FREEZE_SELF_CHALLENGE_PASS'
    cp_hash = {item['path']: item['sha256'] for item in checkpoint['members']}
    for rel in [
        'stage1-baseline-correction-questions.csv',
        'stage5-owner-non-d1-disposition.json',
        'stage5-owner-non-d1-scan.csv',
        'stage6-package/notes.md',
        'stage6-package/opponents.csv',
        'stage6-package/source-games.csv',
        'stage6-package/source-notes.md',
        'stage6-package/venues.csv',
        'stage6-pre-freeze-blockers.csv',
        'stage6-self-challenge.md',
        'stage6-status.json',
    ]:
        assert cp_hash[rel] == sha256_bytes((capsule / rel).read_bytes()), rel

    stage3b_manifest = read_json(capsule / 'stage3b-manifest.json')
    assert stage3b_manifest['files']['stage1-scope-authority.json']['sha256'] == sha256_bytes(
        (capsule / 'stage1-scope-authority.json').read_bytes()
    )

    status = read_json(capsule / 'stage6-status.json')
    assert status['school_key'] == SCHOOL
    assert status['research_base_sha'] == BASE_SHA
    assert status['state'] == 'COMPLETE_PRE_FREEZE_SELF_CHALLENGE_PASS'
    assert status['durable_stage6_complete'] is True
    assert status['stage3b_complete_checkpoint_sha256'] == STAGE3B_SHA
    assert status['stage6_candidate_package_sha256'] == STAGE6_PACKAGE_SHA
    assert status['supplemental_game_population'] == 176
    assert status['unknown_exact_dates_after_stage6'] == 75
    assert status['unknown_han_after_stage6'] == 0
    assert status['home_researched_unresolved_venue_rows'] == 104
    assert status['pre_freeze_self_challenge'] == 'PASS'
    assert status['owner_non_d1_scan']['status'] == 'APPROVED'

    owner = read_json(capsule / 'stage5-owner-non-d1-disposition.json')
    assert owner['owner_scan_status'] == 'APPROVED'
    assert owner['flagged_identities'] == []
    assert owner['distinct_non_d1_identities'] == 37
    assert owner['supplemental_games_represented'] == 112


def verify_current_corrections(root: Path):
    _, ala = read_csv(root / 'schools/alabama/source-games.csv')
    rows = [r for r in ala if r.get('source_game_id', '').strip() == 'ALARAW-01436']
    assert len(rows) == 1
    row = rows[0]
    assert row.get('game_date', '').strip() == '1979-12-22'
    assert row.get('normalized_opponent_key', '').strip() == 'miami-oh'
    assert 'Miami (OH)' in (row.get('normalized_opponent_name', '') + row.get('source_opponent_label', ''))

    _, conf = read_csv(root / 'schools/miami/conferences.csv')
    exact = {
        ('1948-1949', '1953-1954', 'independent'),
        ('1954-1955', '1964-1965', 'florida-intercollegiate-conference'),
        ('1965-1966', '1970-1971', 'independent'),
    }
    got = {(r['start_season'], r['end_season'], r['conference_key']) for r in conf}
    assert exact.issubset(got)


def opponent_support(stage_rows, source_rows, baseline):
    stage_by = {(r['source_opponent_label'].strip(), r['canonical_opponent_key'].strip()): r for r in stage_rows}
    identities = sorted({(r['source_opponent_label'].strip(), r['normalized_opponent_key'].strip()) for r in source_rows})
    counts = Counter(r['normalized_opponent_key'].strip() for r in source_rows)
    label_counts = Counter(r['source_opponent_label'].strip() for r in source_rows)
    label_seasons = defaultdict(list)
    for r in source_rows:
        label_seasons[r['source_opponent_label'].strip()].append(r['season_label'].strip())
    base_by = defaultdict(list)
    for r in baseline['opponent_rows']:
        base_by[(r.get('source_opponent_label', '').strip(), r.get('canonical_opponent_key', '').strip())].append(r)

    output = []
    support_scope = defaultdict(set)
    for idx, ident in enumerate(identities, 1):
        assert ident in stage_by, f'missing Stage 6 opponent authority {ident}'
        accepted = stage_by[ident]
        matches = base_by.get(ident, [])
        if not matches:
            candidate = {field: accepted.get(field, '') for field in baseline['opponent_fields']}
            action = 'NEW_SUPPLEMENTAL'
            baseline_hash = ''
            changed = ''
        else:
            assert len(matches) == 1, ident
            inherited = matches[0]
            candidate = dict(inherited)
            # Mechanical additive extension only; preserve inherited identity/research fields.
            old_count = int(inherited.get('games_with_source_label', '0') or '0')
            candidate['games_with_source_label'] = str(old_count + label_counts[ident[0]])
            seasons = [s for s in [inherited.get('first_season', '').strip(), inherited.get('last_season', '').strip(), *label_seasons[ident[0]]] if s]
            candidate['first_season'] = min(seasons)
            candidate['last_season'] = max(seasons)
            addition = f"ALL_HISTORY_EXPANSION adds {label_counts[ident[0]]} accepted supplemental game(s) from checkpoint 0034."
            old_note = inherited.get('audit_note', '').strip()
            candidate['audit_note'] = (old_note + ' ' + addition).strip()
            diffs = [f for f in baseline['opponent_fields'] if candidate.get(f, '') != inherited.get(f, '')]
            assert set(diffs).issubset(fr.OPPONENT_EXTENSION_FIELDS), (ident, diffs)
            action = 'EXTEND_INHERITED' if diffs else 'REUSE_INHERITED'
            baseline_hash = fr.canonical_row_sha256(inherited)
            changed = ';'.join(sorted(diffs))
        if current_d1_false(candidate.get('current_d1', '')):
            if action == 'NEW_SUPPLEMENTAL':
                support_scope[ident[1]].add('SUPPLEMENTAL_NEW')
            elif action == 'EXTEND_INHERITED':
                support_scope[ident[1]].add('INHERITED_EXTENSION')
        output.append({
            'support_id': f'MIA-EXP-OPP-{idx:04d}',
            'support_action': action,
            'source_opponent_label': ident[0],
            'canonical_opponent_key': ident[1],
            'baseline_row_sha256': baseline_hash,
            'changed_fields': changed,
            'candidate_row_json': json.dumps(candidate, ensure_ascii=False, sort_keys=True, separators=(',', ':')),
            'evidence_basis': 'Stage 6 accepted opponent identity; inherited rows extended only in freeze-permitted additive accounting fields.',
        })
    normalized_scope = {}
    for key, scopes in support_scope.items():
        if scopes == {'SUPPLEMENTAL_NEW'}:
            normalized_scope[key] = 'SUPPLEMENTAL_NEW'
        elif scopes == {'INHERITED_EXTENSION'}:
            normalized_scope[key] = 'INHERITED_EXTENSION'
        else:
            normalized_scope[key] = 'SUPPLEMENTAL_NEW_AND_INHERITED_EXTENSION'
    return output, normalized_scope, counts


def venue_support(stage_rows, source_rows, baseline):
    # Only curated physical venues used by supplemental source rows need support.
    used_names = {r.get('curated_venue_name', '').strip().casefold() for r in source_rows if r.get('curated_venue_name', '').strip()}
    selected = []
    for r in stage_rows:
        names = {r.get('canonical_name', '').strip().casefold()}
        names.update(x.strip().casefold() for x in r.get('aliases', '').split(';') if x.strip())
        if names & used_names:
            selected.append(r)
    base_by = defaultdict(list)
    for r in baseline['venue_rows']:
        base_by[r.get('venue_key', '').strip()].append(r)
    output = []
    for idx, accepted in enumerate(sorted(selected, key=lambda r: r['venue_key']), 1):
        key = accepted['venue_key'].strip()
        matches = base_by.get(key, [])
        if not matches:
            candidate = {field: accepted.get(field, '') for field in baseline['venue_fields']}
            action, baseline_hash, changed = 'NEW_SUPPLEMENTAL', '', ''
        else:
            assert len(matches) == 1, key
            inherited = matches[0]
            candidate = dict(inherited)
            # Preserve inherited identity; extend additive venue accounting from accepted Stage 6 row.
            for f in fr.VENUE_EXTENSION_FIELDS:
                if f in accepted and accepted.get(f, '') and accepted.get(f, '') != inherited.get(f, ''):
                    candidate[f] = accepted[f]
            diffs = [f for f in baseline['venue_fields'] if candidate.get(f, '') != inherited.get(f, '')]
            assert set(diffs).issubset(fr.VENUE_EXTENSION_FIELDS), (key, diffs)
            action = 'EXTEND_INHERITED' if diffs else 'REUSE_INHERITED'
            baseline_hash = fr.canonical_row_sha256(inherited)
            changed = ';'.join(sorted(diffs))
        output.append({
            'support_id': f'MIA-EXP-VEN-{idx:04d}',
            'support_action': action,
            'venue_key': key,
            'baseline_row_sha256': baseline_hash,
            'changed_fields': changed,
            'candidate_row_json': json.dumps(candidate, ensure_ascii=False, sort_keys=True, separators=(',', ':')),
            'evidence_basis': 'Stage 6 accepted physical venue authority; inherited rows preserved or extended only in freeze-permitted additive fields.',
        })
    return output


def build(root: Path, capsule: Path, delta: Path):
    verify_capsule(capsule)
    verify_current_corrections(root)
    baseline = fr.authenticate_baseline(root, SCHOOL, BASE_SHA)

    source_fields, source_rows = read_csv(capsule / 'stage6-package/source-games.csv')
    assert len(source_rows) == 176
    expected_missing = {
        'season_year',
        'opponent_current_d1',
        'identity_override',
        'identity_override_basis',
        'identity_match_program_key',
        'identity_match_source_game_id',
    }
    assert set(baseline['source_fields']) - set(source_fields) == expected_missing
    assert set(source_fields) - set(baseline['source_fields']) == {'country'}
    assert all(not row.get('country', '').strip() for row in source_rows)

    _, projection_opponents = read_csv(capsule / 'stage6-package/opponents.csv')
    projection_d1 = {}
    for row in projection_opponents:
        ident = (
            row.get('source_opponent_label', '').strip(),
            row.get('canonical_opponent_key', '').strip(),
        )
        value = row.get('current_d1', '').strip()
        assert ident not in projection_d1
        assert value in {'Yes', 'No'}
        projection_d1[ident] = value

    projected_source_rows = []
    for row in source_rows:
        projected = {field: row.get(field, '') for field in baseline['source_fields']}
        season = row.get('season_label', '').strip()
        assert len(season) == 9 and season[4] == '-' and season[:4].isdigit() and season[5:].isdigit()
        projected['season_year'] = season[5:]
        ident = (
            row.get('source_opponent_label', '').strip(),
            row.get('normalized_opponent_key', '').strip(),
        )
        assert ident in projection_d1
        projected['opponent_current_d1'] = projection_d1[ident]
        projected['identity_override'] = ''
        projected['identity_override_basis'] = ''
        projected['identity_match_program_key'] = ''
        projected['identity_match_source_game_id'] = ''
        projected_source_rows.append(projected)

    assert sum(not r.get('game_date', '').strip() for r in source_rows) == 75
    assert sum(r.get('site_research_status', '').strip() == 'RESEARCHED_UNRESOLVED_HOME_VENUE' for r in source_rows) == 104
    assert all(r.get('curated_site_type', '').strip() != 'UNKNOWN' for r in source_rows)

    delta.mkdir(parents=True, exist_ok=True)
    write_csv(
        delta / 'expansion-source-games.csv',
        baseline['source_fields'],
        projected_source_rows,
    )

    # V2 inherited-unpublished reuse census.
    inherited_refs = []
    reused_per_season = Counter()
    for r in baseline['source_rows']:
        season = r.get('season_label', '').strip()
        if er.expansion_season_disposition(season, baseline['program'], INCEPTION) == er.EXPANSION_REQUIRED:
            inherited_refs.append({
                'source_game_id': r['source_game_id'].strip(),
                'season_label': season,
                'baseline_row_sha256': fr.canonical_row_sha256(r),
                'evidence_basis': 'Exact unchanged inherited unpublished source row reused under v2; authenticated at immutable research_base_sha.',
            })
            reused_per_season[season] += 1
    write_csv(delta / 'expansion-inherited-source-references.csv', fr.INHERITED_SOURCE_REFERENCE_FIELDS, inherited_refs)

    scope = read_json(capsule / 'stage1-scope-authority.json')
    scope_out = {k: scope[k] for k in ('baseline_scope', 'accepted_scope', 'authority_kind', 'owner_decision_reference', 'scope_notes')}
    assert scope_out['accepted_scope'] == 'INCEPTION+'
    assert scope_out['authority_kind'] == 'OWNER_SUPERSESSION'
    (delta / 'expansion-scope-authority.json').write_bytes(fr.canonical_json_bytes(scope_out))

    _, stage_opponents = read_csv(capsule / 'stage6-package/opponents.csv')
    opp_support, required_scan_scope, per_opponent = opponent_support(stage_opponents, source_rows, baseline)
    write_csv(delta / 'expansion-opponents.csv', fr.OPPONENT_SUPPORT_FIELDS, opp_support)

    _, stage_venues = read_csv(capsule / 'stage6-package/venues.csv')
    ven_support = venue_support(stage_venues, source_rows, baseline)
    write_csv(delta / 'expansion-venues.csv', fr.VENUE_SUPPORT_FIELDS, ven_support)

    # Exact season accounting is a mechanical projection of the accepted complete game universe.
    expected = fr.expected_expansion_seasons(baseline['program'], INCEPTION, baseline['baseline_terminal_season'])
    per_season = Counter(r['season_label'].strip() for r in source_rows)
    per_season.update(reused_per_season)
    accounting = []
    for season in expected:
        count = per_season.get(season, 0)
        if count:
            activity = 'ACTIVE'
            basis = 'Stage 6 accepted complete supplemental game universe plus exact v2 inherited-unpublished reuse census.'
        else:
            activity = 'DORMANT_OR_NO_TEAM'
            if '1971-1972' <= season <= '1984-1985':
                basis = 'Stage 1 owner scope authority explicitly classifies 1971-72 through 1984-85 as NO_TEAM/DORMANT.'
            else:
                basis = 'Stage 1 complete game-universe authority carried through Stage 6 contains zero recognized competitive varsity games for this expansion-required season; no game is fabricated at freeze.'
        accounting.append({
            'season_label': season,
            'activity_disposition': activity,
            'identified_competitive_game_count': str(count),
            'accounting_basis': basis,
        })
    write_csv(delta / 'expansion-season-accounting.csv', fr.SEASON_ACCOUNTING_FIELDS, accounting)

    write_csv(delta / 'expansion-exclusions.csv', fr.EXCLUSION_FIELDS, [])

    residuals = []
    rid = 1
    for r in source_rows:
        if not r.get('game_date', '').strip():
            residuals.append({
                'residual_id': f'MIA-EXP-RES-{rid:04d}',
                'season_label': r['season_label'].strip(),
                'source_game_id': r['source_game_id'].strip(),
                'residual_category': 'UNKNOWN_EXACT_DATE',
                'status': 'NONBLOCKING_RESEARCHED',
                'research_basis': 'Stage 6 exact-date self-challenge exhausted the obvious comparable institutional/reciprocal source families; blank retained without inference.',
            })
            rid += 1
        if r.get('site_research_status', '').strip() == 'RESEARCHED_UNRESOLVED_HOME_VENUE':
            basis = r.get('site_research_basis', '').strip()
            assert basis
            residuals.append({
                'residual_id': f'MIA-EXP-RES-{rid:04d}',
                'season_label': r['season_label'].strip(),
                'source_game_id': r['source_game_id'].strip(),
                'residual_category': 'RESEARCHED_UNRESOLVED_HOME_VENUE',
                'status': 'NONBLOCKING_RESEARCHED',
                'research_basis': basis,
            })
            rid += 1
    assert sum(r['residual_category'] == 'UNKNOWN_EXACT_DATE' for r in residuals) == 75
    assert sum(r['residual_category'] == 'RESEARCHED_UNRESOLVED_HOME_VENUE' for r in residuals) == 104
    write_csv(delta / 'expansion-residuals.csv', fr.RESIDUAL_FIELDS, residuals)

    _, stage5_scan = read_csv(capsule / 'stage5-owner-non-d1-scan.csv')
    scan_by = {r['canonical_opponent_key'].strip(): r for r in stage5_scan}
    scan_rows = []
    for key in sorted(required_scan_scope):
        assert key in scan_by, f'Stage 5 owner scan missing required key {key}'
        s = scan_by[key]
        assert int(s['game_count']) == per_opponent[key], (key, s['game_count'], per_opponent[key])
        scan_rows.append({
            'opponent_key': key,
            'supplemental_game_count': str(per_opponent[key]),
            'representative_raw_labels': s['representative_source_labels'].strip(),
            'support_scope': required_scan_scope[key],
            'scan_disposition': 'CLEARED',
            'scan_basis': 'Owner APPROVED Stage 5 NON_D1 sanity scan on 2026-11-18; zero flagged identities.',
        })
    write_csv(delta / 'expansion-non-d1-scan.csv', fr.NON_D1_SCAN_FIELDS, scan_rows)

    _, questions = read_csv(capsule / 'stage1-baseline-correction-questions.csv')
    assert len(questions) == 1 and questions[0]['question_id'] == 'MIA-EXP-BCQ-001'
    q = questions[0]
    correction_rows = [{
        'question_id': q['question_id'],
        'inherited_source_game_id': '',
        'canonical_game_id': q['canonical_game_id'],
        'issue': q['issue'],
        'evidence_basis': q['evidence_basis'] + f' External correction proof: protected main {MAIN_SHA} now records Alabama ALARAW-01436 as Miami (OH) / miami-oh; correction merged through PR #667.',
        'expansion_impact': 'NO_EXPANSION_IMPACT',
        'disposition': 'RESOLVED_EXTERNALLY_ON_PROTECTED_MAIN_PR_667__DO_NOT_INCLUDE_AS_MIAMI_FL',
    }]
    write_csv(delta / 'expansion-baseline-correction-questions.csv', fr.CORRECTION_QUESTION_FIELDS, correction_rows)

    notes = f'''# Miami (FL) ALL_HISTORY_EXPANSION Research Freeze\n\nresearch_base_sha={BASE_SHA}\nresearched institutional inception={INCEPTION}\n\nThis artifact freezes the accepted supplemental expansion Research against the immutable inherited baseline. The inherited published package is not re-researched or rewritten by this freeze.\n\nStage 6 checkpoint 0034 remains the terminal pre-freeze historical authority: 176 supplemental competitive games; 75 researched unresolved exact dates; 0 UNKNOWN H/A/N; 104 explicitly researched unresolved HOME exact venues; owner NON_D1 sanity scan APPROVED; pre-freeze adversarial self-challenge PASS.\n\nThe two external inherited-baseline blockers are now durably resolved on protected main {MAIN_SHA}. PR #667 corrected Alabama ALARAW-01436 to Miami (OH) / miami-oh. PR #678 corrected Miami's published pre-hiatus conference chronology to Independent (1948-49 through 1953-54), Florida Intercollegiate Conference (1954-55 through 1964-65), Independent (1965-66 through 1970-71). Those corrections remain outside supplemental expansion mutation authority.\n'''
    (delta / 'expansion-notes.md').write_text(notes, encoding='utf-8')
    source_notes = '# Miami (FL) ALL_HISTORY_EXPANSION freeze source notes\n\nStage 7 preserves Stage 6 accepted source provenance without new historical research.\n\n' + (capsule / 'stage6-package/source-notes.md').read_text(encoding='utf-8')
    (delta / 'expansion-source-notes.md').write_text(source_notes, encoding='utf-8')

    return baseline, source_rows, residuals, scan_rows


def main(argv=None):
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--capsule', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args(argv)
    root = Path.cwd().resolve()
    outdir = args.output_dir.resolve()
    delta = outdir / 'delta'
    outdir.mkdir(parents=True, exist_ok=True)

    baseline, source_rows, residuals, scan_rows = build(root, args.capsule.resolve(), delta)
    freeze1 = outdir / 'miami-expansion-research-frozen-stage7.zip'
    freeze2 = outdir / 'miami-expansion-research-frozen-stage7-determinism-check.zip'
    report = fr.freeze_expansion(root, SCHOOL, delta, BASE_SHA, INCEPTION, freeze1)
    verify = fr.verify_expansion(root, freeze1)
    report2 = fr.freeze_expansion(root, SCHOOL, delta, BASE_SHA, INCEPTION, freeze2)
    assert report['zip_sha256'] == report2['zip_sha256']
    assert freeze1.read_bytes() == freeze2.read_bytes()
    manifest = json.loads(__import__('zipfile').ZipFile(freeze1).read(fr.MANIFEST_MEMBER))
    assert manifest['state'] == 'EXPANSION_RESEARCH_FROZEN'
    assert manifest['expansion']['supplemental_source_game_count'] == 176
    assert manifest['expansion']['residual_status_summary'].get('BLOCKING', 0) == 0
    assert manifest['expansion']['non_d1_scan_status_summary'].get('UNRESOLVED', 0) == 0
    assert manifest['expansion']['baseline_correction_question_status_summary'] == {'NO_EXPANSION_IMPACT': 1}

    status = {
        'schema_version': 1,
        'workflow_kind': 'ALL_HISTORY_EXPANSION',
        'stage': 'STAGE_7',
        'state': 'EXPANSION_RESEARCH_FROZEN',
        'school_key': SCHOOL,
        'current_protected_main_sha': MAIN_SHA,
        'research_base_sha': BASE_SHA,
        'source_stage6_checkpoint_sha256': STAGE6_ZIP_SHA,
        'source_stage6_candidate_package_sha256': STAGE6_PACKAGE_SHA,
        'source_stage3b_checkpoint_sha256': STAGE3B_SHA,
        'freeze_zip_sha256': report['zip_sha256'],
        'freeze_manifest_sha256': report['manifest_sha256'],
        'fresh_verify_status': verify['status'],
        'deterministic_second_freeze_match': True,
        'supplemental_game_population': 176,
        'unknown_exact_date_residuals': 75,
        'researched_unresolved_home_venue_residuals': 104,
        'unknown_han': 0,
        'non_d1_scan_rows': len(scan_rows),
        'blocking_residuals': 0,
        'baseline_correction_questions_blocking': 0,
        'external_corrections': {
            'MIA-EXP-BCQ-001': {'status': 'RESOLVED', 'pr': 667},
            'MIA-EXP-DOWNSTREAM-CONF-001': {'status': 'RESOLVED', 'pr': 678},
        },
        'tracked_repository_mutations': 0,
        'next_permitted_unit': 'NONE_WITHIN_THIS_STAGE7_UNIT__DOWNSTREAM_IMPLEMENTATION_REQUIRES_SEPARATE_AUTHORITY',
    }
    (outdir / 'stage7-status.json').write_text(json.dumps(status, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    print(json.dumps({'freeze': report, 'verify': verify, 'status': status}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
