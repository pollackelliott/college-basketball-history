# Sealed onboarding decisions

`tools/onboard_school.py --apply` archives the exact owner-approved plan for each
school here as:

```text
<school_key>-<first-12-characters-of-approved-plan-hash>.json
```

The file records the immutable input fingerprint, every dated identity and
discrepancy decision, publication/accomplishment approvals, evidence basis, and the
full SHA-256 plan hash. It is audit provenance; do not hand-edit it after apply.
