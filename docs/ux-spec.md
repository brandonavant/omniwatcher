# OmniWatcher -- UX Specification

## Document Header

| Field          | Value                                                                               |
|----------------|-------------------------------------------------------------------------------------|
| Version        | v1.2                                                                                |
| Date           | 2026-04-01                                                                          |
| Author         | Brandon Avant                                                                       |
| Change Summary | Add viewport meta tag, mobile input handling, orientation, and performance guidance |

---

## 1. Navigation and Layout

### Global Layout

- **Top bar:** Logo and product name ("OmniWatcher") left-aligned. Navigation links center-aligned: Watchers, Webhooks.
  User avatar menu right-aligned (dropdown: Settings, Log out).
- **Main content area:** Centered container, max-width 960px. Scrollable independently, from the top bar.
- **No sidebar.** The feature set is compact enough for top-bar navigation. A sidebar would add complexity without
  value for the target persona.

### Responsive Breakpoints

| Breakpoint | Width        | Layout Change                                                              |
|------------|--------------|----------------------------------------------------------------------------|
| Mobile     | < 768px      | Navigation collapses to hamburger menu. Content fills full viewport width. |
| Tablet     | 768 - 1024px | Top-bar navigation visible. Content container max-width 720px.             |
| Desktop    | > 1024px     | Top-bar navigation visible. Content container max-width 960px.             |

### Viewport Configuration

The application must include the following viewport meta tag:

```html

<meta name="viewport" content="width=device-width, initial-scale=1">
```

**Rules:**

- Do NOT set `maximum-scale` or `user-scalable=no`. Users must be able to pinch-to-zoom for accessibility (WCAG 1.4.4
  Resize Text). The iOS auto-zoom issue on form fields is solved by rendering inputs at 16px or larger (see Section 3
  Form Validation), not by disabling zoom.
- Do not set `minimum-scale`. The browser default is acceptable.
- Next.js sets this tag automatically via the `metadata` export in `app/layout.tsx`. Verify it is present and not
  overridden.

## 2. Screen Specifications

### 2.1 Login

**URL:** `/login`

**Layout:** Centered card (max-width 400px) with the OmniWatcher logo above.

**Fields:**

- Email (text input, type `email`).
- Password (text input, type `password`, with show/hide toggle).
- "Log in" primary button (full-width).
- "Don't have an account? Register" link below the button, navigates to `/register`.

**Behavior:**

- On success: redirect to `/watchers`.
- On failure (invalid credentials): inline error above the form -- "Invalid email or password."
- On failure (network): inline error -- "Unable to reach the server. Please try again."
- Button shows a loading spinner during submission. Button is disabled while loading.

**States:**

- **Loading (submission):** Button disabled with spinner. Fields remain visible but disabled.

### 2.2 Register

**URL:** `/register`

**Layout:** Centered card (max-width 400px) with the OmniWatcher logo above.

**Fields:**

- Name (text input).
- Email (text input, type `email`).
- Password (text input, type `password`, with show/hide toggle). Minimum 8 characters.
- Confirm password (text input, type `password`).
- "Create account" primary button (full-width).
- "Already have an account? Log in" link below the button, navigates to `/login`.

**Validation:**

- Passwords must match. Mismatch shown as inline error below the "confirm password" field on blur.
- Email format validated on blur. Invalid format shown as inline error.
- All fields required. Empty fields flagged on submit.
- Password minimum 8 characters, validated on blur.

**Behavior:**

- On success: redirect to `/watchers`.
- On failure (email taken): inline error -- "An account with this email already exists."
- On failure (network): inline error -- "Unable to reach the server. Please try again."

### 2.3 Watcher List (Home)

**URL:** `/watchers`

**Layout:** Page heading "Watchers" with a "+ New watcher" primary button right-aligned in the heading row. Below the
heading, a vertical list of watcher cards.

**Watcher cards:**

Each card displays:

- **Parsed topic** as the card title (single line, truncated with ellipsis if over 80 characters).
- **Status badge:** "Active" (green) or "Paused" (amber). Displayed inline after the title.
- **Schedule summary** as secondary text. Rendered type-specifically:
    - `frequency`: "Every N hours at HH:MM TZ"
    - `days_of_week`: "Mon, Wed, Fri at HH:MM TZ" (abbreviated day names)
    - `specific_date`: "Once on MMM DD, YYYY at HH:MM TZ"
- **Source count:** "N sources" as tertiary text.
- **Last check:** Relative timestamp ("2h ago", "3d ago") or "No checks yet" if `last_check_at` is null.
- **Next check:** Absolute timestamp rendered in the user's local timezone, or "Paused" if status is paused.

**Interactions:**

- **Click card:** Navigates to `/watchers/:id` (watcher detail).
- **"+ New watcher" button:** Navigates to `/watchers/new`.

**Sorting:** Watchers are sorted by status (active first, paused second), then by `next_check_at` ascending within
each group. This is server-determined; no client-side sort controls at MVP.

**States:**

- **Loading:** Skeleton cards (3 placeholders) matching the card layout.
- **Empty (no watchers):** Centered message with illustration: "No watchers yet. Create one to start tracking what
  matters." with a "+ New watcher" primary button.
- **Error (load failure):** Inline error banner above the card list with a "Retry" button.

### 2.4 Watcher Creation

**URL:** `/watchers/new`

A multistep flow. The user stays on `/watchers/new` throughout; steps are rendered in place, not as separate routes.
A step indicator at the top shows progress: **Describe** > **Review** > **Active**. The browser does not add history
entries for step transitions (no back-button confusion).

#### Step 1: Describe

**Layout:** A single large text area (6 rows minimum, auto-expands) with placeholder text:

> Describe what you want to track, why it matters, and how often to check. For example: "Track the Silent Hill 1
> Remake for me. Check daily at 09:00 and let me know about new trailers, newly-announced dates, delays, and release
> arrivals."

Below the text area: a "Continue" primary button.

**Validation:**

- Description is required. Empty submission shows inline error: "Please describe what you want to track."
- Maximum 2000 characters. A character counter appears below the text area when the user has typed 1500+ characters.
  Exceeding 2000 disables the "Continue" button with inline error: "Description must be under 2000 characters."

**Behavior on submit:**

- Button changes to a loading state with a spinner. The text area becomes read-only.
- The button label updates progressively as the system works through the onboarding pipeline:
    1. "Analyzing your description..." -- displayed immediately on submit. The system is parsing the user's
       description to extract the topic, change triggers, and schedule.
    2. "Discovering sources..." -- displayed when parsing completes. The system is searching the web for relevant,
       authoritative sources.
    3. "Assessing source quality..." -- displayed when source discovery completes. The system is evaluating each
       source's relevance and trustworthiness.
- Each status transition replaces the previous button label. The spinner remains visible throughout.
- If the system cannot determine a clear topic or change triggers, it returns clarification questions instead of
  proceeding to source discovery. The clarification questions are displayed below the text area as a bulleted list
  with a heading: "We need a bit more detail." The button reverts to "Continue" and the text area becomes editable.
  The user edits their description to address the questions and resubmits. Clarification questions are cleared on
  resubmission.
- On successful completion of all steps: transition to Step 2 with the parsed configuration and discovered sources
  pre-populated.

**Error:**

- If the system encounters an error at any point during analysis: the spinner stops, the button reverts to
  "Continue", the text area becomes editable, and an inline error appears above the button -- "Something went wrong.
  Please try again."
- If the process does not complete within a reasonable time: the same error state is shown. No automatic retry; the
  user resubmits to restart the process from the beginning.

#### Step 2: Review

**Layout:** The system presents the parsed watcher configuration for the user to confirm or adjust. Sections are
stacked vertically.

**Sections:**

1. **Description** (read-only display of the user's original text, with an "Edit" link that returns to Step 1 with the
   text preserved).

2. **Topic** (read-only display of the parsed topic). Not directly editable -- if the topic is wrong, the user returns
   to Step 1 and rewrites the description.

3. **Change triggers** (editable list).
    - Displayed as a list of chips/tags. Each trigger has an "x" button to remove it.
    - An inline text input below the list allows adding new triggers. Press Enter or click "Add" to add.
    - At least one trigger is required. Removing the last trigger shows an inline error: "At least one change trigger
      is required."

4. **Schedule** (editable).
    - Displayed as a human-readable summary (same format as the watcher card).
    - An "Edit" button opens an inline editing section:
        - **Schedule type selector:** Three radio buttons: "Recurring interval", "Days of the week", "Specific date".
        - Fields change based on type:
            - *Recurring interval:* Frequency dropdown (1h, 2h, 4h, 6h, 8h, 12h, 24h, 48h, 72h, 168h) and preferred time
              picker (HH:MM).
            - *Days of the week:* Day checkboxes (Mon-Sun) and one or more time pickers (add/remove times, minimum
              60-minute
              gap enforced).
            - *Specific date:* Date picker (future dates only) and time picker.
        - Timezone displayed below the fields as a read-only label sourced from the user's profile timezone. Not
          editable
          in this flow.
    - "Save" confirms edits. "Cancel" reverts to the previous schedule.

5. **Sources** (editable list).
    - Displayed as a list. Each source shows:
        - An icon indicating type: globe icon for URL sources, magnifying glass icon for search sources.
        - Label (the user-facing display name).
        - Trust level badge: "High" (green), "Medium" (amber), "Low" (muted).
        - An "x" button to remove the source.
    - An "Add source" button opens an inline form:
        - Type selector: "URL" or "Search query".
        - Value input: URL field (`type="url"`, `inputmode="url"`, validated as HTTPS) or free-text search query
          (`inputmode="search"`).
        - Label input: user-facing name.
        - "Add" button.
    - At least one source is required. Removing the last source shows an inline error: "At least one source is
      required."
    - Sources discovered during onboarding have their trust level pre-set by the system. Users can remove low-trust
      sources but cannot change trust levels directly at MVP (the system assigns trust levels).

**Bottom actions:**

- "Create watcher" primary button.
- "Back" secondary button (returns to Step 1 with all data preserved).

**Behavior on submit:**

- "Create watcher" button changes to "Creating..." with spinner.
- On success: transition to Step 3.
- On failure: inline error above the buttons -- "Something went wrong. Please try again."

#### Step 3: Active

**Layout:** A success confirmation card.

- Checkmark icon.
- "Your watcher is live." heading.
- Summary: parsed topic, next check time.
- "View watcher" primary button (navigates to `/watchers/:id`).
- "Create another" secondary button (resets the flow to Step 1).

### 2.5 Watcher Detail

**URL:** `/watchers/:id`

**Layout:** Two sections stacked vertically: configuration summary at the top, alert history below.

#### Configuration Summary

Displays the watcher's current configuration in a card:

- **Parsed topic** as the heading.
- **Status badge** inline with the heading: "Active" (green) or "Paused" (amber).
- **Description** (collapsible, collapsed by default if longer than 200 characters, with a "Show more" / "Show less"
  toggle).
- **Change triggers** displayed as chips/tags (read-only in this view).
- **Schedule** displayed as a human-readable summary.
- **Sources** displayed as a compact list (icon, label, trust level badge).
- **Last check:** Relative timestamp or "No checks yet".
- **Next check:** Absolute timestamp in the user's local timezone, or "Paused".

**Actions (top-right of the card, rendered as an overflow menu accessed via a "..." button):**

- **Edit** -- navigates to `/watchers/:id/edit`.
- **Pause** (shown when active) -- pauses the watcher. Confirmation dialog: "Pause this watcher? Scheduled checks
  will stop until you resume it." with "Pause" (destructive style) and "Cancel" buttons. On confirmation, the status
  badge updates to "Paused" and the next check field changes to "Paused".
- **Resume** (shown when paused) -- resumes the watcher. No confirmation needed. Status badge updates to "Active" and
  the next check time is recalculated and displayed.
- **Delete** -- soft-deletes the watcher. Confirmation dialog: "Delete this watcher? It will be permanently removed
  after 30 days." with "Delete" (destructive style) and "Cancel" buttons. On confirmation, the user is redirected to
  `/watchers`.

#### Alert History

**Heading:** "History" with a count of total alerts.

**Layout:** Reverse-chronological list of alert cards. Each alert card displays:

- **Title** (bold).
- **Summary** (Markdown rendered, truncated at 3 lines with a "Show more" / "Show less" toggle).
- **Source URLs** as clickable links (open in new tab).
- **Timestamp** in relative format ("2h ago") with the full absolute timestamp shown on hover as a tooltip.

**Pagination:** 20 alerts per page. "Load more" button at the bottom if more exist.

**States:**

- **Loading:** Skeleton alert cards (3 placeholders).
- **Empty (no alerts):** "No alerts yet. This watcher will notify you when it detects meaningful changes."
- **Error (load failure):** Inline error banner with a "Retry" button.

### 2.6 Watcher Edit

**URL:** `/watchers/:id/edit`

**Layout:** Same section layout as Step 2 of watcher creation (change triggers, schedule, sources), pre-populated with
the watcher's current values. The description and parsed topic are displayed as read-only context at the top (not
editable after creation -- the user would create a new watcher instead).

**Editable sections:**

- Change triggers (same interaction pattern as creation Step 2).
- Schedule (same interaction pattern as creation Step 2).
- Sources (same interaction pattern as creation Step 2).

**Bottom actions:**

- "Save changes" primary button.
- "Cancel" secondary button (navigates back to `/watchers/:id` without saving).

**Behavior on submit:**

- "Save changes" button changes to "Saving..." with spinner.
- On success: redirect to `/watchers/:id` with a success toast -- "Watcher updated."
- On failure: inline error above the buttons.

**Constraint:** If the watcher's schedule is changed and the watcher is active, the orchestration is restarted (handled
server-side). The user does not need to take any additional action.

### 2.7 Webhook Destinations

**URL:** `/webhooks`

**Layout:** Page heading "Webhook Destinations" with a "+ Add destination" primary button right-aligned. Below the
heading, a vertical list of destination cards.

**Destination cards:**

Each card displays:

- **Name** as the card title.
- **Type badge:** "Generic" or "Discord".
- **URL** (displayed truncated, showing the domain and a portion of the path).
- **Default badge** (if `is_default` is true): "Default" label.
- An overflow menu ("..." button) with: Edit, Send test, Delete.

**Interactions:**

- **"+ Add destination" button:** Opens the add/edit dialog (see below).
- **Edit:** Opens the add/edit dialog pre-populated with the destination's current values.
- **Send test:** Sends a test webhook payload to the destination. Shows a transient toast on result:
  "Test delivered successfully." (on 2xx/204) or "Test delivery failed: {reason}." (on error).
- **Delete:** Confirmation dialog: "Delete this webhook destination? Watchers will no longer deliver alerts to it."
  with "Delete" (destructive style) and "Cancel" buttons. On confirmation, the card is removed.

**Add/Edit Dialog:**

A modal dialog with fields:

- **Name** (text input, required, max 100 characters).
- **Type** selector: "Generic webhook" or "Discord webhook" (radio buttons). Selecting a type updates the hint text
  on the URL field.
- **URL** (text input, `type="url"`, `inputmode="url"`, required, validated as HTTPS URL).
    - Generic hint: "The HTTPS endpoint that will receive POST requests."
    - Discord hint: "Paste your Discord webhook URL (starts with https://discord.com/api/webhooks/)."
- **Set as default** checkbox. If checked, this destination becomes the default. Only one destination can be default.
- "Save" primary button. "Cancel" secondary button.

**Note:** The secret for generic webhooks is generated server-side and is not displayed or editable by the user. After
creation, the secret is shown once in a success dialog: "Webhook destination created. Your signing secret is:
`{secret}`. Copy it now -- it will not be shown again." with a copy-to-clipboard button.

**States:**

- **Loading:** Skeleton cards (2 placeholders).
- **Empty (no destinations):** Centered message: "No webhook destinations configured. Add one so your watchers can
  deliver alerts." with a "+ Add destination" primary button. This message also appears as a warning banner on the
  watcher creation flow (Step 2) if the user has no destinations.
- **Error (load failure):** Inline error banner with a "Retry" button.

### 2.8 Settings

**URL:** `/settings`

**Layout:** Page heading "Settings". A single card with account information.

**Sections:**

- **Profile:** Name (editable inline), email (read-only display).
- **Password:** "Change password" button. Opens an inline form: current password, new password, confirm new password.
  "Save" and "Cancel" buttons.
- **Timezone:** Dropdown with IANA timezone options, pre-selected to the user's current profile timezone. Changing the
  timezone affects how schedules are displayed and how new watcher schedules default. Existing watcher schedules are
  not retroactively changed (they store their own timezone).
- **Danger zone:** "Delete account" button with destructive styling. Confirmation dialog: "Delete your account? All
  your watchers, alerts, and webhook destinations will be permanently deleted. This action cannot be undone." with
  "Delete my account" (destructive) and "Cancel" buttons.

## 3. Interaction Patterns

### Keyboard Navigation

- `Tab` moves focus through interactive elements in document order.
- `Escape` closes any open dialog, dropdown, or overflow menu.
- `Enter` activates the focused element (buttons, links, form submissions).
- Arrow keys navigate within dropdowns and menus.

### Loading States

- **Page load:** Skeleton screens matching the content layout (not a centered spinner). Skeletons pulse with subtle
  animation.
- **Action in progress:** Button shows a loading spinner replacing its label text. Button is disabled during the
  action. For multi-second operations (watcher creation analysis), the button label updates progressively through
  named stages as each step completes: "Analyzing your description...", "Discovering sources...", "Assessing source
  quality..." (see Section 2.4, Step 1 for the full sequence).
- **Optimistic updates:** Pause, resume, and delete actions update the UI immediately. If the server rejects the
  change, revert the UI and show an error toast.

### Toast Notifications

- Displayed at the bottom-right of the viewport (bottom-center on mobile).
- Auto-dismiss after 5 seconds. Include a manual dismiss button ("x").
- Used for: successful save confirmations, test webhook results, action errors that do not warrant inline errors.
- Maximum 3 toasts visible simultaneously. Older toasts dismissed when the limit is exceeded.

### Confirmation Dialogs

- Used for destructive actions: pause watcher, delete watcher, delete webhook destination, delete account.
- Modal overlay with dimmed background. Focus is trapped within the dialog.
- Always include a clear description of what will happen, a destructive-styled confirm button with specific label
  (e.g., "Delete", "Pause" -- never generic "OK"), and a "Cancel" button.

### Form Validation

- **Client-side validation** runs on blur for individual fields and on submit for the full form. Shows inline error
  messages below the relevant field with a red border on the field.
- **Server-side validation** is authoritative. Client-side validation is for UX responsiveness only.
- Error messages are specific: "Email must be a valid email address", not "Invalid input."
- **Mobile input sizing:** All `<input>`, `<select>`, and `<textarea>` elements must render text at 16px or larger on
  viewports below 768px. This prevents iOS Safari from auto-zooming the page when a form field receives focus. See
  brand-identity.md Section 4 "Responsive Type Scale" for the authoritative rule.

### Mobile Input Handling

#### Input Mode Attributes

Every form field must specify the correct `type` and `inputmode` attributes to invoke the appropriate mobile keyboard.

| Field                                 | `type`     | `inputmode` | Keyboard Behavior            |
|---------------------------------------|------------|-------------|------------------------------|
| Email (login, register)               | `email`    | `email`     | Shows @ and . keys           |
| Password (login, register, settings)  | `password` | --          | Secure entry                 |
| Name (register, settings)             | `text`     | `text`      | Standard keyboard            |
| URL (webhook destination, source add) | `url`      | `url`       | Shows / and .com keys        |
| Search query (source add)             | `text`     | `search`    | Shows search/go key          |
| Description (watcher creation)        | --         | `text`      | Standard keyboard (textarea) |
| Time picker (schedule)                | `time`     | --          | Native time picker           |
| Date picker (specific date schedule)  | `date`     | --          | Native date picker           |

#### Virtual Keyboard and Viewport

- Use the Visual Viewport API (`window.visualViewport`) to detect keyboard appearance rather than relying on
  `window.innerHeight` changes, which are unreliable across browsers.
- **Scroll-on-focus:** When a field receives focus and the keyboard appears, scroll the field into view using
  `Element.scrollIntoView({ block: 'center', behavior: 'smooth' })` after a 100ms delay (to allow the keyboard
  animation to settle).
- **Toast anchoring:** Fixed-position toasts must anchor to the visual viewport. When the keyboard is open, toasts
  appear above the keyboard, not behind it.
- **No pinned bottom buttons alongside keyboard.** Bottom-aligned action buttons (watcher creation "Continue", watcher
  edit "Save changes") should scroll into view naturally with the form, not be pinned to the visual viewport bottom.
  Pinned buttons consume too much of the already-reduced viewport when the keyboard is open.

#### Focus Management on Mobile

- **Validation errors:** On form submission failure on mobile, scroll the first errored field into view and focus it.
- **Modal open (full-screen on mobile):** Focus the first interactive element. On close, return focus to the trigger
  element.
- **Step navigation (watcher creation):** When transitioning between steps, focus the first interactive element of the
  new step.

## 4. Accessibility

**Target:** WCAG 2.2 Level AA. All success criteria for this level apply. Reference the canonical
[WCAG 2.2 specification](https://www.w3.org/TR/WCAG22/) for the full list of requirements.

**Product-specific accessibility notes:**

- **Confirmation dialogs** must trap focus within the dialog and return focus to the trigger element on close. The
  dialog must be announced via `role="alertdialog"` with `aria-describedby` linking to the dialog description.
- **Status badges** (Active, Paused, trust levels) use color. The status text label must always be present alongside
  the color so that no information is conveyed by color alone.
- **Toast notifications** must use `role="status"` with `aria-live="polite"` so screen readers announce them without
  interrupting the user's current task.
- **Step indicator** in the watcher creation flow must convey progress to assistive technology via `aria-current="step"`
  on the active step and descriptive text (e.g., "Step 1 of 3: Describe").
- **Markdown-rendered alert summaries** in the history section must produce semantic HTML (headings, lists, links) so
  that screen readers can navigate them meaningfully.
- **Focus indicators** must be custom (not browser default) and clearly visible against both light and dark surface
  colors. The focus ring must meet a minimum 3:1 contrast ratio against adjacent colors per WCAG 2.4.11.

## 5. Responsive Behavior

| Component              | Mobile (< 768px)          | Tablet (768 - 1024px)    | Desktop (> 1024px)       |
|------------------------|---------------------------|--------------------------|--------------------------|
| Top bar navigation     | Hamburger menu            | Full navigation links    | Full navigation links    |
| Watcher cards          | Full-width, stacked       | Full-width, stacked      | Full-width, stacked      |
| Watcher creation steps | Full-width, stacked       | Centered (max 720px)     | Centered (max 720px)     |
| Watcher detail card    | Full-width                | Centered (max 720px)     | Centered (max 960px)     |
| Alert history cards    | Full-width                | Centered (max 720px)     | Centered (max 960px)     |
| Webhook cards          | Full-width, stacked       | Full-width, stacked      | Full-width, stacked      |
| Dialogs (modal)        | Full-screen               | Centered (max 480px)     | Centered (max 480px)     |
| Settings card          | Full-width                | Centered (max 720px)     | Centered (max 720px)     |
| Toasts                 | Bottom-center, full-width | Bottom-right (max 360px) | Bottom-right (max 360px) |
| Touch targets          | 44px min tap area         | 44px (pointer: coarse)   | Standard sizes           |

### Orientation Handling

OmniWatcher supports both portrait and landscape on all devices. The app does not lock orientation via the Screen
Orientation API or `manifest.json`.

**Landscape on phones** (< 768px width in portrait, typically < 400px height in landscape):

- Top bar remains in hamburger mode (orientation does not change the breakpoint).
- Full-screen dialogs remain full-screen but scroll vertically if content exceeds the reduced viewport height.
- Watcher creation Step 1 textarea: reduce minimum rows from 6 to 3 in landscape to leave room for the submit button
  above the fold.
- Form fields remain single-column. Do not switch to multi-column in landscape on phones -- the ~700px landscape width
  approaches but does not reach the tablet breakpoint, and multi-column on a phone creates awkwardly narrow columns.
- When viewport height is below 400px with the keyboard open, collapse the step indicator to a single-line text format
  ("Step 1 of 3") instead of the full visual indicator. This preserves the step context without consuming scarce
  vertical space.

**Landscape on tablets:** No special treatment needed. Tablet landscape typically exceeds 1024px width, which triggers
desktop layout automatically via the breakpoint system.

### Mobile Performance

#### Image Handling

OmniWatcher is a text-first interface at MVP (see brand-identity.md Section 8). There are no content images -- visual
richness comes from typography, color, and whitespace. The only raster assets are logo PNG variants (favicon, PWA
icons, OG image), which are loaded once and browser-cached. Lucide icons are imported as individual SVG components, not
as a sprite sheet or full icon font.

#### Lazy Loading

- **Route-based code splitting** is automatic via Next.js `app/` router. No additional configuration needed.
- **Modal and dialog components** (confirmation dialogs, webhook add/edit dialog) should be lazy-loaded using
  `next/dynamic` with `ssr: false` to keep them out of the initial bundle.
- **Alert history pagination** (Section 2.5) already avoids loading all alerts upfront (20 per page with "Load more").

#### Network Resilience

- **Offline indicator:** When `navigator.onLine` is false or the `offline` event fires, display a subtle top banner:
  "You're offline. Changes will sync when you reconnect." in `--color-warning` text on `--bg-surface`. Dismiss
  automatically on reconnection.
- **API request timeout:** 15 seconds. Show the standard network error toast on timeout (see Section 6).
- **Prefetch policy:** Next.js's default viewport-intersection prefetch for `next/link` is acceptable. Do not add
  custom aggressive prefetch logic. Respect the `Save-Data` client hint if present by disabling prefetch
  (`next/link` with `prefetch={false}`).

#### Bundle Considerations

- Keep total JavaScript bundle under 200KB gzipped for initial page load. No heavy client-side dependencies beyond
  React, Next.js, and the Tailwind runtime.
- Geist Sans and Geist Mono are loaded via `next/font` with automatic self-hosting, subsetting, and `display: swap`
  to prevent flash of invisible text on slower connections.

## 6. Error States Summary

| Error              | Display                            | Recovery                                                                |
|--------------------|------------------------------------|-------------------------------------------------------------------------|
| Network failure    | Toast, auto-retry                  | "Unable to reach the server. Please try again." after 3 retries         |
| Validation error   | Inline below input                 | Fix input and resubmit                                                  |
| 401 Unauthorized   | Redirect to `/login`               | Log in again                                                            |
| 403 Forbidden      | Full-page message                  | "You don't have access to this resource." with "Go to watchers" link    |
| 404 Not Found      | Full-page message                  | "This page doesn't exist." with "Go to watchers" link                   |
| 500 Server Error   | Toast                              | "Something went wrong. Please try again."                               |
| Watcher not found  | Full-page message                  | "This watcher doesn't exist or has been deleted." with "Go to watchers" |
| No webhook dest.   | Warning banner on creation         | "No webhook destinations configured." with link to `/webhooks`          |
| Onboarding failure | Inline error above button (Step 1) | Button reverts to "Continue"; user resubmits                            |
| Onboarding timeout | Same as onboarding failure         | User resubmits; no automatic retry                                      |
