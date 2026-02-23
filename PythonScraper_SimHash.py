import sys                          
import requests
from bs4 import BeautifulSoup
from collections import Counter
import re


# python PythonScraper_SimHash.py <URL>
# Example: python PythonScraper_SimHash.py https://www.sitare.org
# sys.argv[0] = script name, sys.argv[1] = URL provided by user
if len(sys.argv) != 2:
    print("Usage: PythonScraper_SimHash.py <URL>") 
    sys.exit(1)
site_url = sys.argv[1]
print("URL entered:", site_url)


# Send an HTTP GET request to the provided URL and check if the page loaded successfully
page_response = requests.get(site_url)
if page_response.status_code == 200:
    print("Page fetched successfully")
else:
    print(f"FAILED SUCCESSFULLY Status code: {page_response.status_code}")
    sys.exit(1)


# Creates the parsetree that's structured DOM out of the raw html
raw_htmlcontent = page_response.text        
parse_tree = BeautifulSoup(raw_htmlcontent, "html.parser")

# Extract the page title if it exists
if parse_tree.title:
    page_title = parse_tree.title.string
else:
    page_title = "Page doesn't have any TITLE"
print("Page Title:\n", page_title)


# It extracts all the text from the html page while removing tags.
if parse_tree.body:
    page_body = parse_tree.body.get_text()
else:
    page_body = "PAGE DOESN't HAVE BODY"
print("Page_body:\n" + page_body + "\n")


# It scrapes all the links which are in anchor tag.
page_links = []
for hyperlink in parse_tree.find_all("a"):
    link_url = hyperlink.get("href")                    
    if link_url:                                        
        page_links.append(link_url)
print("All URLs found are")
for url in page_links:
    print(url)


#converts text to lowercase and rmoves special character only alphanums allowed, then count the frequency of each wor.
lower_case = page_body.lower()
words = re.findall(r'\b[a-z0-9]+\b', lower_case)
word_count = Counter(words)


def get_hash(word):
    p = 53                                              # Prime base for polynomial rolling hash
    mod = 1 << 64                                       
    hashed_value = 0
    multiplier = 1
    for ch in word:
        hashed_value = (hashed_value + ord(ch) * multiplier) & (mod - 1)   # it adds the weighted ascii value of each character
        multiplier = (multiplier * p) & (mod - 1)                         
    return hashed_value

def evaluate_SimHash(word_count):
    bits_list = [0] * 64                                #creates bit list of 64 bits with 0 initally.
    for word in word_count:
        hashed_word = get_hash(word)
        frequency = word_count[word]
        i = 0
        while i < 64:
            if (hashed_word >> i) & 1:                  
                bits_list[i] += frequency               # if bit is 1 then increase frequency
            else:
                bits_list[i] -= frequency               # if bit is 0 then decrease the frequency
            i += 1


    fingerprint = 0                                     #final fingerprint is created
    for i in range(64):
        if bits_list[i] > 0:                            # if it is positive then set bit i to 1.
            fingerprint = fingerprint + (1 << i)
    return fingerprint                                  


def similarity_check(hash1, hash2):
    x = hash1 ^ hash2                                 #taking XOR.
    diff_bits = 0
    while x:
        if x & 1:
            diff_bits += 1                            
        x >>= 1
    matching_bits = 64 - diff_bits
    return matching_bits                              #we get how much of word is similar and detect duplicates based on the similarity among the documents.



SimHash_value = evaluate_SimHash(word_count)
print(f"SimHash (64-bit): {SimHash_value}\nBinary: {bin(SimHash_value)}")
