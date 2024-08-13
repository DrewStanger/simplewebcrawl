import os

from bs4 import BeautifulSoup
from collections import deque
import requests
import logging
from urllib.parse import urlparse, urljoin
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import json


class WebCrawler:
    """
    WebCrawler crawls a given domain to a specified depth
    It returns a map of all visited urls and the urls contained on that domain
    """
    def __init__(self, domain, max_depth, max_workers=10):
        """
        Initialize the WebCrawler with a subdomain and maximum crawl depth.

        :param domain: The starting subdomain URL.
        :param max_depth: The maximum depth to crawl from the starting URL.
        """
        self.domain = domain
        self.visited = set()
        self.max_depth = max_depth
        self.url_graph = {}
        self.executor = ThreadPoolExecutor(max_workers=max_workers)  # ThreadPoolExecutor

    def fetch_page_content(self, url):
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

    def find_links(self, page_content):
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

    def format_url(self, url):
        """
        Formats a given url into an absolute url
        This means we can handle /relative-link but drops uris like #main
        :param url:
        :return: formatted url or None for invalid urls
        """
        parsed_url = urlparse(url)
        if url.startswith('/'):
            return urljoin(self.domain, url)
        elif parsed_url.scheme in ['http', 'https']:
            return url
        return None

    def is_within_domain(self, url):
        """
        Return True if the url belongs to the provided domain
        :param url:
        :return: Boolean, True if belongs to same domain, False otherwise
        """
        return url.startswith(self.domain)

    def process_page(self, current_url, depth):
        """
        Processes a specific url and returns a list which contains the urls found on the page
        :param current_url: the url from the front of the queue for processing
        :param depth: the current depth from the starting url
        :return: next_urls, either an empty list if there are no urls or a list of urls and the current depth
        """
        if current_url in self.visited:
            return []

        self.visited.add(current_url)
        self.url_graph[current_url] = []

        page_content = self.fetch_page_content(current_url)
        if not page_content:
            return []

        next_urls = []
        found_urls = self.find_links(page_content)

        for link in found_urls:
            formatted_url = self.format_url(link)
            if formatted_url and self.is_within_domain(formatted_url):
                if formatted_url not in self.url_graph[current_url]:
                    self.url_graph[current_url].append(formatted_url)
                if formatted_url not in self.visited:
                    next_urls.append((formatted_url, depth + 1))

        return next_urls

    def write_output(self):
        with open(os.path.join('output/', 'url_graph.json'), 'w') as f:
            json.dump(self.url_graph, f, indent=4)  # Write the graph to a JSON file with indentation for readability

        print('output written to webcrawler/output/')

    def crawl(self):
        """
        Crawls the domain starting from the initial domain, exploring up to a specified depth.

        The method uses a breadth-first search (BFS) approach to traverse web pages. It starts
        with the user provided URL and explores linked pages on the same domain up to a maximum depth defined
        by `self.max_depth`.
        It iterates until the queue is empty and there are no further pages to explore
        """
        url_queue = deque([(self.domain, 0)])
        future_to_url = {}
        print('starting...')

        while url_queue or future_to_url:
            while url_queue:
                current_url, current_depth = url_queue.popleft()
                if current_depth > self.max_depth:
                    break

                if current_url in self.visited:
                    continue

                # Submit the task to the executor
                future = self.executor.submit(self.process_page, current_url, current_depth)
                future_to_url[future] = current_url

            # Iterate over the completed futures
            for future in as_completed(future_to_url):
                current_url = future_to_url.pop(future)
                try:
                    next_urls = future.result()
                    url_queue.extend(next_urls)
                except Exception as exc:
                    logging.error(f'{current_url} generated an exception: {exc}')

        self.executor.shutdown(wait=True)
        # Write the URL graph to a JSON file in the output/ folder
        self.write_output()



def parse_args():
    parser = argparse.ArgumentParser(description="Web Crawler!")
    parser.add_argument("--domain", help="The domain to start crawling from")
    parser.add_argument("--max_depth", type=int, default=1, help="Max depth to crawl")
    parser.add_argument("--conc", type=int, default=10, help="Max number of concurrent requests")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    crawler = WebCrawler(args.domain, args.max_depth, args.conc)
    crawler.crawl()
