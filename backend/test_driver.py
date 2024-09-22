import json

import utils.ai as bot
print("Loaded AI module")
import utils.google_search_client as google_search
from utils.helpers import get_middle_truncated_text

## 1. Get Search Query
print("Step 1: Get Search Query")
# search_query = "how to write a flask route that returns hello world"
# search_query = "why were javascript frameworks created when everything could be done with vanilla javascript"
# search_query = "What are the techniques to improve the performance of a dynamic website"
search_query = "How is automatic speech recognition done?"
# search_query = input("Enter search query: ")


# 2. Perform Search
print("Step 2: Perform Search")
search_results = google_search.search(search_query, top_n=3)


# 3. Scrape Contents of Each Search Result Website 
print("Step 3: Scrape Contents of Each Search Result Website")
links = [search_result["link"] for search_result in search_results]
scraped_contents = google_search.scrape_contents(links)
for i, scraped_content in enumerate(scraped_contents):
    search_results[i]["content"] = get_middle_truncated_text(scraped_content)


# 4. Generate  summary for each website
print("Step 4: Generate Summary for Each Website")
for i, search_result in enumerate(search_results):
    print(f"Summarizing {i+1} of {len(search_results)}")
    search_result["summary"] = bot.summarize_result_website(search_query=search_query, website_contents=search_result["content"])
    # print(f"Summary for {search_result['link']}: {search_result['summary']}")

# 6. Summarize Search Results
print("Step 6: Summarize Search Results")
search_summary = bot.summarize_search_results(search_query=search_query, search_results=[{k: v for k, v in search_result.items() if k in ["title", "link", "summary"]} for search_result in search_results])
print("\n\n\n----------------- Search Summary -----------------")
print(search_summary)

