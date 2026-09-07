# Bounded Implementation Protocol Compatibility Notes

This note records the intended relationship between `docs/implementation-lane-bounded-execution.md` and the existing onboarding documentation.

- The new bounded protocol changes **chat turn boundaries and continuation semantics only**.
- `docs/school-onboarding-fast-path.md`, `docs/onboarding-process-hardening.md`, `docs/implementation-efficiency-recovery.md`, and `docs/codespace-terminal-safety.md` remain controlling for the mechanics and safety rules executed inside each bounded stage.
- Owner Gate 1 remains one consolidated historical decision packet.
- Exact Preview visual approval remains mandatory and applies only to the exact PR-head SHA.
- Production proof remains mandatory after merge.
- Purely technical failures do not reopen unchanged historical decisions.
- The owner's Codespace should be used only when needed and in phase-sized, compact-output operations; the bounded protocol does not claim terminal access that the chat does not possess.
- `Proceed` / `Continue` authorizes only the next identified ordinary implementation stage or unfinished remainder. It never substitutes for a required owner historical decision or exact Preview approval.

No school data, schema, canonical data, tooling, or release behavior is changed by this documentation.
