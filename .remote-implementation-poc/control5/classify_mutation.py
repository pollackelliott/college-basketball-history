#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def classify(expected_predecessor, actual_target, manifest_path=None, successor_path=None):
    if not manifest_path:
        if actual_target == expected_predecessor:
            return "NOT_ATTEMPTED"
        return "DIVERGED_STOP"

    manifest = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    bundle = Path(manifest_path).parent
    target_payload = bundle / manifest["target_payload_file"]
    sidecar = bundle / manifest["sidecar_authority_file"]
    if sha256(target_payload) != manifest["target_payload_sha256"]:
        raise SystemExit("WRITEAHEAD_PAYLOAD_HASH_MISMATCH")
    if sha256(sidecar) != manifest["sidecar_authority_sha256"]:
        raise SystemExit("WRITEAHEAD_SIDECAR_HASH_MISMATCH")
    if manifest["expected_target_predecessor_sha"] != expected_predecessor:
        raise SystemExit("WRITEAHEAD_PREDECESSOR_MISMATCH")

    prepared = manifest["prepared_commit_sha"]
    if actual_target == expected_predecessor:
        return "PREPARED_NOT_PUBLISHED"
    if actual_target == prepared:
        if successor_path:
            successor = json.loads(Path(successor_path).read_text(encoding="utf-8"))
            if (
                successor.get("prepared_commit_sha") == prepared
                and successor.get("actual_published_target_sha") == actual_target
                and successor.get("final_transaction_state") == "COMPLETE"
            ):
                return "COMPLETE"
        return "PUBLISHED_NOT_FINALIZED"
    return "DIVERGED_STOP"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--expected-predecessor", required=True)
    p.add_argument("--actual-target", required=True)
    p.add_argument("--manifest")
    p.add_argument("--successor")
    args = p.parse_args()
    print(classify(args.expected_predecessor, args.actual_target, args.manifest, args.successor))


if __name__ == "__main__":
    main()
