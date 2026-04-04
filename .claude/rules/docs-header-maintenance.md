---
paths:
  - "docs/**/*.md"
---

# Document Header Maintenance

When editing any file in `docs/`, you MUST update the Document Header table before finishing. Do not skip this step.

## Required updates on every edit

1. **Version** -- bump the patch segment for small fixes (typos, wording tweaks). Bump the minor segment for substantive
   changes (new sections, revised requirements, architectural decisions).
2. **Date** -- set to today's date in `YYYY-MM-DD` format.
3. **Author** -- set to the name of the person or agent making the change.
4. **Change Summary** -- write a concise, single-line description of what changed. Reference a decision ID (e.g.,
   `AD-12`) when one exists.

## Canonical header format

The header must appear immediately after the document's H1 title, as an H2 section with a Markdown table:

```markdown
## Document Header

| Field          | Value                        |
|----------------|------------------------------|
| Version        | v1.2                         |
| Date           | 2026-04-01                   |
| Author         | Brandon Avant                |
| Change Summary | Revise alert delivery design |
```

Do not add, remove, or reorder columns. Do not change the section heading.

## Exempt files

- `docs/interview-summary.md` -- raw interview notes; no Document Header required.
