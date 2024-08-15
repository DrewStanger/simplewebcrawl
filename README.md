# WebCrawler 

This is a multi-threaded web crawler implemented in Python. It uses a Breadth-First Search (BFS) approach, starting 
from a provided domain, to explore all URLs within that domain up to a specified depth.

The results from a crawl are stored as a JSON file, mapping each visited URL to a list of URLs found on that page.

## Installation

Install the necessary dependencies using pip:

```
pip3 install -r requirements.txt
```

## Usage

You can run the web crawler from the root of the project with the following command:

```
python -m webcrawler.crawler --domain <domain_url> --max_depth <depth> --conc <number_of_concurrent_requests>
```
For example, to crawl monzo.com with a maximum depth of 1 and 10 concurrent requests, run:
```
python -m webcrawler.crawler --domain http://monzo.com --max_depth 1 --conc 10
``` 
Replace <domain_url>, <depth>, and <number_of_concurrent_requests> with the appropriate values:

    --domain: The domain to start crawling from (e.g., http://monzo.com).
    --max_depth: The maximum depth to crawl from the starting URL (default is 1).
    --conc: The maximum number of concurrent requests (default is 10).

### Output

After the crawler has completed it run you will find the file `url_graph.json` in the `output/` folder. The resulting 
output is a map which links the visited URL to a list of the URLs contained on the page, 
and should look something like this
```
{
    "https://example.com": [
        "https://example.com/about",
        "https://example.com/contact"
    ],
    "https://example.com/about": [
        "https://example.com/team",
        "https://example.com/careers"
    ]
}
```
## Testing

Unit tests are provided for each function in the web crawler. 
You can run these tests from the root of the project using pytest:

```
pytest tests/
``` 

## Trade-offs and Potential Improvements

Several design decisions were made to meet the required use case effectively. 
Below are some trade-offs and areas for potential improvement:

### Use of BFS

The BFS approach ensures that the crawler searches all webpages at the current depth before moving on to the next. 
Links discovered are added to a queue, and the crawler checks if a link has already been visited before exploring it further.

This approach is beneficial for discovering all links at a particular depth before diving deeper into the site.
 

### Concurrency

The `ThreadPoolExecutor` is used to process pages concurrently, fetching and discovering links in parallel. 
Depending on the number of concurrent workers, this can significantly reduce the crawl time.

### Testing

Unit testing has been completed, an improvement that could be made to the overall testing of this web crawler is 
integration testing. In order to implement this and simulate the real world application of the web crawler a local
web server could be launched for testing purposes which contains various html pages which would provide a consistent 
testing platform.

This could also enable performance and load testing.


### Output

The output is written to JSON, mapping visited URLs to the list of discovered URLs. For very large websites or deep 
crawls, this could become a bottleneck as the data is stored in memory before being written to the file. A potential 
improvement could be to write to the file continuously or to use a database to store results as the crawl progresses.

