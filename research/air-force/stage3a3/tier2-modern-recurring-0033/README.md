# Air Force — Stage 3A-3 modern recurring tranche 0033

This is the first bounded Tier 2 tranche after authenticated Tier 1 COMPLETE checkpoint 0032. It resolves 12 regular-season NEUTRAL game sites across three recurring tournament source families: Bimini Jam/Junkanoo Jam (6), Sun Bowl Invitational (3), and All-Military Classic (3).

The 116-row stage3a3-neutral-row-state.json is the new row-level authoritative Stage 3A-3 neutral state overlay keyed by research_game_id. It records original Stage 3A-2 venue fields separately from accepted Tier 1 and newly documented Tier 2 facts; the committed Stage 3A-2 ledger remains byte-exact and unchanged. The 75-row remaining-neutral-queue.json preserves original row evidence verbatim from the checkpoint 0032 residual for unfinished rows.

Each tier2-accepted-site-evidence.json member binds an exact opponent/game and official source URLs, with no venue inference from location, prior editions, or home arena convention. Family sources and attempted modes are captured in family-source-register.json.

The root manifest.json seals all members by Git object hashes. Protected main 242370fc551fd749c157c74d92917ddfafbe40e0 and Research base 3f5a15458aa468347e56e669327d6fe4c9c6ee69 remain immutable.

Tier 2 is IN PROGRESS after this tranche. Residual: modern 30, historical 45. Stop here; next assignment is remaining recurring families, not modern one-offs.
