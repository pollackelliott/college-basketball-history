# Basketball History — v0.1.0 checkpoint

Date: August 9, 2026

## Completed release

- Public site: https://college-basketball-history.vercel.app
- Repository branch: `main`
- Release commit: `2b86483`
- Annotated tag: `v0.1.0` — “Six-program public prototype”
- Local `main` and `origin/main` were clean and synchronized at the stopping point.
- Production QA passed for loading, routing, search, filters, pagination, matchup history, responsive behavior, and all six published programs.
- Published programs: Arkansas, Illinois, Kansas, Kentucky, Missouri, and Northwestern.

## Next session

Begin the data-expansion phase from the protected `v0.1.0` checkpoint. No expansion work has started yet. Preserve the current six programs as the regression set while deciding the first expansion batch and validating the existing ingestion, canonicalization, publication, and site-generation pipeline against it.

## Product follow-up

Clean up the deployed website’s mobile display before the next public release. Perform a dedicated mobile QA and refinement pass covering the header/navigation and search experience, card spacing, filters, pagination, typography, touch targets, conference accordions, and horizontally scrolling history tables at common phone widths. Verify the resulting production deployment on a narrow viewport and, if available, a physical phone.

## Resume checkpoint

Start by reopening the Codespace and confirming:

```bash
cd /workspaces/college-basketball-history
git status -sb
git show --no-patch --decorate --oneline v0.1.0
```

Expected branch status: `## main...origin/main`.
