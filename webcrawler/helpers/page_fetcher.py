import logging
import requests


def fetch_page_content(url):
    """
    Request the url page content.
    :param url: url to request
    :return: raw HTML as a string or None if unsuccessful
    """
    try:
        res = requests.get(url, timeout=10)
        return res.text
    except requests.RequestException as e:
        # if we fail to fetch a page log an error, but continue crawling
        logging.error(f'Failed to fetch {url}, {e}')
        return None