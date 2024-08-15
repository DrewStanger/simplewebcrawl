from collections import deque
import json
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

from webcrawler.helpers.link_extractor import find_links
from webcrawler.helpers.page_fetcher import fetch_page_content
from webcrawler.utils.parse_args import parse_args
from webcrawler.utils.url_processer import format_url, is_within_domain

script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, '', 'output')
url_graph_path = os.path.join(output_dir, 'url_graph.json')


class WebCrawler:
    """
    WebCrawler crawls a given domain to a specified depth
    It returns a map of all visited urls and the urls contained on that domain
    """

    def __init__(self, domain, max_depth, max_workers=10):
        """
        Initialize the WebCrawler with a subdomain and maximum crawl depth.

        :param domain: The starting domain URL i.e. http://google.com.
        :param max_depth: The maximum depth to crawl from the starting URL.
        :param max_workers: Number of concurrent workers that ThreadPoolExecutor will use.
        """
        self.domain = domain
        self.visited = set()
        self.max_depth = max_depth
        self.url_graph = {}
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def process_page(self, current_url, depth):
        """
        Processes a given url and returns a list of urls found on the page
        :param current_url: the url from the front of the queue for processing
        :param depth: the current depth from the starting url
        :return: next_urls, [] or List of urls found and the current depth.
        """
        normalised_url = format_url(self.domain, current_url)

        if normalised_url in self.visited:
            return []

        self.url_graph[normalised_url] = []

        page_content = fetch_page_content(normalised_url)
        self.visited.add(normalised_url)
        if not page_content:
            return []

        next_urls = []
        print(f'crawling: {normalised_url}')
        found_urls = find_links(page_content)

        for link in found_urls:
            formatted_url = format_url(self.domain, link)
            if formatted_url:
                if formatted_url not in self.url_graph[normalised_url]:
                    self.url_graph[normalised_url].append(formatted_url)
                if formatted_url not in self.visited and is_within_domain(self.domain, formatted_url):
                    next_urls.append((formatted_url, depth + 1))

        return next_urls

    def write_output(self):
        """
        Writes the url_graph data to a JSON file for readability.
        """
        with open(url_graph_path, 'w') as f:
            json.dump(self.url_graph, f, indent=4)
        print('crawl complete!')
        print('output written to webcrawler/output/')

    def crawl(self):
        """
        Crawls the domain from the starting URL up to `self.max_depth`.
        Processes pages concurrently, following links until no further items remain in the queue.
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


if __name__ == '__main__':
    args = parse_args()
    crawler = WebCrawler(args.domain, args.max_depth, args.conc)
    crawler.crawl()
