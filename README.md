### WebCrawler 

This is a multi-threaded web crawler implemented in Python. The python works iteratively from a provided starting domain 
and will explore all URLs contained in that domain to a specified depth.

The results from a crawl are stored as a JSON file mapping visited URLs to a list of URLs found within that page.

### How to Install 

### How to use

You can run the web crawler with the following command

```
python webcrawler.py --domain <domain_url> --max_depth <depth> --conc <number_of_concurrent_requests>
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