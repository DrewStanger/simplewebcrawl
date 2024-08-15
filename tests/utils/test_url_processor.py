import pytest

from webcrawler.utils.url_processer import format_url, is_within_domain


@pytest.mark.parametrize("domain,url,expected", [
    ("https://example.com", "/relative", "https://example.com/relative"),
    ("https://example.com", "https://example.com/absolute", "https://example.com/absolute"),
    ("https://example.com", "https://other.com", "https://other.com"),
    ("https://example.com", "javascript:void(0)", None),
    ("https://example.com", "#", None),
    ("http://example.com", "/relative", "https://example.com/relative"),
    ("http://example.com", "https://example.com/absolute", "https://example.com/absolute"),
])
def test_format_url(domain, url, expected):
    assert format_url(domain, url) == expected


@pytest.mark.parametrize("domain,url,expected", [
    ("https://example.com", "https://example.com/page", True),
    ("https://example.com", "https://example.com/page/subpage", True),
    ("https://example.com", "https://other.com", False),
    ("https://example.com", "https://sub.example.com", False),
    ("http://example.com", "http://example.com/page", True),
    ("http://example.com", "https://example.com/page", True),
])
def test_is_within_domain(domain, url, expected):
    assert is_within_domain(domain, url) == expected
