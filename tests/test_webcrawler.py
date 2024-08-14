import pytest
from unittest.mock import Mock, patch

import requests
from bs4 import BeautifulSoup

from webcrawler.webcrawler import WebCrawler, parse_args


@pytest.fixture
def crawler():
    return WebCrawler("https://example.com", 3)


def test_init(crawler):
    assert crawler.domain == "https://example.com"
    assert crawler.max_depth == 3
    assert isinstance(crawler.visited, set)
    assert isinstance(crawler.url_graph, dict)


@patch('requests.get')
def test_fetch_page_content_success(mock_get, crawler):
    mock_get.return_value.text = "<html><body>This is test content!</body></html>"
    content = crawler.fetch_page_content("https://example.com")
    assert content == "<html><body>This is test content!</body></html>"


@patch('requests.get')
def test_fetch_page_content_failure(mock_get, crawler):
    mock_get.side_effect = requests.RequestException("Test error")
    content = crawler.fetch_page_content("https://example.com")
    assert content is None


def test_find_links(crawler):
    html_content = """
    <html>
        <body>
            <a href="https://example.com/test1">Link 1</a>
            <a href="/page2">Link 2</a>
            <img src="https://example.com/testimage.jpg">
        </body>
    </html>
    """
    links = crawler.find_links(html_content)
    assert set(links) == {"https://example.com/test1", "/page2", "https://example.com/testimage.jpg"}


@pytest.mark.parametrize("url,expected", [
    ("/relative", "https://example.com/relative"),
    ("https://example.com/absolute", "https://example.com/absolute"),
    ("https://other.com", "https://other.com"),
    ("javascript:void(0)", None),
    ("#", None)
])
def test_format_url(crawler, url, expected):
    assert crawler.format_url(url) == expected


@pytest.mark.parametrize("url,expected", [
    ("https://example.com/page", True),
    ("https://example.com/page/subpage", True),
    ("https://other.com", False),
    ("https://sub.example.com", False),
])
def test_is_within_domain(crawler, url, expected):
    assert crawler.is_within_domain(url) == expected

@patch.object(WebCrawler, 'fetch_page_content')
@patch.object(WebCrawler, 'find_links')
def test_process_page(mock_find_links, mock_fetch_content, crawler):
    mock_fetch_content.return_value = ("<html><body>This is test content! Look at <a href='https://example.com/page1'> "
                                       "and <a href='https://example.com/page2'></body></html>")
    mock_find_links.return_value = ["https://example.com/page1", "https://example.com/page2"]

    result = crawler.process_page("https://example.com", 0)

    assert "https://example.com" in crawler.visited
    assert crawler.url_graph["https://example.com"] == ["https://example.com/page1", "https://example.com/page2"]
    assert result == [("https://example.com/page1", 1), ("https://example.com/page2", 1)]

def test_parse_args():
    with patch('sys.argv', ['script.py', '--domain', 'https://test.com', '--max_depth', '5', '--conc', '20']):
        args = parse_args()
        assert args.domain == 'https://test.com'
        assert args.max_depth == 5
        assert args.conc == 20

