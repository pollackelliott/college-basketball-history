# Codespace Terminal Safety for School Onboarding

- **Status:** Required companion to `school-onboarding-fast-path.md`
- **Applies to:** All interactive onboarding work in the project Codespace
- **Purpose:** Prevent avoidable terminal death, partial-command ambiguity, and repository churn while preserving fail-fast safety

The onboarding architecture is now strong enough that the most common avoidable failures are not basketball-data failures. They are shell-driving failures.

LSU and Georgia both completed successfully, but the surrounding work reinforced a simple rule:

> **Keep the interactive shell boring and alive. Run complex fail-fast logic in a child script, not in the shell the owner is sitting in.**

## 1. Do not enable Bash nounset in this Codespace

The project Codespace includes RVM shell integration that has reacted badly to Bash nounset. In this environment, do not use:

```bash
set -u
```

and do not use:

```bash
set -euo pipefail
```

This has previously terminated the interactive terminal with an RVM `unbound variable` failure unrelated to basketball data.

For a child script that benefits from fail-fast behavior, use:

```bash
set -eo pipefail
```

or explicit return-code checks.

## 2. Never use `exit` as the STOP mechanism in a pasted interactive block

A guard that calls `exit 1` is safe inside a child script. The same command pasted directly into the current interactive shell can terminate the shell itself.

Therefore:

- short interactive commands may print `STOP:` and simply stop there;
- complex guarded work belongs in `/tmp/<descriptive-name>.sh` and may use `exit 1` safely;
- do not wrap giant multi-stage procedures directly around the owner's live shell.

Recommended pattern:

```bash
cat > /tmp/cbh-step.sh <<'BASH'
#!/usr/bin/env bash
set -eo pipefail

REPO="/workspaces/college-basketball-history"
cd "$REPO" || {
  echo "STOP: repository path is unavailable."
  exit 1
}

# Explicit guards and work here.
BASH

bash /tmp/cbh-step.sh
```

If the child script stops, the interactive terminal survives.

## 3. Expected-negative probes must be handled explicitly

Under `set -e`, a command returning status 1 stops the script even when status 1 is the expected answer to a question.

Common examples include:

- checking whether a branch exists;
- `grep` searches where no match is acceptable;
- testing whether a file is tracked;
- checking whether a path already exists;
- probing for an optional artifact.

Do not write an expected-negative probe as a naked command under `set -e`.

Use explicit control flow:

```bash
if git show-ref --verify --quiet refs/heads/data/example-onboarding; then
  echo "STOP: branch already exists."
  exit 1
else
  echo "PASS: branch is available."
fi
```

or deliberately neutralize the expected negative result with `|| true` only when that behavior is genuinely intended.

## 4. Prefer a short child script over a giant pasted shell block

A large 100-200 line pasted block can fail for reasons unrelated to the underlying workflow:

- copy/paste truncation;
- accidental line-continuation damage;
- shell-state leakage;
- expected nonzero commands under `set -e`;
- accidental `exit` of the interactive terminal;
- partial completion that is hard to reconstruct.

For substantial Phase 0, Gate 1 encoding, or recovery work:

1. write a quoted heredoc to `/tmp`;
2. execute the script once;
3. make the script print clear stage headings and a final PASS/STOP result;
4. keep diagnostic logs in `/tmp` or ignored `.onboarding/` paths;
5. do not place helper scripts in the repository root.

Several short guarded commands are also preferable when the work has natural checkpoints.

## 5. Keep transport and helper artifacts out of the tracked-worktree boundary

Untracked files in the repository root can block clean-worktree guards even when the basketball data is correct.

Rules:

- transport ZIPs are temporary inputs, not repository content;
- after verified extraction, remove the ZIP from the repository root;
- helper scripts belong in `/tmp`;
- generated onboarding artifacts belong under ignored `.onboarding/<school>/` when appropriate;
- never broaden a cleanliness guard merely because a convenience file was left in the repo.

## 6. On failure, inspect state once before rerunning

Do not reflexively rerun a long installer after it stops.

First inspect:

```bash
git branch --show-current
git rev-parse HEAD
git status --short
git --no-pager log -4 --oneline
```

Then determine:

- which stage actually completed;
- whether HEAD changed;
- whether tracked files changed;
- whether only an untracked helper/transport artifact exists;
- whether the failure was technical or historical.

A failed guard should reduce uncertainty, not trigger repeated blind retries.

## 7. Do not reopen historical decisions for a shell failure

If a terminal or script failure occurs after Owner Gate 1, first determine whether the reviewed decision universe changed.

If the problem is purely technical and the historical inputs/decisions remain identical:

- fix the narrow technical defect;
- regenerate preflight if required by the sealed workflow;
- prove the decision-ID universe is unchanged;
- carry forward the already-approved decisions by exact `decision_id`;
- reseal with a new hash when required;
- do not ask the owner to decide the same basketball history again.

Historical decisions reopen only when historical inputs materially change.

## 8. Shell-safety checklist before giving the owner a command block

Before asking the owner to paste terminal instructions, verify:

- no `set -u` or `set -euo pipefail`;
- no `exit` that will execute in the live interactive shell;
- every expected-negative command is wrapped explicitly;
- complex logic runs as a child script;
- helper/diagnostic files are outside the repo or ignored;
- exact expected branch/HEAD/worktree guards are present when needed;
- the command prints a clear PASS or STOP result;
- the next action after STOP is inspection, not blind rerun.

The desired outcome is not fewer safeguards. It is safeguards that fail safely without killing the workspace the owner is using.