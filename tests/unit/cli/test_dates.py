import pytest
import typer

from loyverse_sdk.cli._dates import normalize_date


class TestNormalizeDate:
    def test_iso8601_passthrough(self):
        assert normalize_date("2024-01-15T12:30:00Z") == "2024-01-15T12:30:00Z"

    def test_bare_date_midnight(self):
        result = normalize_date("2024-06-15")
        assert result.startswith("2024-06-15T00:00:00")

    def test_bare_date_end_of_day(self):
        result = normalize_date("2024-06-15", end_of_day=True)
        assert result.startswith("2024-06-15T23:59:59")

    def test_yesterday_produces_utc(self):
        result = normalize_date("yesterday")
        assert result.endswith("Z")
        assert "T00:00:00" in result

    def test_today_produces_utc(self):
        result = normalize_date("today")
        assert result.endswith("Z")
        assert "T00:00:00" in result

    def test_invalid_date_raises_bad_parameter(self):
        with pytest.raises(typer.BadParameter, match="Invalid date"):
            normalize_date("not-a-date")

    def test_yesterday_end_of_day(self):
        result = normalize_date("yesterday", end_of_day=True)
        assert "T23:59:59" in result

    def test_strips_whitespace(self):
        result = normalize_date("  2024-06-15  ")
        assert result.startswith("2024-06-15T00:00:00")
