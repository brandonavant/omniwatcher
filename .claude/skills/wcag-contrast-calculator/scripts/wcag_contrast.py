#!/usr/bin/env python3
# noinspection SpellCheckingInspection
"""Calculate WCAG 2.2 contrast ratios between two hex colors.

Uses the IEC 61966-2-1 correct sRGB linearization threshold (0.04045),
not the historically published WCAG value of 0.03928.
"""

import sys


# WCAG AA and AAA thresholds
THRESHOLDS: dict[str, float] = {
    "AA Normal Text": 4.5,
    "AA Large Text": 3.0,
    "AAA Normal Text": 7.0,
    "AAA Large Text": 4.5,
}


def parse_hex(hex_color: str) -> tuple[int, int, int]:
    """Parse a hex color string into an (R, G, B) tuple.

    Args:
        hex_color: A hex color string, with or without a leading '#'.

    Returns:
        A tuple of (red, green, blue) integers in the range 0-255.

    Raises:
        ValueError: If the string is not a valid 6-digit hex color.
    """
    color = hex_color.lstrip("#")
    if len(color) != 6:
        raise ValueError(f"Invalid hex color: {hex_color!r} (expected 6 hex digits)")
    try:
        r = int(color[0:2], 16)
        g = int(color[2:4], 16)
        b = int(color[4:6], 16)
    except ValueError:
        raise ValueError(f"Invalid hex color: {hex_color!r} (non-hex characters)")
    return r, g, b

# noinspection SpellCheckingInspection
def linearize(channel: float) -> float:
    """Convert an sRGB channel value to linear RGB.

    Uses the IEC 61966-2-1 standard threshold of 0.04045.

    Args:
        channel: An sRGB channel value normalized to [0, 1].

    Returns:
        The linearized channel value.
    """
    if channel <= 0.04045:
        return channel / 12.92
    return ((channel + 0.055) / 1.055) ** 2.4


def relative_luminance(r: int, g: int, b: int) -> float:
    """Calculate relative luminance per WCAG 2.2.

    Args:
        r: Red channel (0-255).
        g: Green channel (0-255).
        b: Blue channel (0-255).

    Returns:
        The relative luminance value.
    """
    r_lin = linearize(r / 255)
    g_lin = linearize(g / 255)
    b_lin = linearize(b / 255)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def contrast_ratio(hex1: str, hex2: str) -> float:
    """Calculate the WCAG 2.2 contrast ratio between two hex colors.

    Args:
        hex1: First hex color (with or without '#').
        hex2: Second hex color (with or without '#').

    Returns:
        The unrounded contrast ratio, where the lighter color is always the numerator.
        Use format_ratio() to produce a display string.

    Raises:
        ValueError: If either color is not a valid 6-digit hex string.
    """
    r1, g1, b1 = parse_hex(hex1)
    r2, g2, b2 = parse_hex(hex2)
    lum1 = relative_luminance(r1, g1, b1)
    lum2 = relative_luminance(r2, g2, b2)
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


def format_ratio(ratio: float) -> str:
    """Format a contrast ratio for display with two decimal places.

    Args:
        ratio: The unrounded contrast ratio.

    Returns:
        A formatted string like "14.83:1".
    """
    return f"{ratio:.2f}:1"


def evaluate_thresholds(ratio: float) -> dict[str, bool]:
    """Evaluate a contrast ratio against all WCAG AA and AAA thresholds.

    Args:
        ratio: The contrast ratio to evaluate.

    Returns:
        A dict mapping threshold names to pass/fail booleans.
    """
    return {name: ratio >= threshold for name, threshold in THRESHOLDS.items()}


def main() -> None:
    """Run the contrast ratio calculator from the command line.

    Expects two hex color arguments. Prints the contrast ratio and
    pass/fail results for each WCAG threshold.
    """
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <hex1> <hex2>", file=sys.stderr)
        print(f"Example: {sys.argv[0]} #E2E8F0 #080C14", file=sys.stderr)
        sys.exit(1)

    hex1 = sys.argv[1]
    hex2 = sys.argv[2]

    try:
        ratio = contrast_ratio(hex1, hex2)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    results = evaluate_thresholds(ratio)

    print(f"Contrast ratio: {format_ratio(ratio)}")
    print()
    for name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        threshold = THRESHOLDS[name]
        print(f"  {name} ({threshold}:1): {status}")


if __name__ == "__main__":
    main()
