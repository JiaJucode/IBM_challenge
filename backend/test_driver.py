import json

import utils.ai as bot
print("Loaded AI module")
import utils.google_search_client as google_search
from utils.helpers import recursive_truncate

## 1. Get Search Query
print("Step 1: Get Search Query")
search_query = "how to write a flask route that returns hello world"
# search_query = "why were javascript frameworks created when everything could be done with vanilla javascript"
# search_query = input("Enter search query: ")


# 2. Perform Search
print("Step 2: Perform Search")
search_results = google_search.search(search_query, top_n=3)
print("Search Results:")
print(json.dumps(search_results, indent=4))
print("\n\n")


# 3. Scrape Contents of Each Search Result Website 
print("Step 3: Scrape Contents of Each Search Result Website")
links = [search_result["link"] for search_result in search_results]
scraped_contents = google_search.scrape_contents(links)
for i, scraped_content in enumerate(scraped_contents):
    search_results[i]["content"] = scraped_content

print("Scraped Contents:") 
print(json.dumps(search_results, indent=4))

# 4. Generate Search Summary
# print("Step 4: Generate Search Summary")
# # keep title, link, and content keys only
# search_summary = bot.summarize_search_results(search_query=search_query, search_results=[{k: v for k, v in search_result.items() if k in ["title", "link", "content"]} for search_result in search_results])
# print("\n\n\n----------------- Search Summary -----------------")
# print(search_summary)
# print("\n\n\n")


w0 = search_results[1]
summary = bot.summarize_result_website(search_query=search_query, website_contents=w0["content"])
print("\n\n\n----------------- Summary -----------------")
print(f"Website: {w0['link']}, Title: {w0['title']} \n\n")
print(summary)
print("\n\n\n")


