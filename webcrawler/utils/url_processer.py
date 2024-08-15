from urllib.parse import urljoin, urlparse, urlunparse


def format_url(domain, url):
    """
    Formats a given url into an absolute url and normalises it,
    i.e. treat http://example.com, http://example.com/ and https://example.com/ as the same url
    This means we can handle /relative-link but drops uris like #main that we do not want to crawl
    :param domain:
    :param url:
    :return: normalised url or None for invalid urls
    """
    parsed_url = urlparse(url)
    if url.startswith('/'):
        full_url = urljoin(domain, url)
    elif parsed_url.scheme in ['http', 'https']:
        full_url = url
    else:
        return None

    parsed = urlparse(full_url)
    path = parsed.path.rstrip('/')
    normalised = urlunparse(('https', parsed.netloc.lower(), path, '', '', ''))
    return normalised


def is_within_domain(domain, url):
    """
    Return True if the url belongs to the provided domain.

    :param domain: The base domain to check against.
    :param url: The URL to check.
    :return: Boolean, True if the URL belongs to the same domain, False otherwise.
    """
    parsed_domain = urlparse(domain)
    parsed_url = urlparse(url)

    return parsed_url.netloc == parsed_domain.netloc
