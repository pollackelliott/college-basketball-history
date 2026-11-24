# Vercel deployment-trigger policy

- **Status:** Repository-owned deployment-trigger policy for the public static site.
- **Applies to:** Vercel Git deployments for `college-basketball-history`.
- **Purpose:** preserve exact release Previews and Production deployment while preventing
  ordinary Research/tooling/control/transport pull requests from consuming deployment quota.

The public deployment is the checked-in `site/` tree configured by `vercel.json`.

## Required behavior

Automatic Git deployments are an explicit allow-list:

1. `main` always deploys. This preserves Production behavior.
2. `data/**` deploys. These school publication branches require exact-head Preview proof.
3. `maintenance/**` deploys. These shared-publication branches may require exact-head Preview proof.
4. Every other branch is deployment-disabled, including `tooling/**`, `research/**`,
   `control-center/**`, `control/remote-implementation`, `transport/**`,
   `hardening/**`, `docs/**`, and arbitrary feature branches.

A non-publication pull request must not create a Vercel Preview merely because it changes
tooling, tests, workflows, documentation, Research artifacts, or generic repository code.

## Static quota-control boundary

Vercel enables unspecified branches by default, so a deny-list is insufficient. The
repository therefore uses a fail-closed minimatch allow-list:

```json
{
  "git": {
    "deploymentEnabled": {
      "**": false,
      "main": true,
      "data/**": true,
      "maintenance/**": true
    }
  }
}
```

Vercel evaluates all matching rules and deploys when at least one matching rule is
`true`. The broad `**: false` rule therefore disables every branch unless an exact
approved publication family also matches a `true` rule.

This static branch policy is the quota-control mechanism because a disabled Git branch
does not create the automatic deployment that would consume the Hobby deployment ceiling.

## Ignored Build Step defense in depth

The repository-owned Ignored Build Step command remains:

```text
python tools/vercel_deployment_gate.py
```

Vercel's Ignored Build Step uses the opposite convention from ordinary success/failure:
exit 0 skips a deployment and exit 1 continues it.

The helper mirrors the same branch allow-list:

- `main` -> deploy;
- `data/**` -> deploy;
- `maintenance/**` -> deploy;
- every other branch -> skip.

The helper is secondary defense only. It must not be relied upon for the daily deployment
ceiling because Vercel may create a deployment record before an Ignored Build Step cancels
the build.

## Release invariant

This policy must never weaken the exact-Preview requirement.

School release branches and shared-reference publication branches remain explicitly
deploy-enabled. The remote release verifier still requires a successful Vercel Preview for
the exact release PR head before Owner Gate 2 can become ready.

Ordinary school Research branches, generic tooling repairs, Control Center maintenance,
workflow/test changes, and artifact transport are intentionally not deployable website
states and must not consume Preview slots.

If a future workflow requires an exact Vercel Preview from a new branch family, that family
must be explicitly added to this allow-list with regression coverage. Do not broaden the
default branch rule.

## Regression coverage

Regression coverage must prove:

- `main` deploys;
- `data/**` deploys;
- `maintenance/**` deploys;
- the catch-all `**` rule is `false`;
- tooling, Research, Control Center, control, transport, hardening, docs, and arbitrary
  feature branches remain disabled even if their commit changes `site/` or
  `vercel.json`;
- the Ignored Build Step helper mirrors the static allow-list.
