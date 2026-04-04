# OmniWatcher -- Brand Identity and Design System

## Document Header

| Field          | Value                                                                                    |
|----------------|------------------------------------------------------------------------------------------|
| Version        | v1.2                                                                                     |
| Date           | 2026-04-01                                                                               |
| Author         | Brandon Avant                                                                            |
| Change Summary | Add mobile/responsive design guidance: touch targets, responsive typography, performance |

### Document Coverage

Every brand identity document should address these categories. Check each off as you complete it. If a section does not
apply to your product, state why -- do not silently omit it.

- [x] Antipattern awareness (Section 1)
- [x] Brand direction and positioning (Section 2)
- [x] Color system with approved pairings (Section 3)
- [x] Typography with type scale (Section 4)
- [x] Spacing and layout (Section 5)
- [x] Visual language: radii, elevation, borders (Section 6)
- [x] Iconography (Section 7)
- [x] Imagery, illustration, and logo system (Section 8)
- [x] Motion, animation, and loading states (Section 9)
- [x] Voice and tone (Section 10)
- [x] Anti-generic checklist (Section 11)

---

## Section 1: Why AI-Coded Apps Look Generic

Before defining what OmniWatcher should look like, we must catalog what it should NOT look like. These five antipatterns
appear in virtually every AI-coded application. Recognizing them is the first step to avoiding them.

### 1.1 Tailwind Default Syndrome

The agent uses the same utility classes on every component:

- `rounded-lg` on buttons, cards, inputs, avatars, modals -- all identical radius
- `bg-gray-50` and `bg-gray-100` as the only surface colors
- `p-4 gap-4` as universal spacing -- everything 16px apart, zero rhythm
- `shadow-sm` on every elevated surface
- `text-gray-500` as the only secondary text color

**Why it happens:** Agents optimize for "working correctly" not "looking intentional." Tailwind defaults are safe --
they never look broken, so agents never move past them.

### 1.2 Typography Flatness

- System font or Inter everywhere -- headings, body, labels, buttons, all the same face
- Two sizes: "normal" and "a bit bigger"
- No weight variation (everything is `font-medium`)
- No letter-spacing, no line-height differences, no typographic hierarchy
- Headings look like body text that got bigger

**Why it happens:** Agents treat typography as content delivery, not as a design element. They size text to fit, not to
create visual hierarchy.

### 1.3 Layout Monotony

- Everything in a CSS grid of equal-width cards
- All content centered in the viewport
- Same gap between every element on the page
- No asymmetry, no sidebar variation, no intentional whitespace
- Mobile layout is just the desktop layout reflowed into a single column

**Why it happens:** Grid layouts are the easiest to get right. Agents avoid asymmetry because it is harder to make
responsive.

### 1.4 Missing Personality

- Generic button text: "Submit", "Cancel", "Save", "Delete"
- Empty states: "No items found" with a gray icon
- Loading: centered spinner, nothing else
- Hover effects: lighter background color, nothing more
- No transitions, no motion, no delight anywhere

**Why it happens:** Personality requires understanding the product and its users. Agents do not have that context unless
you provide it explicitly in this document.

### 1.5 Dark Mode Failures

- Inverted light mode (swap white for near-black, call it done)
- All dark surfaces are the same shade -- no elevation hierarchy
- Pure white (#FFF) text on pure dark (#000) backgrounds -- harsh and fatiguing
- Accent colors at full saturation on dark backgrounds (vibrant to the point of glowing)
- Borders either invisible or too prominent

**Why it happens:** Agents apply dark mode as a color swap, not as a rethinking of elevation, contrast, and visual
weight.

---

## Section 2: Brand Direction

### 2.1 Brand Essence

**Quiet intelligence.** OmniWatcher is a focused monitoring interface that watches so you don't have to -- patient,
attentive, precise. It is a dark room with clear indicators: every element has a purpose, and when something lights up,
it means something.

### 2.2 Brand Attributes

| Attribute    | OmniWatcher IS                                   | OmniWatcher IS NOT                         |
|--------------|--------------------------------------------------|--------------------------------------------|
| Mood         | Calm, watchful, precise                          | Flashy, playful, aggressive                |
| Density      | Spacious but purposeful                          | Dashboard-dense or wastefully empty        |
| Color        | Deep navy base with sharp cyan signal accents    | Warm and cozy OR sterile corporate blue    |
| Typography   | Modern, clean, hierarchy through weight and mono | Decorative, serif, or uniformly sans-serif |
| Interactions | Quick, functional, minimal flourish              | Bouncy, animated, or theatrical            |

### 2.3 Target Audience Aesthetic

OmniWatcher's users are technically curious individuals who appreciate focused, well-crafted tools. They are not
necessarily developers, but they are comfortable with technology and have high taste in digital products. They are drawn
to tools that feel intelligent without showing off -- products like Linear (focused density), Vercel (typographic
clarity), and Better Stack (dark monitoring UI). They distrust products that feel over-designed or marketing-heavy.
Their aesthetic is refined utility: substance over style, but style as evidence of substance.

### 2.4 Competitive Visual Positioning

| Competitor    | Their Look                                       | Our Differentiation                                      |
|---------------|--------------------------------------------------|----------------------------------------------------------|
| Visualping    | Light, simple, screenshot-diff-focused           | Dark, LLM-driven intelligence, card-based not diff-based |
| Distill.io    | Light, utilitarian, browser-extension feel       | Web-native, richer card UI, no extension dependency      |
| Google Alerts | Minimal to the point of featureless, email-first | Full web UI with watchfulness as the core experience     |
| Uptime Robot  | White, dashboard-heavy, chart-centric            | No charts or graphs -- card-based alert history          |
| Datadog       | Dense, enterprise, dark but overwhelming         | Dramatically simpler, personal-scale, single-focus       |

**Design references:** Linear (component density and card design), Better Stack (dark monitoring UI with status
indicators), Vercel (typography and spacing discipline).

---

## Section 3: Color System

OmniWatcher uses a single dark theme. The palette is built on a deep navy base (not neutral gray) with cyan signal
accents that evoke digital monitoring. All colors are defined as CSS custom properties and exposed through Tailwind CSS
v4's `@theme` directive.

### 3.1 Core Palette

```css
:root {
    /* Background hierarchy (darkest to lightest) */
    --color-bg-base: #080C14; /* Page background -- deep navy-black */
    --color-bg-elevated: #0F1520; /* Cards, panels */
    --color-bg-surface: #182030; /* Inputs, hover states */
    --color-bg-overlay: #1E2A3C; /* Dropdowns, modals */

    /* Text hierarchy */
    --color-text-primary: #E2E8F0; /* Headings, important content -- warm off-white */
    --color-text-secondary: #8494A7; /* Descriptions, metadata */
    --color-text-tertiary: #4A5568; /* Placeholders, disabled */

    /* Accent (cyan -- "signal" color) */
    --color-accent: #22D3EE; /* Primary actions, links, focus rings */
    --color-accent-hover: #67E8F9; /* Hover state for accent elements */
    --color-accent-subtle: #22D3EE1A; /* Accent backgrounds (10% opacity) */

    /* Semantic */
    --color-success: #34D399; /* Active status, confirmations */
    --color-warning: #FBBF24; /* Paused status, caution */
    --color-error: #F87171; /* Errors, inline validation */
    --color-info: #60A5FA; /* Informational, non-actionable */

    /* Destructive button */
    --color-destructive: #B91C1C; /* Destructive action background */
    --color-destructive-hover: #991B1B; /* Destructive hover */
    --color-destructive-foreground: #E2E8F0; /* Text on destructive background */
}
```

### 3.2 Approved Color Pairings

Every text/background combination used in OmniWatcher must appear in this table. Contrast ratios are computed per WCAG
2.2 relative luminance formula.

| Foreground         | Background       | Contrast | Usage                       | WCAG AA |
|--------------------|------------------|----------|-----------------------------|---------|
| `--text-primary`   | `--bg-base`      | 15.9:1   | Primary text on page        | Pass    |
| `--text-primary`   | `--bg-elevated`  | 15.0:1   | Text in cards, panels       | Pass    |
| `--text-primary`   | `--bg-surface`   | 13.2:1   | Text in inputs              | Pass    |
| `--text-secondary` | `--bg-base`      | 6.3:1    | Metadata on page            | Pass    |
| `--text-secondary` | `--bg-elevated`  | 6.0:1    | Metadata in cards           | Pass    |
| `--text-tertiary`  | `--bg-surface`   | 2.2:1    | Placeholders (decorative)   | Exempt  |
| `--color-accent`   | `--bg-base`      | 10.9:1   | Accent text, links on page  | Pass    |
| `--color-accent`   | `--bg-elevated`  | 10.3:1   | Accent text, links in cards | Pass    |
| `--bg-base`        | `--color-accent` | 10.9:1   | Dark text on accent buttons | Pass    |
| `--destructive-fg` | `--destructive`  | 5.3:1    | White text on destructive   | Pass    |
| `--color-success`  | `--bg-base`      | 10.2:1   | Active badge text on page   | Pass    |
| `--color-success`  | `--bg-elevated`  | 9.6:1    | Active badge text in cards  | Pass    |
| `--color-warning`  | `--bg-base`      | 11.8:1   | Paused badge text on page   | Pass    |
| `--color-warning`  | `--bg-elevated`  | 11.1:1   | Paused badge text in cards  | Pass    |
| `--color-error`    | `--bg-base`      | 7.1:1    | Error text on page          | Pass    |
| `--color-error`    | `--bg-elevated`  | 6.7:1    | Error text in cards         | Pass    |

**Rules:**

- Do not create pairings outside this table. If a new pairing is needed, add it here with a verified contrast ratio
  first.
- Primary action buttons use dark text (`--bg-base`) on cyan (`--color-accent`) background. White text on cyan fails
  contrast (1.5:1).
- Destructive buttons use `--text-primary` on `--color-destructive` background.
- Semantic colors (success, warning, error) are used for text labels alongside status badges, never as background fills
  for large surfaces.

### 3.3 Banned Colors

Zero instances of these Tailwind defaults anywhere in the codebase:

`bg-gray-*`, `bg-zinc-*`, `bg-slate-*`, `bg-neutral-*`,
`text-gray-*`, `text-zinc-*`, `text-slate-*`, `text-neutral-*`,
`border-gray-*`, `border-zinc-*`, `border-slate-*`

Use the custom properties from Section 3.1 exclusively, mapped through `@theme`.

---

## Section 4: Typography

### Font Stack

| Role    | Typeface   | Weights  | Usage                                           |
|---------|------------|----------|-------------------------------------------------|
| Display | Geist Sans | 600, 700 | Page titles, section headers                    |
| Body    | Geist Sans | 400, 500 | Descriptions, content, labels, buttons          |
| Mono    | Geist Mono | 400      | Timestamps, URLs, source counts, technical data |

OmniWatcher uses Geist throughout (loaded via `next/font/google`). Geist is sharper and more geometric than Inter, with
distinctive character shapes that give the UI a technical feel without resorting to decorative typefaces. Typographic
personality comes from weight variation, tracking differences, and the deliberate use of Geist Mono for technical
content -- not from mixing display and body faces.

### Type Scale

| Token         | Size | Line Height | Weight | Letter Spacing | Usage                              |
|---------------|------|-------------|--------|----------------|------------------------------------|
| `--text-2xl`  | 24px | 32px        | 600    | -0.025em       | Page titles                        |
| `--text-xl`   | 20px | 28px        | 600    | -0.02em        | Section headers, card titles       |
| `--text-lg`   | 16px | 24px        | 500    | -0.01em        | Emphasis, sub-headers              |
| `--text-base` | 14px | 20px        | 400    | 0              | Body text, descriptions            |
| `--text-sm`   | 13px | 18px        | 400    | 0.005em        | Secondary text, metadata, captions |
| `--text-xs`   | 11px | 16px        | 500    | 0.03em         | Badges, labels, chip text          |

**Rules:**

- Every page must use at least 3 different sizes from this scale.
- Headings use tighter (negative) letter-spacing. Body and metadata use neutral or slightly positive letter-spacing.
  This contrast creates visual hierarchy beyond size alone.
- Geist Mono is used for all timestamps (relative and absolute), source counts ("5 sources"), schedule summaries
  ("Every 24h at 09:00"), URLs in source lists, and any system-generated identifiers.
- Weight 700 (bold) is reserved for page titles only. Do not use bold for emphasis within body text -- use weight 500
  or `--text-lg` instead.

### Responsive Type Scale

The desktop type scale above is the default. On mobile viewports (< 768px), the following adjustments apply:

| Token         | Desktop | Mobile | Change Rationale                                                     |
|---------------|---------|--------|----------------------------------------------------------------------|
| `--text-2xl`  | 24px    | 22px   | Slight reduction to fit narrower viewports without truncation        |
| `--text-xl`   | 20px    | 18px   | Proportional reduction; still visually distinct from `--text-lg`     |
| `--text-lg`   | 16px    | 16px   | No change -- 16px is the iOS auto-zoom threshold (see rule below)    |
| `--text-base` | 14px    | 14px   | No change -- body text remains readable at this size on mobile       |
| `--text-sm`   | 13px    | 13px   | No change                                                            |
| `--text-xs`   | 11px    | 12px   | Bumped up -- 11px is too small for badge/chip text in touch contexts |

Line-height, weight, and letter-spacing values remain the same across breakpoints. Tablet (768 - 1024px) uses the
desktop type scale with no separate adjustments.

**iOS auto-zoom prevention rule:** All `<input>`, `<select>`, and `<textarea>` elements must render text at 16px
(`--text-lg`) or larger on iOS. Inputs rendered at `--text-base` (14px) cause Safari to auto-zoom the viewport when the
field receives focus, disrupting layout and disorienting the user. This is solved by sizing inputs correctly -- not by
setting `maximum-scale=1` or `user-scalable=no` on the viewport meta tag, which harms accessibility.

**Implementation:** Define mobile type scale overrides in a `@media (max-width: 767px)` block within `:root`, or use
Tailwind responsive prefixes (`md:text-2xl` for the desktop value, `text-[22px]` as the mobile default).

---

## Section 5: Spacing and Layout

### Spacing Scale

```css
:root {
    --space-0: 0px;
    --space-1: 4px;
    --space-2: 8px;
    --space-3: 12px;
    --space-4: 16px;
    --space-5: 20px;
    --space-6: 24px;
    --space-8: 32px;
    --space-10: 40px;
    --space-12: 48px;
    --space-16: 64px;
}
```

**Rule:** Every screen must use at least 3 different spacing values. Uniform `p-4 gap-4` everywhere is a brand
violation.

### Layout Principles

- **No sidebar.** OmniWatcher uses top-bar navigation exclusively. The feature set is compact enough that a sidebar adds
  complexity without value (see UX spec Section 1).
- **Content container:** Max-width 960px (desktop), 720px (tablet for detail/creation views), full-width (mobile).
  Centered horizontally with `--space-6` horizontal padding.
- **Asymmetric vertical spacing.** Use more space above sections than below. Section headings get `--space-10` above and
  `--space-4` below. This creates clear visual grouping: the heading belongs to the content below it, not the content
  above it.
- **Card internal padding:** `--space-5` (20px) on desktop, `--space-4` (16px) on mobile. Not `--space-4` everywhere --
  the larger padding on desktop gives cards more breathing room.
- **Card list gaps:** `--space-3` (12px) between cards in a list. Tighter than the internal padding so the cards read as
  a unified list, not isolated islands.
- **Form field gaps:** `--space-5` (20px) between form fields. `--space-2` (8px) between a label and its input.
- **Button groups:** `--space-3` (12px) between buttons in a row.

### Touch Target Sizing

Interactive elements must meet minimum tap area requirements on touch devices to prevent mis-taps and satisfy WCAG
2.5.8 (Target Size).

| Element                        | Minimum Tap Area (mobile) | Desktop Size | Notes                                                        |
|--------------------------------|---------------------------|--------------|--------------------------------------------------------------|
| Primary / secondary buttons    | 44 x 44px                 | 36px height  | Full-width buttons on mobile inherently satisfy width        |
| Icon buttons (overflow, "x")   | 44 x 44px                 | 32 x 32px    | Use padding to extend hit area around the visual icon        |
| Navigation items (top bar)     | 44 x 44px                 | Natural size | Hamburger menu button and its items                          |
| Form inputs                    | 44px height               | 36px height  | Includes text inputs, selects, textareas, dropdowns          |
| Checkboxes / radio buttons     | 44 x 44px                 | 20 x 20px    | Tap area includes the label; visual indicator stays small    |
| Inline text links              | 44px line-height          | Natural size | Ensure sufficient vertical spacing between stacked links     |
| Chip / tag remove ("x") button | 44 x 44px                 | 24 x 24px    | Critical -- chips sit close together in trigger/source lists |

**Rules:**

- The 44px refers to the **tappable area**, not the visual element. A 16px icon button achieves 44px tap area with
  14px padding on each side. The visual element can remain its documented size.
- Adjacent interactive elements must have at least `--space-2` (8px) between their tap areas to prevent accidental
  activation of the wrong target.
- The 44px minimum is enforced below 768px. Between 768 - 1024px, enforce 44px for `pointer: coarse` devices; for
  `pointer: fine` (e.g., tablet with keyboard and trackpad), desktop sizes are acceptable.
- Use `@media (pointer: coarse)` to apply touch-specific sizing where breakpoint alone is insufficient. This correctly
  handles tablets in desktop-width landscape mode that still use touch input.

---

## Section 6: Visual Language

### 6.1 Corner Radius Strategy

| Component        | Radius        | Rationale                                                    |
|------------------|---------------|--------------------------------------------------------------|
| Buttons          | 6px           | Sharp and functional -- buttons are tools, not decorations   |
| Cards / panels   | 8px           | Slightly softer for content containers                       |
| Inputs           | 6px           | Matches buttons -- inputs and buttons sit side-by-side       |
| Modals / dialogs | 12px          | Larger containers get softer corners                         |
| Chips / badges   | 9999px (pill) | Status badges (Active, Paused) and change trigger tags       |
| Toasts           | 8px           | Matches cards -- toasts are floating content containers      |
| Tooltips         | 4px           | Tight, minimal -- tooltips are ephemeral                     |
| Step indicator   | 9999px (pill) | Step circles use pill shape to appear as circular indicators |

**Rule:** If a PR uses the same `border-radius` on buttons, cards, inputs, AND modals, it must be revised.

### 6.2 Elevation and Shadows

OmniWatcher's dark UI communicates depth through background color differentiation and luminance borders, not through box
shadows. Standard Tailwind shadows (`shadow-sm`, `shadow-md`, `shadow-lg`) produce muddy halos on dark backgrounds and
are banned.

| Level   | Treatment                                                                              | Usage                               |
|---------|----------------------------------------------------------------------------------------|-------------------------------------|
| Level 0 | No border. Flush with `--bg-base`.                                                     | Page background                     |
| Level 1 | `1px` border at `rgba(255, 255, 255, 0.06)`                                            | Cards, panels, inputs (unfocused)   |
| Level 2 | `1px` border at `rgba(255, 255, 255, 0.08)` + `box-shadow: 0 4px 12px rgba(0,0,0,0.3)` | Dropdowns, popovers, overflow menus |
| Level 3 | `1px` border at `rgba(255, 255, 255, 0.10)` + `box-shadow: 0 8px 24px rgba(0,0,0,0.5)` | Modals, confirmation dialogs        |

**Banned on dark surfaces:** Tailwind's `shadow-sm`, `shadow-md`, `shadow-lg`, `shadow-xl` -- these are calibrated for
light backgrounds.

### 6.3 Border Treatments

| Context           | Border                                        | Notes                                                   |
|-------------------|-----------------------------------------------|---------------------------------------------------------|
| Default border    | `rgba(255, 255, 255, 0.06)`, `1px`            | Barely visible, defines edges without drawing attention |
| Divider lines     | Same as default border                        | Used sparingly -- between major sections only           |
| Input (unfocused) | `rgba(255, 255, 255, 0.10)`, `1px`            | Slightly more visible than cards                        |
| Input (focused)   | `--color-accent`, `2px`                       | Cyan border signals active state                        |
| Input (error)     | `--color-error`, `2px`                        | Red border signals validation failure                   |
| Focus rings       | `--color-accent`, `2px outline`, `2px offset` | Use `outline` not `box-shadow` to avoid layout shift    |

### 6.4 Gradients

OmniWatcher uses gradients only for functional purposes:

- **Scroll fade:** `linear-gradient(to bottom, transparent, --color-bg-base)` at the bottom of the alert history list to
  indicate more content below.
- **No decorative gradients.** No purple-to-blue hero backgrounds, no gradient buttons, no gradient text. The UI is flat
  and intentional.

---

## Section 7: Iconography

### Icon Library

**Library:** Lucide Icons (lucide.dev)

**Why:** Clean stroke-based icons on a 24px grid. Maintained fork of Feather Icons with excellent coverage. Lucide is
the
default icon library used by shadcn/ui, which OmniWatcher's component library is built on. NOT Heroicons (signals
"Tailwind template"), NOT Font Awesome (too heavy, mixed styles).

### Icon Sizing

| Context               | Size | Notes                                                    |
|-----------------------|------|----------------------------------------------------------|
| Top bar navigation    | 20px | Logo, navigation items, user avatar menu                 |
| Inline actions        | 16px | Edit, copy, remove ("x" on chips), overflow menu ("...") |
| Source type indicator | 16px | Globe for URL sources, Search for search sources         |
| Empty states          | 40px | Large decorative icons, in `--text-tertiary`             |
| Status indicators     | 14px | Checkmark (success step), spinner (loading)              |
| Step indicator        | 16px | Step numbers or check icons in the watcher creation flow |

### Style Rules

- **Stroke weight:** 1.5px (Lucide default). Increase to 1.75px if icons feel thin against `--bg-base`.
- **Color:** Icons inherit text color by default. Apply `--color-accent` only when the icon represents an interactive
  element in its active/focused state.
- **Fill vs. stroke:** Stroke-only by default. Use filled variants only for selected/active states.
- **Consistency:** Every icon in the UI must come from Lucide. Mixing icon libraries is a brand violation.

---

## Section 8: Imagery and Illustration

OmniWatcher is a text-first monitoring tool. There are no hero images, no decorative illustrations, and no background
imagery. Visual richness comes from typography, color, and the deliberate use of whitespace -- not from graphics.

### 8.1 Empty State Treatments

| Context                    | Icon                              | Heading                                                                            | Action                     |
|----------------------------|-----------------------------------|------------------------------------------------------------------------------------|----------------------------|
| No watchers                | `eye` (40px, tertiary)            | "No watchers yet. Create one to start tracking what matters."                      | "+ New watcher" button     |
| No alerts (watcher detail) | `bell-off` (40px, tertiary)       | "No alerts yet. This watcher will notify you when it detects meaningful changes."  | None                       |
| No webhook destinations    | `webhook` (40px, tertiary)        | "No webhook destinations configured. Add one so your watchers can deliver alerts." | "+ Add destination" button |
| Load failure               | `alert-triangle` (40px, tertiary) | Context-specific error message (see UX spec Section 6)                             | "Retry" button             |

**Layout:** Icon centered above heading, both horizontally centered in the empty container. Heading uses
`--text-secondary` at `--text-base`. Action button appears `--space-3` below the heading.

### 8.2 Avatars

- **User avatars (top bar):** Circle-cropped, 32px. Fallback: user's initials (first letter of first and last name) on
  `--bg-surface` in `--text-secondary`, `--text-xs`, weight 500.
- **No product logo in content areas.** The logo appears in the top bar only. It does not repeat on cards, empty states,
  or loading screens.

### 8.3 Logo System

The logo is the single most visible brand asset. It must be defined with enough precision that an AI agent implementing
the frontend can produce it without design review cycles. OmniWatcher's logo is generated using AI vector tools and
refined by hand to meet production quality standards.

#### Design Direction

The logo reflects the brand essence from Section 2.1: **quiet intelligence**. It is a symbol of watchfulness -- not an
eye, not a magnifying glass (both overused in monitoring products), but a geometric abstraction that evokes focused
attention.

| Attribute  | Logo IS                                                            | Logo IS NOT                                             |
|------------|--------------------------------------------------------------------|---------------------------------------------------------|
| Shape      | Geometric, minimal, clean edges                                    | Ornate, illustrated, hand-drawn, organic                |
| Complexity | Recognizable at 16px (favicon scale)                               | Dependent on fine detail that disappears at small sizes |
| Palette    | `--color-accent` (#22D3EE) on dark, `--bg-base` (#080C14) on light | Multi-color, gradient-heavy, photorealistic             |
| Style      | Flat, solid fills, no gradients, no shadows                        | Skeuomorphic, 3D, glossy, embossed                      |
| Feeling    | Precise, technical, calm                                           | Aggressive, playful, corporate-generic                  |

#### Concept

The logo combines a **logomark** (standalone symbol) and a **logotype** (the word "OmniWatcher" in Geist Sans 600).
These are used together or separately depending on context. The logomark should be abstract-geometric -- think of a
stylized sensor, beacon, or concentric signal motif using clean lines and the cyan accent color. It must read clearly as
a single shape at 16x16 pixels.

#### Generation Workflow

The logo is generated as SVG using [Recraft](https://www.recraft.ai/) (the only major AI tool that outputs native SVG
vectors directly from prompts as of 2026). The workflow is:

1. **Generate in Recraft.** Use the SVG output mode with a flat/minimal style preset. Prompt for a geometric logomark on
   `--bg-base` (#080C14) using `--color-accent` (#22D3EE) as the primary shape color. Avoid prompting for text -- the
   logotype is set manually in Geist Sans.
2. **Clean up the SVG.** AI-generated SVGs average ~45% redundant data. Open the output in Figma, Inkscape, or
   Illustrator and: remove overlapping/fragmented paths, eliminate micro-gradients or shadows the AI may have added,
   simplify to the fewest `<path>` elements possible, and verify the shape is recognizable at 16px.
3. **Optimize.** Run the cleaned SVG through [SVGO](https://github.com/svg/svgo) to strip metadata and minimize file
   size.
4. **Set the logotype.** Create the wordmark "OmniWatcher" in Geist Sans weight 600. Pair it with the logomark
   horizontally (mark left, text right, `--space-2` gap). This is the "full logo" variant.
5. **Export all variants** listed in the asset table below.

**Licensing note:** Recraft Pro/Teams plans grant full commercial use rights. Make substantial human modifications
during
cleanup to strengthen copyright eligibility. Run a reverse image search and trademark search before committing to a
final design.

#### Required Variants

The logo must be exported in all of the following formats. AI agents building the frontend must reference these assets
from the project's `public/` directory.

| Asset                | Size / Scale | Format | File Name               | Usage                                               |
|----------------------|--------------|--------|-------------------------|-----------------------------------------------------|
| Full logo (dark bg)  | Scalable     | SVG    | `logo-full-dark.svg`    | Top bar on dark theme, marketing pages              |
| Full logo (light bg) | Scalable     | SVG    | `logo-full-light.svg`   | Social sharing backgrounds, print, external use     |
| Logomark only        | Scalable     | SVG    | `logo-mark.svg`         | Mobile top bar, compact contexts, loading states    |
| Favicon (modern)     | Scalable     | SVG    | `favicon.svg`           | Modern browsers; may embed `prefers-color-scheme`   |
| Favicon (legacy)     | 16/32/48px   | ICO    | `favicon.ico`           | Legacy browser fallback                             |
| Apple touch icon     | 180x180px    | PNG    | `apple-touch-icon.png`  | iOS home screen bookmark                            |
| PWA icon (standard)  | 192x192px    | PNG    | `icon-192.png`          | Android home screen, Lighthouse audit               |
| PWA icon (large)     | 512x512px    | PNG    | `icon-512.png`          | Splash screen, Lighthouse audit                     |
| PWA icon (maskable)  | 512x512px    | PNG    | `icon-512-maskable.png` | Android adaptive icon (safe zone padded)            |
| Open Graph image     | 1200x630px   | PNG    | `og-image.png`          | Social sharing cards (Facebook, LinkedIn, X, Slack) |

**Rules:**

- The maskable icon must keep the logomark within the central 80% safe zone so OS-applied shape masks do not clip it.
- The Open Graph image is not just the logo; it is a branded composition: logomark + "OmniWatcher" logotype + optional
  tagline, composed on `--bg-base` with `--color-accent` accents, at 1200x630px.
- All PNG exports are derived from the master SVG -- never upscale a small raster.
- Serve `favicon.svg` as the primary favicon with `favicon.ico` as fallback. Do not generate a full set of
  `favicon-16x16.png`, `favicon-32x32.png`, etc. -- the SVG + ICO combination covers all modern and legacy browsers.

#### Placement Rules

These rules consolidate and extend the placement guidance scattered across Sections 7 and 8.2:

- **Top bar:** Full logo (mark + logotype) on desktop/tablet. Logomark only on mobile (< 768px). Rendered at 20px
  height, matching Section 7's icon sizing table.
- **Login and register pages:** Full logo centered above the auth card, rendered at 32px height (larger than the top bar
  to create a focal point on otherwise minimal pages).
- **Favicon and PWA icons:** Logomark only, as listed in the asset table.
- **Open Graph image:** Full logo centered on a `--bg-base` background.
- **Nowhere else.** The logo does not appear on cards, empty states, loading skeletons, or within content areas.

#### Clear Space and Minimum Size

- **Clear space:** Maintain a minimum margin around the logo equal to the height of the logomark on all sides. No other
  elements (text, icons, borders) may intrude into this zone.
- **Minimum size:** The logomark must not be rendered smaller than 16x16px. The full logo (mark + logotype) must not be
  rendered smaller than 16px height.

---

## Section 9: Motion and Animation

### 9.1 Transition Rules

- **Duration:** Fast (100ms) for hover states and color changes, medium (200ms) for panels and dropdowns, slow (300ms)
  for modal entrances and page transitions. Never exceed 400ms.
- **Easing:** `ease-out` for entrances, `ease-in` for exits, `ease-in-out` for transforms.
- **What animates:** opacity transitions, slide-ins (dropdowns, overflow menus), scale (modals from 95% to 100%),
  height changes (collapsible description sections).
- **What does NOT animate:** color changes on text, layout reflows, scroll position.
- **Reduced motion:** Respect `prefers-reduced-motion`. Replace all animations with instant state changes. The skeleton
  pulse animation must also be disabled under reduced motion.

### 9.2 Loading States

| Context                                  | Treatment                                                                                                                          |
|------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Page load (watcher list, webhooks, etc.) | Skeleton cards matching content layout, pulsing at 1.5s cycle in `--bg-surface`                                                    |
| Page load (watcher detail)               | Skeleton card (config) + skeleton alert cards (3 placeholders)                                                                     |
| Inline action (save, delete, pause)      | Button enters disabled state with a 16px spinner replacing the label text                                                          |
| Watcher creation onboarding (Step 1)     | Button shows spinner + progressive label: "Analyzing your description...", "Discovering sources...", "Assessing source quality..." |
| Toast notification appearance            | Slide in from right (desktop) or bottom (mobile), 200ms ease-out                                                                   |
| Modal entrance                           | Fade in overlay (150ms) + scale modal from 95% to 100% (200ms ease-out)                                                            |

**Rule:** No bare centered spinners. Loading states must communicate structure (skeletons) or progress (labeled
spinners). A screen that shows only a spinner with no context violates the brand.

### 9.3 Optimistic Updates

Pause, resume, and delete actions update the UI immediately without waiting for the server response. If the server
rejects the change, the UI reverts and shows an error toast. This makes the interface feel fast and responsive despite
the serverless backend's cold-start latency.

---

## Section 10: Voice and Tone

### Principles

- **Direct.** "Watcher updated." not "Your watcher has been successfully updated!"
- **Specific.** "Email must be a valid email address." not "Invalid input."
- **Confident.** "Delete" not "Are you sure you want to delete?" (Use a confirmation dialog, but the button label is
  direct.)
- **Watchful, not robotic.** The system describes what it is doing in human terms: "Discovering sources..." not
  "Executing source discovery pipeline..." The AI is invisible infrastructure -- it watches, detects, and reports. It
  does not "generate", "predict", or "leverage AI."
- **No marketing language.** Avoid "powerful", "intelligent", "AI-powered", "leverage", "streamline", "unlock",
  "empower" in any user-facing text. The product proves itself through function, not adjectives.

### Button Labels

Button labels name the action they perform. Never generic ("Submit", "OK", "Confirm").

| Action                    | Label              | NOT                                                             |
|---------------------------|--------------------|-----------------------------------------------------------------|
| Create a new watcher      | "Create watcher"   | "Submit", "Save", "Confirm"                                     |
| Save edits                | "Save changes"     | "Update", "Submit"                                              |
| Start watcher creation    | "Continue"         | "Next", "Proceed"                                               |
| Add a webhook destination | "Save"             | "Submit", "Create"                                              |
| Remove a source           | "x" icon (no text) | "Remove", "Delete" (too heavy for chip removal)                 |
| Delete a watcher          | "Delete"           | "Remove", "OK"                                                  |
| Pause a watcher           | "Pause"            | "Disable", "Stop"                                               |
| Cancel an action          | "Cancel"           | "Back", "Close" (unless closing a modal with no pending action) |
| Sign in                   | "Log in"           | "Sign in", "Login" (one word)                                   |
| Create account            | "Create account"   | "Register", "Sign up"                                           |
| Test a webhook            | "Send test"        | "Test", "Ping"                                                  |

### Error Messages

Error messages tell the user what went wrong and how to fix it.

| Error                       | Message                                                  |
|-----------------------------|----------------------------------------------------------|
| Invalid credentials         | "Invalid email or password."                             |
| Network failure             | "Unable to reach the server. Please try again."          |
| Email already taken         | "An account with this email already exists."             |
| Validation (empty field)    | "{Field name} is required."                              |
| Validation (email format)   | "Email must be a valid email address."                   |
| Validation (password match) | "Passwords do not match."                                |
| Generic server error        | "Something went wrong. Please try again."                |
| Watcher not found           | "This watcher doesn't exist or has been deleted."        |
| Forbidden                   | "You don't have access to this resource."                |
| Onboarding failure          | "Something went wrong. Please try again." (above button) |

### Confirmation Dialogs

Confirmation dialogs state the consequence, not just the action:

- **Pause watcher:** "Pause this watcher? Scheduled checks will stop until you resume it."
- **Delete watcher:** "Delete this watcher? It will be permanently removed after 30 days."
- **Delete webhook:** "Delete this webhook destination? Watchers will no longer deliver alerts to it."
- **Delete account:** "Delete your account? All your watchers, alerts, and webhook destinations will be permanently
  deleted. This action cannot be undone."

### Forbidden Terms

Never use in user-facing text: "AI", "artificial intelligence", "model", "prompt", "generate", "inference", "token",
"pipeline", "LLM", "neural", "machine learning". These are implementation details, not product concepts. The user
creates watchers, receives alerts, and reviews history. The mechanisms behind these are invisible.

---

## Section 11: Anti-Generic Checklist

Run every item against each component or page. All Typography, Color, Layout, and Visual Language items must pass.
Interaction and Voice items should pass but can be deferred with justification.

### Typography (7 items)

1. [ ] At least 3 distinct font sizes are used on this screen.
2. [ ] At least 2 distinct font weights are visible.
3. [ ] Letter-spacing varies between headings and body (tighter on headings, neutral on body).
4. [ ] Line-height differs between headings and body text.
5. [ ] No text uses banned Tailwind default color utilities (`text-gray-*`, `text-zinc-*`, etc.).
6. [ ] Heading hierarchy is visually clear without relying on size alone (weight and tracking contribute).
7. [ ] Geist Mono is used for timestamps, source counts, schedule summaries, and URLs.

### Color (6 items)

8. [ ] Zero instances of banned Tailwind default color utilities.
9. [ ] Cyan accent appears in 1-2 focal points per screen (primary buttons, active links), not everywhere.
10. [ ] Body text contrast is 4.5:1 or higher (WCAG AA).
11. [ ] Surface colors create 3+ distinct elevation levels (base, elevated, surface, overlay).
12. [ ] Interactive elements have visible hover, focus, and active states.
13. [ ] Every text/background pairing exists in the approved pairings table (Section 3.2).

### Layout (7 items)

14. [ ] At least 3 different spacing values used on this screen.
15. [ ] Related items are visually grouped (tighter spacing within, more between).
16. [ ] Content is within the documented max-width constraints (960px desktop, 720px tablet).
17. [ ] Mobile and desktop layouts differ meaningfully (not just reflowed into a single column).
18. [ ] Intentional whitespace exists (section gaps are larger than intra-section gaps).
19. [ ] Touch targets meet 44px minimum tap area on mobile viewports (buttons, icons, links, inputs).
20. [ ] Landscape orientation does not break layout or hide critical controls on phone-sized viewports.

### Visual Language (4 items)

21. [ ] Corner radii vary by component type (not uniform across all elements).
22. [ ] Elevation is communicated through the defined system (luminance borders, not ad-hoc shadows).
23. [ ] Focus rings use `--color-accent` with `2px outline` and `2px offset` (not browser defaults).
24. [ ] Icons are from Lucide at the specified sizes.

### Interaction (4 items)

25. [ ] Button labels are specific to their action (no "Submit", "OK", "Confirm").
26. [ ] At least one micro-interaction exists (hover transition, modal entrance, toast slide-in).
27. [ ] Loading states match the defined treatments (skeletons or labeled spinners, never bare spinners).
28. [ ] Empty states include an icon, descriptive heading, and a suggested next action.

### Voice (3 items)

29. [ ] No user-facing text uses forbidden terms (AI, generate, model, prompt, LLM, etc.).
30. [ ] Error messages are specific and actionable.
31. [ ] Placeholder text is realistic and helpful.

### Visual Verification (5 items)

32. [ ] Page is visually distinguishable from Visualping, Distill.io, and a generic Tailwind template.
33. [ ] Brand is evident even with the logo hidden (dark navy base, cyan accents, Geist typography).
34. [ ] No clipping, overflow, or collapse at 375px and 1280px viewports.
35. [ ] Form inputs render at 16px or larger on iOS (no auto-zoom on focus).
36. [ ] Interface is usable on a 375x667 portrait viewport AND a 667x375 landscape viewport.

**Minimum passing score:** 30/36. All Typography, Color, Layout, and Visual Language items are mandatory.
