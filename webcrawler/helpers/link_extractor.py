from bs4 import BeautifulSoup


def find_links(page_content):
    """
    Looks at each tag which can contain a url, finds all URLs and returns these as a list
    :param page_content: string of raw HTML page content
    :return: list of all found urls from the content
    """
    soup = BeautifulSoup(page_content, 'html.parser')
    links = []
    for tag in ['a', 'link', 'script', 'img']:
        links.extend([elem.get('href') or elem.get('src') for elem in soup.find_all(tag) if
                        elem.get('href') or elem.get('src')])
    return links
