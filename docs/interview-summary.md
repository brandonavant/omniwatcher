# OmniWatcher -- Project Interview Summary

## Product Vision

OmniWatcher is a web-based monitoring tool that automatically watches the web for information changes that matter to a
specific user, eliminating the tedious cycle of manually re-checking Google searches, Reddit threads, official sites,
and social media for updates on niche topics. It targets people who track events, products, announcements, and evolving
interests that may change suddenly or quietly over weeks or months -- things like convention ticket availability, game
remake announcements, or evolving technical topics -- and who are tired of fragmented, inconsistent manual processes
where important updates slip through the cracks.

## Target Persona

Fairly technical, highly curious individuals who currently track information across a fragmented mix of Google searches,
bookmarks, Reddit, official sites, calendars, email, and ad hoc notes. They are comfortable with technology but do not
want complexity for its own sake. What they care most about is **relevance, timing, and signal quality**: the right
sources monitored, low-value noise filtered out, and actionable information surfaced at the right moment. They want a
tool that quietly watches, remembers context, and tells them what matters -- whether that is an evolving technical topic
from authoritative sources, a limited-supply event ticket window opening, or a personal planning trigger tied to their
calendar. They do not care about power-user workflow complexity; they care that the system works reliably in the
background with minimal management overhead.

## Core Experience

The user creates a watcher by describing what they want to track, why it matters, and which sources to trust.
OmniWatcher then runs on a schedule, detects meaningful changes (not just page edits), filters for relevance and source
quality, and sends a concise alert with a summary of what changed, why it matters, and a link to verify. The system
remembers what it has already seen per watcher, avoids repeating itself, and builds continuity over time. For personal
use cases, the user can leave context-aware instructions that surface later when real-world conditions are met (e.g., a
calendar event approaching). Managing watchers -- creating, editing, pausing, resuming, reviewing -- is simple enough
that the user never falls back to doing the work manually.

### MVP Features

1. **Watcher creation with goals and source lists.** Define what to watch, why it matters, and which sources to trust
   (official sites, specific companies, prominent people, selected communities).
2. **Scheduled monitoring with meaningful change detection.** Automatic recurring checks that determine whether something
   actually changed in a way that matters, not just that a page was updated.
3. **Relevance and source quality filtering.** Distinguish between authoritative/high-signal sources and noise; surface
   updates from places that matter rather than weak commentary or low-value reposts.
4. **Concise actionable alerts.** Notify the user with a short summary of what changed, why it matters, and a link back
   to the source for quick verification.
5. **Per-watcher memory and history.** Remember what has been seen, avoid repetition, show how a topic has evolved over
   time, and provide continuity across checks.
6. **Conditional reminders tied to personal context.** Support leaving instructions that surface later when a real-world
   condition is met, such as a Google Calendar event approaching.
7. **Simple watcher management.** Create, edit, pause, resume, and review watchers through a straightforward interface.

## Tech Stack Decisions

- **Frontend:** Next.js, React, web application with both natural-language interaction (for creating/shaping watchers)
  and conventional management UI (for editing, pausing, deleting, reviewing)
- **Backend:** Python, FastAPI for the API layer
- **Database:** Cosmos DB (leaning toward for simplicity and cost; open to revisiting if relational storage proves
  clearly better)
- **Web Research:** Tavily (early favorite based on prior prototype performance)
- **LLM Provider:** Deferred -- to be chosen later based on capability, fit, and cost
- **Infrastructure:** Azure, scale-to-zero architecture (Azure Functions, possibly Container Apps)
- **IaC:** Terraform or OpenTofu for all infrastructure provisioning
- **CI/CD:** GitHub Actions
- **Source Control:** GitHub

## Non-Negotiables

- **Cost-conscious architecture.** Prefer scale-to-zero and consumption-based services; avoid always-on infrastructure
  unless there is a compelling reason. This is especially critical early on with a small user base.
- **Respect external rate limits and token costs.** Watchers run on sensible schedules, avoid unnecessary polling, and
  read only the minimum context needed to make a decision.
- **Minimum watcher frequency is hourly.** Users cannot create hyper-frequent tasks (e.g., every minute).
- **Data minimization.** Store only what is needed; protect personal context; scope third-party integrations (calendar,
  etc.) as narrowly as possible.
- **Intentional data retention.** Watcher history and results are kept; raw fetched content and transient context are not
  retained forever without a product reason.
- **Secure authentication.** Standard user sign-in flow for the web app; proper secret management for third-party
  integrations.
- **Multi-user from day one.** Authentication, user isolation, and data ownership boundaries designed correctly from the
  start, even though the initial user base is small. Not full enterprise tenancy, but correct foundational boundaries.
- **Correctness over speed.** Watcher results prioritize correctness, relevance, and cost efficiency over real-time
  latency. The interactive web experience should still feel responsive.

## Non-Goals (MVP)

- General autonomous agent or broad personal-assistant platform behavior
- Multistep autonomous task execution or broad workflow automation
- Large connector ecosystem -- v1 supports Google Calendar only for personal integrations
- Gmail or email ingestion
- Native mobile apps
- CLI-first workflows
- Real-time or every-minute monitoring
- Advanced collaboration features (shared watchers, team features)
- Sophisticated source-authority modeling beyond basic signal/noise filtering

## Deployment

- **Cloud:** Azure (personal subscription)
- **Environments:** Non-production and production within the same subscription
- **Domain:** bytehorizonforge.com (likely a subdomain), DNS managed in AWS Route 53 with the application running in
  Azure
- **Compute model:** Scale-to-zero (Azure Functions, Container Apps)
- **IaC:** Terraform/OpenTofu -- avoid manual portal-driven setup
- **User scope:** Multi-user architecture from the start; single primary user initially
