"""Tests for the WCAG contrast ratio calculator."""

import pytest

from wcag_contrast import contrast_ratio, evaluate_thresholds, format_ratio, parse_hex


class TestParseHex:
    """Hex parsing edge cases."""

    def test_uppercase_with_hash(self) -> None:
        assert parse_hex("#FF8800") == (255, 136, 0)

    def test_lowercase_with_hash(self) -> None:
        assert parse_hex("#ff8800") == (255, 136, 0)

    def test_uppercase_without_hash(self) -> None:
        assert parse_hex("FF8800") == (255, 136, 0)

    def test_lowercase_without_hash(self) -> None:
        assert parse_hex("ff8800") == (255, 136, 0)

    def test_mixed_case(self) -> None:
        assert parse_hex("#aAbBcC") == (170, 187, 204)

    def test_invalid_length_raises(self) -> None:
        with pytest.raises(ValueError, match="expected 6 hex digits"):
            parse_hex("#FFF")

    def test_invalid_characters_raises(self) -> None:
        with pytest.raises(ValueError, match="non-hex characters"):
            parse_hex("#ZZZZZZ")


class TestKnownReferencePairs:
    """Known WCAG reference pairs with exact expected values."""

    def test_black_on_white(self) -> None:
        assert contrast_ratio("#000000", "#FFFFFF") == 21.0

    def test_white_on_black(self) -> None:
        """Order should not matter — lighter is always the numerator."""
        assert contrast_ratio("#FFFFFF", "#000000") == 21.0

    def test_identical_colors(self) -> None:
        assert contrast_ratio("#000000", "#000000") == 1.0

    def test_identical_white(self) -> None:
        assert contrast_ratio("#FFFFFF", "#FFFFFF") == 1.0

    def test_identical_arbitrary(self) -> None:
        assert contrast_ratio("#3A7BDE", "#3A7BDE") == 1.0


class TestRegressionCases:
    """Regression cases from brand-identity.md Section 3.2.

    The document claimed incorrect ratios for these pairings.
    These tests assert the actual calculated values rounded to two
    decimal places (the display precision).
    """

    def test_text_primary_on_bg_elevated(self) -> None:
        """--text-primary (#E2E8F0) on --bg-elevated (#0F1520).

        Document claimed 15.0:1, actual is 14.83:1.
        """
        ratio = contrast_ratio("#E2E8F0", "#0F1520")
        assert round(ratio, 2) == 14.83

    def test_accent_on_bg_elevated(self) -> None:
        """--accent (#22D3EE) on --bg-elevated (#0F1520).

        Document claimed 10.3:1, actual is 10.12:1.
        """
        ratio = contrast_ratio("#22D3EE", "#0F1520")
        assert round(ratio, 2) == 10.12

    def test_white_on_cyan(self) -> None:
        """White (#FFFFFF) on cyan (#22D3EE).

        Document claimed 1.5:1, actual is 1.81:1.
        """
        ratio = contrast_ratio("#FFFFFF", "#22D3EE")
        assert round(ratio, 2) == 1.81


class TestBoundaryValues:
    """Pairs that land just above and below each WCAG threshold.

    Verifies that pass/fail flips correctly at each boundary using
    the unrounded contrast ratio.
    """

    # --- 3.0:1 threshold (AA Large Text) ---

    def test_just_below_3_to_1(self) -> None:
        """#595959 on black = ~2.998:1 — should fail AA Large Text."""
        ratio = contrast_ratio("#595959", "#000000")
        results = evaluate_thresholds(ratio)
        assert results["AA Large Text"] is False

    def test_just_above_3_to_1(self) -> None:
        """#5A5A5A on black = ~3.045:1 — should pass AA Large Text."""
        ratio = contrast_ratio("#5A5A5A", "#000000")
        results = evaluate_thresholds(ratio)
        assert results["AA Large Text"] is True

    # --- 4.5:1 threshold (AA Normal Text / AAA Large Text) ---

    def test_just_below_4_5_to_1(self) -> None:
        """#747474 on black = ~4.493:1 — should fail AA Normal Text."""
        ratio = contrast_ratio("#747474", "#000000")
        results = evaluate_thresholds(ratio)
        assert results["AA Normal Text"] is False
        assert results["AAA Large Text"] is False

    def test_just_above_4_5_to_1(self) -> None:
        """#757575 on black = ~4.558:1 — should pass AA Normal Text."""
        ratio = contrast_ratio("#757575", "#000000")
        results = evaluate_thresholds(ratio)
        assert results["AA Normal Text"] is True
        assert results["AAA Large Text"] is True

    # --- 7.0:1 threshold (AAA Normal Text) ---

    def test_just_below_7_to_1(self) -> None:
        """#949494 on black = ~6.923:1 — should fail AAA Normal Text."""
        ratio = contrast_ratio("#949494", "#000000")
        results = evaluate_thresholds(ratio)
        assert results["AAA Normal Text"] is False

    def test_just_above_7_to_1(self) -> None:
        """#959595 on black = ~7.011:1 — should pass AAA Normal Text."""
        ratio = contrast_ratio("#959595", "#000000")
        results = evaluate_thresholds(ratio)
        assert results["AAA Normal Text"] is True


class TestFormatRatio:
    """Verify display formatting uses two decimal places."""

    def test_whole_number(self) -> None:
        assert format_ratio(21.0) == "21.00:1"

    def test_one(self) -> None:
        assert format_ratio(1.0) == "1.00:1"

    def test_two_decimal_rounding(self) -> None:
        assert format_ratio(14.832929) == "14.83:1"

    def test_rounds_up(self) -> None:
        assert format_ratio(4.556) == "4.56:1"

    def test_rounds_down(self) -> None:
        assert format_ratio(2.9517) == "2.95:1"
