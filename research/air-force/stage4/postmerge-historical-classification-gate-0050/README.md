# Air Force — Stage 4 post-merge verification / exact historical H/A/N decision (0050)

## Verified technical status

Protected main `229c8302b67112e1b86b8c24006fd904269b4b42` contains merged narrow tooling PR [#738](https://github.com/pollackelliott/college-basketball-history/pull/738).
[Permanent postmerge replay #46182826135](https://github.com/pollackelliott/college-basketball-history/actions/runs/46182826135) completed SUCCESS on the exact merged main against unchanged Stage3B COMPLETE input (SHA256 `c16590d92fe2bf013acde3edd0eebd7eed68bb132421c017b57c41162c356945`).

Permanent Stage4 preflight PASS, 1928/1928 scores intact, 1928/1928 guide literal lines intact, 1865 PDF page refs, zero unaccounted venue gaps. **Stage4 acceptance FAIL on exactly one game-site relationship error.** See machine-readable `status.json` and exact [postmerge replay proof](https://github.com/pollackelliott/college-basketball-history/blob/da39e5ab47a83ec0453d3674d4dc8e648fc39a77/research/air-force/stage4/postmerge-replay-0050/postmerge-proof.json).

## Narrow historical discrepancy

One game: `AF-1959-60-006`, Air Force **63**, DePaul **69**, March 7, 1960, NCAA first round. Original accepted Stage3B source-site classification **HOME** and venue Alumni Hall, Chicago, Illinois. Proposed **NEUTRAL**, same exact venue and all other game facts unchanged.

Primary first-party [Air Force schedule](https://goairforcefalcons.com/sports/mens-basketball/schedule/1959-60) uses `vs DePaul`, which is not itself proof of HOME for an NCAA first-round tournament event. DePaul's [institutional history](https://depaulbluedemons.com/documents/download/2020/3/17/DePaulAtoZ_2020.pdf) independently documents the first-round NCAA game **at Alumni Hall**, a DePaul home facility. Game-specific [Air Force](https://www.sports-reference.com/cbb/schools/air-force/men/1960-schedule.html) and [DePaul](https://www.sports-reference.com/cbb/schools/depaul/men/1960-schedule.html) Sports Reference season schedules both mark the game `N`, corroborated by [MCubed](https://mcubed.net/ncaab/yearly/af/1960.shtml). Original [March 4, 1960 AP newspaper report](https://oregonnews.uoregon.edu/lccn/sn85042470/1960-03-04/ed-1/seq-33/) confirms DePaul Gym hosted the NCAA first-round matchup.

This judgment is based on exact NCAA game-level H/A/N evidence and contemporaneous first-round context, **not** geography alone. Do not construe host-court advantage as the NCAA's recorded home/away designation.

## Authority and next step

Current Stage4 is mechanical under `AGENTS.md` and `docs/research-stage4-authoring-contract.md`; it may not silently reopen accepted Stage3B historical truth. **No school basketball data were mutated.** The required one-game historical decision is whether to authorize an immutable-parent-preserving Stage3B successor that changes **only** this game's H/A/N from HOME to NEUTRAL and then replays the permanent Stage4 coordinator; exact venue/scores/identity/event/source lines stay untouched. Stage5 NON_D1 owner scan has **not** begun.

If owner authorizes it, this is one bounded historical-correction unit, not reopening the full Stage3B or Stage3A populations.
