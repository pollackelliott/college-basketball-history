# Connector-only request prepublication validation bridge

This is a **read-only** execution bridge for connector-only Implementation lanes. It runs the existing protected-main `prepare_exact_request` implementation, which invokes the unchanged permanent `verify_request_predecessor` and request validator. It never publishes a control request, acquires a mutation lock, or grants an owner gate.

## Invocation

1. Authenticate current protected `main`, `control/remote-implementation`, and the relevant school/checkpoint authority. Prepare a complete authorized request **template** with `expected_protected_main_sha` but **without** either `previous_control_state_*` field.
2. Create a fresh branch named `request-validation/<unique-request-id>` from protected main using the GitHub connector. Commit **only** `.remote-implementation/validation-template.json` with the exact template JSON using the connector. The push triggers `connector-request-validation.yml`; no workflow-dispatch capability is needed.
3. Wait for the exact Actions run and require success. Retrieve the two files from its `connector-request-validation-<run>-<attempt>` artifact: `request.json` and `receipt.json`. Require `status=VALIDATED_NOT_PUBLISHED`, the exact triggering input commit, expected request ID, operation, SHA-256 of the **raw** request bytes, exact protected-main runtime SHA, and control predecessor/state hash.
4. **Before publication**, independently re-fetch both live refs. Require they still equal the receipt's main and control SHA. Re-fetch the raw control-state Git blob and require its SHA-256 equals the receipt. Create exactly one commit whose immediate parent is that control SHA, changing only `.remote-implementation/request.json` to the **exact artifact bytes**. Use connector expected-head compare-and-swap on `control/remote-implementation`. Any changed ref, missing artifact, wrong bytes, validator failure, or CAS rejection is a **STOP**, never a silent retry.
5. The published request is **not** accepted until the existing remote runner processes it and independent fresh verification succeeds. The ordinary serialized Implementation lock, historical authority, owner gates, Preview, merge, and Production proof remain unchanged.

## Security and scope

- The workflow triggers only for a template-file push to `request-validation/**`. It has `contents: read` and checks out the **protected-main** validator runtime, never executing code from the untrusted template branch.
- The validator fetches both authoritative refs afresh, hashes raw control-state blob bytes, checks safely idle control, replay identity, complete operation-specific schema/authority, and predecessor hashes, then rechecks both refs before producing the artifact.
- A successful Actions run proves validation **at the receipt's exact refs only**. It does not authorize publication if either ref moves afterward. The connector publisher still owns exact-parent/CAS.
- No branch other than the temporary validation branch is changed by this workflow. Templates must contain no credentials/secrets. The artifact expires after seven days.
- If the connector cannot retrieve and verify the **exact artifact bytes** or cannot CAS-publish the exact request, stop; do not replace the permanent validator with an improvised implementation.
- This bridge is generic for ordinary and expansion remote requests. It does not make Kentucky-specific assumptions and does not automate stage progression.

The workflow must first be merged to protected main through ordinary review/CI. Do not use its presence on an unmerged tooling branch as proof of operational readiness.
