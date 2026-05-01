from datetime import date, datetime

import pytest

from api.tools.formatting import format_date, parse_date


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (datetime(2026, 5, 1, 12, 30), date(2026, 5, 1)),
        (date(2026, 5, 1), date(2026, 5, 1)),
        ("2026-05-01", date(2026, 5, 1)),
        ("2026-05-01T12:30:00", date(2026, 5, 1)),
        (None, None),
        ("", None),
        ("null", None),
        ("<null>", None),
    ],
)
def test_parse_date_accepts_common_api_values(value, expected):
    assert parse_date(value) == expected


def test_format_date_uses_default_display_format():
    assert format_date(datetime(2026, 5, 1, 12, 30)) == "01-05-2026"


def test_parse_date_rejects_unexpected_types():
    with pytest.raises(TypeError):
        parse_date(1)
