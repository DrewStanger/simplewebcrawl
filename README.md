# WebCrawler 

This is a multi-threaded web crawler implemented in Python. The python works iteratively from a provided starting domain 
and will explore all URLs contained in that domain to a specified depth.

The results from a crawl are stored as a JSON file mapping visited URLs to a list of URLs found within that page.

## How to Install 

Install dependencies 

```
pip3 install -r requirements.txt
```

## How to use


You can run the web crawler from root of the project by doing the following

```
python -m webcrawler.crawler --domain <domain_url> --max_depth <depth> --conc <number_of_concurrent_requests>
```
For example, to run the web crawler against monzo.com, run the following.
```
python -m webcrawler.crawler --domain http://monzo.com --max_depth 1 --conc 10
``` 
Replace <domain_url>, <depth>, and <number_of_concurrent_requests> with the appropriate values:

    --domain: The domain to start crawling from (e.g., http://monzo.com).
    --max_depth: The maximum depth to crawl from the starting URL (default is 1).
    --conc: The maximum number of concurrent requests (default is 10).

### Output

After the crawler has completed it run you will find the file `url_graph.json` in the `output/` folder. The resulting 
output is a map which links the visited URL to a list of the URLs contained on the page, and should look something like this
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

There unit tests for each function provided as a part of the web crawler, these can be run from the root of the project
using pytest by running the following command

```
pytest tests/
``` 

## Trade-offs and Potential Improvements

There were a number of decisions made when putting together this project, all of which have been made to provide a suitable
solution for the required use case. 

### Use of BFS

The use of BFS for the webcrawler means that it searches all webpages at the current depth before moving onto the next 
depth. Within the crawler I add each discovered link into the queue and determine if we need to visit it, or if it's already been 
visited before crawling it to obtain more links.

This approach fulfils the requirement of discovering all links that exist on a certain URL before progressing deeper into the site.
 

### Concurrency

`ThreadPoolExecutor` is used to concurrently process pages in order to fetch and then find all links on a page.
This enables the crawling tasks to be ran in parallel and depending on the number of concurrent workers can greatly 
reduce the crawling time.

### Testing

Unit testing has been completed, an improvement that could be made to the overall testing of this web crawler is 
integration testing. In order to implement this and simulate the real world application of the web crawler a local
web server could be launched for testing purposes which contains various html pages which would provide a consistent 
testing platform.

This could also enable performance and load testing.


### Output

The output is written to JSON as a map between URLs visited and a list of the URLs discovered at that domain.
This may become a bottleneck for very large websites, or very deep crawls as all this data is stored in memory and then
written to the output file. A potential improvement here is continuously writing to the file, or instead writing to a
database as the crawl progresses. 

