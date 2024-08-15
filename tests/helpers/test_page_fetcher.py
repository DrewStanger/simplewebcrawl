import pytest
import requests
from requests.exceptions import Timeout, RequestException
from unittest.mock import patch
from webcrawler.helpers.page_fetcher import fetch_page_content

@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get

def test_successful_fetch(mock_requests_get):
    mock_requests_get.return_value.text = "<html>Test content</html>"
    result = fetch_page_content("http://example.com")
    assert result == "<html>Test content</html>"
    mock_requests_get.assert_called_once_with("http://example.com", timeout=10)

def test_timeout(mock_requests_get, caplog):
    mock_requests_get.side_effect = Timeout("Connection timed out")
    result = fetch_page_content("http://example.com")
    assert result is None
    assert "Timeout occurred while fetching http://example.com, skipping." in caplog.text

def test_request_exception(mock_requests_get, caplog):
    mock_requests_get.side_effect = RequestException("404 Not Found")
    result = fetch_page_content("http://example.com")
    assert result is None
    assert "Failed to fetch http://example.com: 404 Not Found" in caplog.text

def test_unexpected_exception(mock_requests_get, caplog):
    mock_requests_get.side_effect = ValueError("Unexpected error")
    result = fetch_page_content("http://example.com")
    assert result is None
    assert "Unexpected error when fetching http://example.com: Unexpected error" in caplog.text