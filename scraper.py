import sys                          
import requests
from bs4 import BeautifulSoup

# python scraper.py <URL>
# Example: python scraper.py univ.sitare.org
# sys.argv[0] = script name, sys.argv[1] = URL provided by user
if len(sys.argv) != 2:
    print("Usage: scraper.py <URL>") 
    sys.exit(1)
site_url = sys.argv[1]
print("URL entered:", site_url)
if site_url.startswith("http") is False:
    site_url = "https://" + site_url

# Send an HTTP GET request to the provided URL and check if the page loaded successfully
page_response = requests.get(site_url)
if page_response.status_code == 200:
    print("Page fetched successfully")
else:
    print(f"FAILED SUCCESSFULLY Status code: {page_response.status_code}")
    sys.exit(1)


# Creates the parsetree that's structured DOM out of the raw html
Body_text = page_response.text        
parse_tree = BeautifulSoup(Body_text, "html.parser")

# Extract the page title if it exists
if parse_tree.title:
    Title = parse_tree.title.string
else:
    Title = "Page doesn't have any TITLE"
print("Page Title:\n", Title)


# It extracts all the text from the html page while removing tags.
if parse_tree.body:
    page_body = parse_tree.body.get_text(separator=" ", strip = True)
else:
    page_body = "PAGE DOESN't HAVE BODY"
print("Page_body:\n" + page_body + "\n")


# It scrapes all the links which are in anchor tag.
Outlinks  = []
for hyperlink in parse_tree.find_all("a"):
    link_url = hyperlink.get("href")                    
    if link_url:                                        
        Outlinks.append(link_url)
print("All URLs found are")
for url in Outlinks:
    print(url)
