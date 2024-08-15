import pytest
from unittest.mock import patch, Mock
from requests.exceptions import Timeout

from webcrawler.helpers.page_fetcher import fetch_page_content


@patch('requests.get')
def test_fetch_page_content_timeout(mock_get):
    mock_get.side_effect = Timeout("Request timed out")
    content = fetch_page_content("https://example.com")
    assert content is None


@patch('requests.get')
def test_fetch_page_content_retry_exhaustion(mock_get):
    mock_get.side_effect = Timeout("Request timed out")
    content = fetch_page_content("https://example.com")
    assert content is None
    assert mock_get.call_count == 1


@patch('requests.get')
@patch('logging.warning')
def test_fetch_page_content_timeout_logging(mock_logging, mock_get):
    mock_get.side_effect = Timeout("Request timed out")
    fetch_page_content("https://example.com")
    mock_logging.assert_called_with("Timeout occurred while fetching https://example.com, skipping.")
