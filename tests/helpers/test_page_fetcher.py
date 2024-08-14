from unittest.mock import patch

import requests

from webcrawler.helpers.page_fetcher import fetch_page_content


@patch('requests.get')
def test_fetch_page_content_success(mock_get):
    mock_get.return_value.text = "<html><body>This is test content!</body></html>"
    content = fetch_page_content("https://example.com")
    assert content == "<html><body>This is test content!</body></html>"


@patch('requests.get')
def test_fetch_page_content_failure(mock_get):
    mock_get.side_effect = requests.RequestException("Test error")
    content = fetch_page_content("https://example.com")
    assert content is None