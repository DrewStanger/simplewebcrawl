import argparse


def parse_args():
    """
    Parses command-line arguments for the web crawler.
    """
    parser = argparse.ArgumentParser(description="Web Crawler!")
    parser.add_argument("--domain", help="The domain to start crawling from")
    parser.add_argument("--max_depth", type=int, default=1, help="Max depth to crawl")
    parser.add_argument("--conc", type=int, default=10, help="Max number of concurrent requests")
    return parser.parse_args()
