# Postseason Tagging Semantics

## NCAA tournament provenance versus appearance accounting

`game_type=NCAA_TOURNAMENT` is the broad repository provenance type for
NCAA-administered tournament/postseason games. It does not, by itself, prove
that a game belongs to the national championship bracket for program
accomplishment accounting.

Most NCAA tournament rows count toward an NCAA Tournament appearance season.
Historical qualifying or district-playoff formats are the narrow exception.
When accepted Research establishes that an NCAA-administered game was a
qualifier/district playoff **rather than a national-bracket round**, preserve
the historical source row and keep the standardized NCAA round blank rather
than inventing a modern round.

For current Research, make that distinction explicit in the source `notes`
with the durable token:

`[NCAA_NON_APPEARANCE_QUALIFIER]`

Accepted legacy Research wording containing the exact semantic phrase
`qualifier rather than a national-bracket round` is compatible and is
normalized in memory to the same canonical marker. This compatibility exists
so an immutable accepted Research Freeze does not need to be rewritten merely
to adopt the newer token.

The permanent source-to-canonical projection appends the canonical marker
`[NCAA_NON_APPEARANCE_QUALIFIER]` only when all of the following are true:

- `normalization_status=RESEARCH_ACCEPTED`;
- `curated_game_type=NCAA_TOURNAMENT`;
- `curated_postseason_round` is blank; and
- the accepted source note carries the durable marker or the exact compatible
  legacy phrase above.

A blank NCAA round alone is never sufficient.

`derive_ncaa_accomplishments()` excludes only canonically marked
non-appearance qualifier games when counting NCAA Tournament appearance
seasons. Genuine historical NCAA appearances whose exact old-format round is
honestly unresolved continue to count and continue to emit the ordinary
missing-round diagnostic.

If an explicitly marked qualifier matches an existing canonical game that
already carries a nonblank NCAA round, that is a competing historical
assertion. The round must be surfaced for Gate 1 review; the qualifier marker
must not be silently applied over the nonblank canonical round.

This distinction changes accomplishment representation only. It does not
change the game result, date, opponent, H/A/N, venue, raw source evidence,
broad NCAA provenance, or the accepted Research conclusion.
