# Vercel deployment-trigger policy

- **Status:** Repository-owned deployment-trigger policy for the public static site.
- **Applies to:** Vercel Git deployments for `college-basketball-history`.
- **Purpose:** preserve exact release Previews and Production deployment while preventing
  durable control/tooling/transport commits from exhausting deployment quotas.

The public deployment is the checked-in `site/` tree configured by `vercel.json`.

## Required behavior

1. `main` always deploys. This preserves the existing Production behavior.
2. `control/remote-implementation` never auto-deploys. Control commits are durable
   orchestration/checkpoint state, not public-site releases.
3. Every other Git branch deploys only when the commit changes `site/` or
   `vercel.json` relative to its first parent.
4. If the gate cannot determine a parent or `git diff` fails, it must fail open and
   allow the deployment rather than suppress a potentially required Preview.

Vercel's Ignored Build Step uses the opposite convention from ordinary success/failure:
exit 0 skips a deployment and exit 1 continues it. The repository-owned command is:

```text
python tools/vercel_deployment_gate.py
```

The Vercel project setting must point to that command after this policy is merged.
During rollout, an inline equivalent may be used so the guard becomes effective before
the helper reaches protected `main`.

## Release invariant

This policy must never weaken the exact-Preview requirement. School release branches and
shared-reference maintenance branches produce checked-in `site/` changes when their
published output changes, so their exact PR heads continue to receive Vercel Previews.
The remote release verifier still requires a successful Preview for the exact PR head
before Owner Gate 2 can become ready.

A tooling/docs/transport/control commit that does not alter `site/` is intentionally not
a deployable website state and should not consume a Preview slot.

## Configuration defense in depth

`vercel.json` also explicitly sets:

```json
{
  "git": {
    "deploymentEnabled": {
      "control/remote-implementation": false
    }
  }
}
```

The project-level Ignored Build Step remains necessary for the already-diverged operational
control branch and for non-site commits on other branches.
