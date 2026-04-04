---
name: wcag-contrast-calculator
description: Calculate WCAG 2.2 contrast ratios between two hex colors and check AA/AAA compliance. Use when verifying color contrast, checking accessibility, or auditing brand colors.
argument-hint: <hex1> <hex2>
allowed-tools: Bash(python3 *)
---

# WCAG Contrast Ratio Calculator

Calculate the exact WCAG 2.2 contrast ratio between two hex colors and check pass/fail against all AA and AAA
thresholds.

## Usage

Run the calculator with two hex color arguments:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/wcag_contrast.py $ARGUMENTS
```

## Output

The script prints:

- The contrast ratio rounded to two decimal places (e.g., `14.83:1`)
- Pass/fail for each WCAG threshold:
    - **AA Normal Text** (4.5:1)
    - **AA Large Text** (3.0:1)
    - **AAA Normal Text** (7.0:1)
    - **AAA Large Text** (4.5:1)

## Implementation details

- Uses the IEC 61966-2-1 correct `sRGB` linearization threshold (0.04045), not the historically
  published WCAG value of 0.03928.
- No external dependencies — standard library only.

## Running tests

```bash
cd ${CLAUDE_SKILL_DIR}/scripts && python3 -m pytest test_wcag_contrast.py -v
```
