# Program badge and compact-header labels

Website presentation only. The source of truth is
`data/reference/program-display-labels.csv`, keyed by immutable `program_key`.
It has two owner-curated columns:

- `badge_initialism`: displayed in circular program badges in team and matchup
  views; size scales to fit the circle.
- `header_short`: shown in sticky team and series navigation **only if**
  the full registered display name cannot fit. Full team-page titles, accessible
  full names, program identity, and historical records do not change.

`tools/build_site_data.py` checks that every program registered in
`data/reference/programs.csv` has exactly one complete entry and writes the
deterministic `site/data/program-display-labels.json`. The web app loads that
asset before displaying teams. The ordinary site freshness check covers it.

## Owner roster reconciliation — October 2026

The owner supplied a 365-school table. The current protected-main registry
also contains 365 programs, but its membership differs in one place:
Saint Francis is absent and West Florida is registered. The original supplied
Saint Francis proposal (`SFU`, `SF`) is preserved in this branch's first
version of the CSV, but is not an active program mapping. The current-row
West Florida mapping (`WFLA`, `WF`) is a clearly identified provisional
presentation choice, not an identity or historical judgment.

The table's “Miami” maps to the existing `miami` (Miami FL) key, and
“New Orleans” maps to `new-orleans` (registered as LSU New Orleans).
No change to the global program registry was necessary.

If a program joins or leaves the current Division I registry, update the CSV
for the new full program set in the same deliberate presentation change.
Do not synthesize unreviewed aliases or modify program keys to make labels fit.
