# Technology Picks Require Web Research

When recommending, selecting, or evaluating any technology, library, framework, service, or pricing model, you MUST
perform live web research before presenting a recommendation. Training knowledge is unreliable for anything that changes
faster than the training cycle -- versions, pricing, deprecation status, maintenance health, and ecosystem rankings all
qualify.

## What triggers this rule

Any response that includes or relies on:

- A specific technology, library, or framework recommendation
- A version number for any dependency
- Pricing for any service or API
- A claim that something is "current," "recommended," "standard," or "best practice"
- A claim that something is deprecated, unmaintained, or end-of-life
- A comparison of competing tools or services
- A rejection of a technology option (you must verify the reason for rejection is still accurate)

## Required research steps

Before presenting a pick, you must verify the following via web search:

1. **Current version and maintenance status.** Is the project actively maintained? When was the last release? Is it in
   maintenance mode or deprecated?
2. **Deprecation and end-of-life status.** Has the vendor announced retirement? What is the migration timeline? Are
   there successor products?
3. **Current pricing.** For paid services, what are the actual current rates? Has the pricing model changed? Are there
   free tiers?
4. **Ecosystem fit.** Does it integrate with the rest of the chosen stack? Are there known incompatibilities with
   current versions of adjacent tools?
5. **Alternatives.** Have newer or better-fit options emerged since training? Search explicitly for "[category]
   alternatives 2026" or similar.
6. **Supply chain risk assessment.** For every third-party dependency, evaluate:
   - **Maintainer count and bus factor.** Single-maintainer projects with no organizational backing are high risk.
     Search for the project on Snyk Advisor or Socket.dev for health scores.
   - **Release recency.** No releases in 12+ months with no explanation is a red flag for both staleness and
     potential account takeover risk (dormant accounts are prime targets for credential theft).
   - **Security policy.** Does the project have a SECURITY.md or documented responsible disclosure process? Missing
     security policies mean vulnerabilities may go unreported or unpatched.
   - **Known vulnerabilities and incidents.** Search for "[package name] vulnerability" and "[package name] supply
     chain attack" to check for recent security incidents.
   - **Transitive dependency exposure.** Check whether the package pulls in high-risk transitive dependencies. The
     March 2026 litellm/TeamPCP supply chain attack demonstrated that compromised packages propagate through
     transitive dependency chains (DSPy, CrewAI, MLflow, LangChain were all affected indirectly). Search for
     "[package name] dependencies" or check PyPI/npm for the dependency tree.
   - **Prefer platform-native or standard-library solutions** over single-purpose third-party packages when the
     functionality is simple (e.g., rate limiting, CSRF tokens, session management). Fewer dependencies = smaller
     attack surface.

## How to research

- Use `WebSearch` or delegate to a research agent with web access.
- Search for the specific technology by name + "2026" (or the current year).
- Check official documentation, release pages, changelogs, and pricing pages.
- Cross-reference community sources (GitHub issues, blog posts, comparison articles) for deprecation signals and
  real-world adoption status.

## What to disclose

- If web research returns conflicting or unclear information, say so. Do not fill gaps with training knowledge and
  present it as verified.
- If a search fails or returns stale results, flag the uncertainty rather than falling back to training data silently.
- Always note when a pick has a known risk factor (acquisition, maintenance mode, upcoming deprecation, low community
  adoption).

## Exceptions

- **Internal project patterns.** If the user has an existing codebase that already uses a technology, you do not need to
  re-research that technology's existence. You should still verify its current version and maintenance status if you are
  recommending continued use or referencing specific features.
- **Trivial standard-library or language-builtin references.** You do not need to web-search Python's `hashlib` or
  TypeScript's `Promise`. This rule applies to third-party dependencies and external services.
- **The user explicitly asks you to skip research.** Honor the request, but note that the recommendation is based on
  training knowledge and may be stale.
