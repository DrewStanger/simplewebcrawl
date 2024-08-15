import logging
import requests
from requests import Timeout


def fetch_page_content(url):
    """
    Request the url page content.
    :param url: url to request
    :return: raw HTML as a string or None if unsuccessful
    """
    try:
        res = requests.get(url, timeout=10)
        return res.text
    except Timeout:
        logging.warning(f"Timeout occurred while fetching {url}, skipping.")
    except requests.RequestException as e:
        logging.error(f"Failed to fetch {url}: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error when fetching {url}: {str(e)}")
        return None
