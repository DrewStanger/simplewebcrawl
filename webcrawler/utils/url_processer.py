

from urllib.parse import urljoin, urlparse


def format_url(url):
    """
    Formats a given url into an absolute url
    This means we can handle /relative-link but drops uris like #main
    :param url:
    :return: formatted url or None for invalid urls
    """
    parsed_url = urlparse(url)
    if url.startswith('/'):
        return urljoin(domain, url)
    elif parsed_url.scheme in ['http', 'https']:
        return url
    return None

def is_within_domain(url):
    """
    Return True if the url belongs to the provided domain
    :param url:
    :return: Boolean, True if belongs to same domain, False otherwise
    """
    return url.startswith(domain)
