# Arizona State Stage 1 expansion historical-accounting candidate

**Candidate tooling only. No Stage 1 closeout or owner authority registry change is included.**

The candidate is intentionally pinned to Arizona State checkpoint 0018, its original
checkpoint transport, the exact immutable Research-base Git source blob, and the four
source-level aggregate-only season records. It is a separate extension of the
permanent early-history accounting tools; existing school closeouts are unchanged.

## Materialization

`tools/research_stage1_expansion_accounting.py materialize <checkpoint0018.zip> <research-base-source-games.csv> --checkpoint-sha f3391cca078e25f4e3a737b632026aa5636d0723519b3b95805688c7dbe6e10d --source-blob bb2e5ddb63e2caab96c2f3eb33d4d231bf75c875 --output <parent.zip>`

Default keeps all ten 1920–21 candidates provisional. The optional
`--accept-verified-candidates` is allowed only after the tool's complete literal
source, inclusion, source-game uniqueness, duplicate-key, exact 11-line detailed
record, and inherited NAU noncollision checks pass. The source-game IDs of all
469 inherited rows remain unchanged. The disputed ASC 42–13 assertion is never
introduced as a game, and the inherited Northern Arizona W45–13 remains intact.

Each result is a hashed, manifest-verified standalone *blocked* Stage 1 parent,
not a frozen or completed package. The checkpoint evidence and the original
research-base source-game CSV are embedded unchanged and reauthenticated.

## Separate owner-authority barrier

`audit` defaults to the protected-main reference
`data/reference/expansion-stage1-accounting-authorities.json`, which is **not
included in this candidate**. No such Arizona State authority currently exists.
A successful future audit must hash-bind a separately approved parent,
research base, identified-game ledger, 39-season census, explicit four-season
aggregate accounting (including the narrow 1943–44 wartime exception), exact
1920–21 record discrepancy, and terminal *contested source representation*
that does **not** assert game identity resolution.

`closeout` and `verify-closeout` additionally enforce exact audit SHA,
independent deterministic reproduction, and byte preservation of all parent
historical members. Neither command declares Stage 1 complete. A later distinct
repository-policy implementation and owner-authority action would be required
for formal Stage 1 completion.

### Candidate QA

Run `python -m unittest discover -s tests -p test_research_stage1_expansion_accounting.py -v`.
A dedicated exact-candidate workflow also checks the real immutable
Research-base file with Git and runs the full repository test suite.

The fixture registry in tests is synthetic and must **never** be treated as
historical owner authority. The positive-closeout test proves tooling logic
only, not permission to close Arizona State's Research Stage 1.
