import pytest
from webcrawler.helpers.link_extractor import find_links

def test_find_links():
    html_content = """
    <html>
        <body>
            <a href="https://example.com/test1">Link 1</a>
            <a href="/page2">Link 2</a>
            <img src="https://example.com/testimage.jpg">
        </body>
    </html>
    """
    links = find_links(html_content)
    assert set(links) == {"https://example.com/test1", "/page2", "https://example.com/testimage.jpg"}

def test_find_links_no_content():
    html_content = "<html></html>"
    links = find_links(html_content)
    assert links == [], "Expected an empty list when no links are present"