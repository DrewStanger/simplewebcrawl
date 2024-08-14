import pytest
from unittest.mock import patch, MagicMock
from collections import deque

from webcrawler.crawler import WebCrawler


@pytest.fixture
def crawler():
    return WebCrawler("https://example.com", 2, 5)


def test_crawler_initialization(crawler):
    assert crawler.domain == "https://example.com"
    assert crawler.max_depth == 2
    assert len(crawler.visited) == 0
    assert len(crawler.url_graph) == 0
    assert crawler.executor._max_workers == 5


@patch('webcrawler.crawler.fetch_page_content')
@patch('webcrawler.crawler.find_links')
def test_process_page(mock_find_links, mock_fetch_page_content, crawler):
    mock_fetch_page_content.return_value = "<html>content</html>"
    mock_find_links.return_value = ["https://example.com/page1", "https://example.com/page2"]

    result = crawler.process_page("https://example.com", 0)

    assert result == [("https://example.com/page1", 1), ("https://example.com/page2", 1)]
    assert "https://example.com" in crawler.visited
    assert "https://example.com" in crawler.url_graph
    assert crawler.url_graph["https://example.com"] == ["https://example.com/page1", "https://example.com/page2"]


def test_process_page_already_visited(crawler):
    crawler.visited.add("https://example.com")
    result = crawler.process_page("https://example.com", 0)
    assert result == []


@patch('webcrawler.crawler.fetch_page_content')
def test_process_page_no_content(mock_fetch_page_content, crawler):
    mock_fetch_page_content.return_value = None
    result = crawler.process_page("https://example.com", 0)
    assert result == []


@patch('builtins.open', new_callable=MagicMock)
@patch('json.dump')
def test_write_output(mock_json_dump, mock_open, crawler):
    crawler.url_graph = {"https://example.com": ["https://example.com/page1"]}
    crawler.write_output()
    mock_open.assert_called_once_with('output/url_graph.json', 'w')
    mock_json_dump.assert_called_once()


@patch.object(WebCrawler, 'process_page')
@patch.object(WebCrawler, 'write_output')
def test_crawl(mock_write_output, mock_process_page, crawler):
    mock_process_page.side_effect = [
        [("https://example.com/page1", 1)],
        [("https://example.com/page2", 2)],
        []
    ]

    crawler.crawl()

    assert mock_process_page.call_count == 3
    mock_write_output.assert_called_once()


if __name__ == "__main__":
    pytest.main()