import pytest

from extended_bs4 import ExtendedBeautifulSoup, StrictBeautifulSoupFaiure

PARSED_HTML = ExtendedBeautifulSoup('<h1 value="123">Test</h1><h2>Test</h2><h2>Test</h2>')


# Test by converting the ExtendedPath to a Path because testing against ExtendedPath directly may hide bugs
class TestStrictSelect:
    def test_strict_select(self):
        assert str(PARSED_HTML.strict_select("h2")) == "[<h2>Test</h2>, <h2>Test</h2>]"

    def test_strict_select_failure(self):
        with pytest.raises(StrictBeautifulSoupFaiure):
            PARSED_HTML.strict_select_one("h3")


class TestStrictSelectOne:
    def test_success(self):
        assert str(PARSED_HTML.strict_select_one("h1")) == '<h1 value="123">Test</h1>'

    def test_failure_no_values(self):
        with pytest.raises(StrictBeautifulSoupFaiure):
            PARSED_HTML.strict_select_one("h3")

    def test_failure_too_many_values(self):
        with pytest.raises(StrictBeautifulSoupFaiure):
            PARSED_HTML.strict_select_one("h2")


class TestStrictGet:
    def test_success(self):
        assert str(PARSED_HTML.strict_select_one("h1").strict_get("value")) == "123"

    def test_failure(self):
        with pytest.raises(StrictBeautifulSoupFaiure):
            PARSED_HTML.strict_select_one("h1").strict_get("missing_value")
