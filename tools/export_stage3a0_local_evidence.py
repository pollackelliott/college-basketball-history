#!/usr/bin/env python3
"""Export the bounded target-school canonical projection for a pinned Stage 3A-0 run."""
import argparse,csv,json,subprocess,hashlib
from pathlib import Path
def main():
    ap=argparse.ArgumentParser();ap.add_argument("school_key");ap.add_argument("--canonical",type=Path,default=Path("data/canonical/games.csv"));ap.add_argument("--output-dir",type=Path);a=ap.parse_args()
    sha=subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip();out=a.output_dir or Path(".research")/a.school_key/"stage3a0-evidence";out.mkdir(parents=True,exist_ok=True)
    with a.canonical.open(newline="",encoding="utf-8-sig") as f:
        rd=csv.DictReader(f);fields=rd.fieldnames or [];rs=[r for r in rd if a.school_key in (r.get("team_a_key"),r.get("team_b_key"))]
    p=out/"target-canonical.csv"
    with p.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rs)
    meta={"school_key":a.school_key,"protected_main_sha":sha,"row_count":len(rs),"canonical_source":str(a.canonical),"projection_sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
    (out/"target-canonical-meta.json").write_text(json.dumps(meta,indent=2,sort_keys=True)+"\n");print(json.dumps(meta,indent=2))
if __name__=="__main__":main()
