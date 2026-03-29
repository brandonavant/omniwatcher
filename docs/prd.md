# OmniWatcher -- Product Requirements Document

## Document Header

| Field          | Value           |
|----------------|-----------------|
| Version        | v1.0            |
| Date           | 2026-03-28      |
| Author         | Brandon Avant   |
| Change Summary | Initial version |

---

## Ubiquitous Language

These terms are authoritative across all spec documents, the UI, and the codebase. Do not introduce synonyms.

| Term                    | Definition                                                                                    |
|-------------------------|-----------------------------------------------------------------------------------------------|
| **Watcher**             | The persistent entity a user creates -- defines what to monitor, where to look, and how often |
| **Check**               | A single scheduled execution of a watcher -- one run of fetch, evaluate, decide               |
| **Source**              | A specific URL or discoverable location a watcher monitors                                    |
| **Source list**         | The set of sources associated with a watcher                                                  |
| **Change trigger**      | A user-defined criterion for what constitutes a meaningful change (e.g., "new trailer")       |
| **Alert**               | The notification payload delivered to the user when a check detects a meaningful change       |
| **Webhook destination** | The user-configured HTTPS endpoint where alerts are delivered                                 |
| **Onboarding**          | The research step during watcher creation where the system discovers sources                  |
| **Watcher memory**      | The per-watcher record of what has already been seen and reported                             |
| **Watcher history**     | The user-facing chronological log of past alerts for a watcher                                |

---

## 1. Vision and Overview

OmniWatcher is a web-based monitoring tool that automatically watches the web for information changes that matter to a
specific user. It eliminates the tedious cycle of manually re-checking Google searches, Reddit threads, official sites,
and social media for updates on niche topics -- things like convention ticket availability, game remake announcements,
or evolving technical subjects. Users describe what they care about, point at trusted sources, and OmniWatcher runs on a
schedule to detect meaningful changes, filter for relevance and source quality, and deliver concise actionable alerts.

The core thesis: people who track events, products, announcements, and evolving interests across fragmented tools
(bookmarks, calendars, email, ad hoc notes) lose important updates because the manual process is inconsistent and
exhausting. OmniWatcher replaces that fragmented process with a single system that quietly watches, remembers context,
and tells the user what matters -- when it matters.

## 2. Target Persona

**Primary persona: The Curious Tracker**

- Fairly technical, highly curious individual who actively follows niche topics across the web.
- Currently, tracks information through a fragmented mix of Google searches, bookmarks, Reddit, official sites,
  calendars, email, and ad hoc notes.
- Comfortable with technology but does not want complexity for its own sake.
- Cares about: **relevance, timing, and signal quality** -- the right sources monitored, low-value noise filtered out,
  and actionable information surfaced at the right moment.
- Does NOT care about: power-user workflow complexity, dashboards full of knobs, or managing the tool itself.
- Wants a system that works reliably in the background with minimal management overhead.
- **Experience breakers:** Alerts that repeat information already seen. Noise from low-quality sources drowning out
  signal. Having to manually check whether the tool is actually running. Any workflow that requires more effort than the
  manual process it replaces.

## 3. Feature Requirements

### F-01: Natural-Language Watcher Creation

Users create a watcher by describing what they want to track in plain language. The system extracts goals, change
triggers, and schedule from the description, then researches and assembles an appropriate source list automatically.

- **AC-01:** User can create a watcher from a single natural-language prompt (e.g., "Track the Silent Hill 1 Remake for
  me. Check daily at 09:00 and let me know about new trailers, newly-announced dates, delays, and release arrivals").
- **AC-02:** The system parses the prompt to extract: the topic to monitor, the change triggers to watch for, and
  a requested schedule (defaulting to daily if unspecified).
- **AC-03:** After parsing, the system performs an onboarding research step -- an up-front web search to discover
  relevant, authoritative sources for the topic (official sites, publisher pages, prominent community hubs, etc.).
- **AC-04:** The system presents the discovered sources to the user for confirmation before the watcher goes live. The
  user can accept, remove, or add sources during this step.
- **AC-05:** A watcher cannot be promoted to active/live state while ambiguity or missing information remains. If the
  system cannot determine a clear topic, at least one viable source, or what constitutes a meaningful change, it must
  prompt the user for clarification before activation.
- **AC-06:** The onboarding flow surfaces all unresolved questions in a single follow-up rather than activating with
  silent defaults. The user explicitly confirms or provides the missing pieces before the watcher goes live.

### F-02: Scheduled Monitoring with Meaningful Change Detection

Automatic recurring checks that determine whether something actually changed in a way that matters, not just that a page
was updated.

- **AC-01:** Each watcher runs on a user-configured schedule (minimum frequency: hourly).
- **AC-02:** The system fetches content from the watcher's source list on each check.
- **AC-03:** Change detection evaluates whether fetched content represents a meaningful change relative to the watcher's
  goal -- not just a page edit, timestamp update, or cosmetic change.
- **AC-04:** The system reads only the minimum context needed to make a relevance decision, respecting external rate
  limits and token costs.

### F-03: Relevance and Source Quality Filtering

Distinguish between authoritative high-signal sources and noise; surface updates from places that matter rather than
weak commentary or low-value reposts.

- **AC-01:** The system assigns a signal quality assessment to each source result based on the source's relationship to
  the watcher's goal (e.g., official announcement vs. forum speculation).
- **AC-02:** Low-signal results (weak commentary, reposts, tangential mentions) are deprioritized or excluded from
  alerts.
- **AC-03:** Users can review and adjust the source list after creation -- add, remove, or change trust levels for
  individual sources.

### F-04: Concise Actionable Alerts

Notify the user with a short summary of what changed, why it matters, and a link back to the source. Alerts are
delivered via webhook so the user does not need to be on the site to receive them.

- **AC-01:** When a meaningful change is detected, the system generates an alert containing: a summary of what changed,
  why it matters relative to the watcher's goal, and a direct link to the source for verification.
- **AC-02:** Alerts are delivered via outbound webhook -- an HTTP POST to a user-configured HTTPS endpoint with a shared
  secret for authentication (e.g., key in header or URL). This covers both generic HTTP receivers and services like
  Discord that accept standard webhook POSTs.
- **AC-03:** Each user configures at least one webhook destination. A watcher does not activate without a configured
  delivery target.
- **AC-04:** Alerts are informative but not verbose -- comparable in length and density to a typical Discord channel
  announcement. Exact length constraints and payload format (Markdown, HTML, plain text) are determined in
  `docs/architecture.md` based on webhook destination capabilities.
- **AC-05:** Each alert is associated with exactly one watcher.
- **AC-06:** Whether generic HTTP webhooks and Discord webhooks can be served by a single unified mechanism (both are
  HTTPS POSTs with a secret in the URL) or require separate handling is assessed in `docs/architecture.md`.

### F-05: Per-Watcher Memory and History

Remember what has been seen, avoid repetition, show how a topic has evolved over time, and provide continuity across
checks.

- **AC-01:** Each watcher maintains its own memory of previously seen content and prior alerts.
- **AC-02:** The system does not generate duplicate alerts for information it has already reported.
- **AC-03:** Users can view a watcher's history -- a chronological log of past alerts and detected changes.
- **AC-04:** History provides continuity: the user can see how a topic has evolved over time across multiple check
  cycles.

### F-06: Simple Watcher Management

Create, edit, pause, resume, and review watchers through a straightforward interface.

- **AC-01:** Users can view all their watchers in a single list with status indicators (active, paused).
- **AC-02:** Users can edit a watcher's description, sources, schedule, and change triggers after creation.
- **AC-03:** Users can pause a watcher (stops scheduled checks) and resume it later.
- **AC-04:** Users can delete a watcher and its associated history.
- **AC-05:** The management interface is simple enough that the user never falls back to doing the work manually.

### F-07: User Authentication

Standard user sign-in flow for the web application.

- **AC-01:** Users register with email and password.
- **AC-02:** Users log in and receive a session.
- **AC-03:** All application endpoints (except health check) require a valid authenticated session.
- **AC-04:** Users can log out (session invalidated).

## 4. Non-Functional Requirements

- **N-01: Cost-Conscious Architecture.** Prefer scale-to-zero and consumption-based services. Avoid always-on
  infrastructure unless there is a compelling reason. Critical early on with a small user base.
- **N-02: Rate Limit and Token Cost Respect.** Watchers run on sensible schedules, avoid unnecessary polling, and read
  only the minimum context needed to make a decision.
- **N-03: Minimum Check Frequency.** Hourly. Users cannot schedule checks more frequently than once per hour.
- **N-04: Data Minimization.** Store only what is needed. Protect personal context.
- **N-05: Intentional Data Retention.** Watcher history and results are kept. Raw fetched content and transient context
  are not retained forever without a product reason.
- **N-06: Secure Authentication.** Standard user sign-in flow. Proper secret management for third-party integrations.
  No plaintext passwords. CSRF protection. Input sanitization on all user content.
- **N-07: Multi-User from Day One.** Authentication, user isolation, and data ownership boundaries designed correctly
  from the start. Not full enterprise tenancy, but correct foundational boundaries.
- **N-08: Correctness Over Speed.** Watcher results prioritize correctness, relevance, and cost efficiency over
  real-time latency. The interactive web experience should still feel responsive.
- **N-09: Prefer Established Off-the-Shelf Solutions.** For complex cross-cutting concerns -- LLM evaluations, prompt
  injection defense, content sanitization, authentication -- prefer mature, well-maintained libraries and services from
  reputable sources (e.g., Microsoft, OWASP, major cloud providers) over hand-rolled implementations. The codebase
  should not contain custom security suites, evaluation frameworks, or sanitization pipelines when a proven
  off-the-shelf
  option exists. The architecture phase must include a research step to identify and evaluate available tooling before
  designing custom solutions.
- **N-10: LLM Output Evaluations.** Core LLM-driven behaviors -- watcher prompt parsing, change detection, relevance
  filtering, and alert generation -- must be covered by evaluation suites that establish a quality baseline and catch
  regressions. The system cannot ship or update LLM prompts without passing evaluations. Evaluation design, tooling,
  and pass criteria are defined in `docs/architecture.md`.
- **N-11: LLM Security and Prompt Injection Mitigation.** The system processes two untrusted input channels through LLM
  calls: user-authored watcher descriptions and web content fetched from external sources. Both are prompt injection
  vectors. The architecture must apply defense-in-depth mitigations aligned with industry-understood standards (e.g.,
  OWASP LLM Top 10). At minimum:
    - **Input/output separation.** Untrusted content (user input, fetched web content) must be structurally isolated
      from
      system instructions in every LLM call. Use delimited injection boundaries, not string concatenation.
    - **Input sanitization.** User-authored descriptions and fetched content are sanitized before inclusion in
      prompts --
      strip or neutralize known injection patterns (role overrides, instruction leaks, encoded payloads).
    - **Output validation.** LLM outputs that drive system behavior (e.g., parsed watcher parameters, alert generation
      decisions) are validated against expected schemas before being acted upon. The system never executes free-form LLM
      output as code, queries, or system commands.
    - **Least privilege.** LLM calls operate with the minimum context and capability needed for the task. No single
      prompt has access to cross-user data, system credentials, or administrative functions.
    - **Indirect injection defense.** Fetched web content is the highest-risk vector because it is fully attacker-
      controlled. The system must treat all fetched content as adversarial and apply additional scrutiny -- e.g.,
      summarization prompts for fetched content should not be able to alter watcher configuration, exfiltrate data, or
      influence other watchers.
    - **Monitoring and logging.** Anomalous LLM behavior (unexpected output structure, repeated failures, outputs that
      fail validation) is logged for review. Specific mitigations and their implementation details are documented in
      `docs/architecture.md`.

## 5. Content Policy and Constraints

- Watcher descriptions and source lists are user-generated text. No moderation required at MVP (personal/small-user
  tool).
- Alert summaries are LLM-generated based on fetched web content. Summaries must attribute their source and link back
  for verification -- the system does not present generated content as ground truth.
- **Trust boundaries.** The system has three trust levels: (1) system instructions -- fully trusted, never exposed to
  users or external content; (2) user input -- partially trusted (authenticated user, but still untrusted for prompt
  construction); (3) fetched web content -- fully untrusted, attacker-controlled. Every LLM call must make the trust
  level of each input explicit in its prompt structure.
- No file uploads at MVP.
- No third-party integrations at MVP (Google Calendar, Gmail, etc.).

## 6. Non-Goals (Explicit)

The following are explicitly NOT in scope for MVP:

- General autonomous agent or broad personal-assistant platform behavior.
- Multistep autonomous task execution or broad workflow automation.
- Third-party integrations (Google Calendar, Gmail, Slack, etc.) -- no external connectors at MVP.
- Gmail or email ingestion.
- Native mobile apps.
- CLI-first workflows.
- Real-time or every-minute monitoring.
- Advanced collaboration features (shared watchers, team features).
- Sophisticated source-authority modeling beyond basic signal/noise filtering.
- Email, SMS, or push notification alert delivery -- MVP uses outbound webhooks only.

## 7. Open Questions

- **OQ-01:** What authentication provider will be used? (Deferred -- to be decided during architecture.)
- **OQ-02:** Can generic HTTP webhooks and Discord webhooks be consolidated into a single delivery mechanism, or do they
  require separate handling? (To be assessed in architecture.)
- **OQ-03:** What is the maximum number of watchers per user? (To be assessed in architecture with cost modeling.)
- **OQ-04:** What is the maximum number of sources per watcher? (To be assessed in architecture with cost modeling.)
- **OQ-05:** Should watcher deletion be a soft delete (recoverable) or hard delete? (To be assessed in architecture
  with data retention implications.)
- **OQ-06:** LLM provider selection is deferred -- to be chosen during architecture based on capability, fit, and cost.
