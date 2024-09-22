import requests
import os
from bs4 import BeautifulSoup, Comment
from language_model import entailment_filter

api_key = os.getenv("GOOGLE_API_KEY")
search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

url = f"https://www.googleapis.com/customsearch/v1?"


def search(search_query, top_n=5):
    # params = f"key={api_key}&q={(search_query).replace(' ', '%20')}&cx={search_engine_id}&lr=lang_en"
    params = {
        "key": api_key,
        "q": search_query,
        "cx": search_engine_id,
        "lr": "lang_en"
    }

    print("searching for: ", search_query)
    search_results = requests.get(url, params=params).json()

    if "error" in search_results or "items" not in search_results:
        print("error: ", search_results)
        return []

    top_results = []
    for item in search_results["items"][:top_n]:
        top_results.append({
            "title": item["title"],
            "link": item["link"],
            "snippet": item["snippet"]
        })

    return top_results


def scrape_contents(query:str, website_links: list) -> list:
    '''
    Scrape contents of websites from a list of website links.
    Returns html content of each website as a single string for each website.
    '''
    contents = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for link in website_links:
        try:
            response = requests.get(link, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "lxml")

            # remove unwanted tags
            for tag in soup(["script", "style", "meta", "link", "head", "title", "header", "footer", "nav", "form"]):
                tag.decompose()

            # remove html attributes from all tags
            for tag in soup.find_all(True):
                tag.attrs = {}

            # remove all html  comments
            for element in soup(text=lambda text: isinstance(text, Comment)):
                element.extract()   

            
            # store contents
            contents.append(entailment_filter(query, ' '.join(soup.stripped_strings)))
            # contents.append(soup.prettify())


        except Exception as e:
            print(f"Failing to scrape website: {link}: {e}")
            contents.append("")
    return contents


if __name__ == "__main__":
    import json

    # query = "Write a flask route that returns hello world"
    # results = search(query, top_n=1)

    # print("Search Results:")
    # print(json.dumps(results, indent=4))
    # print("\n\n")
    results = [{"link": "https://www.mongolia-travel-and-tours.com/climate-mongolia.html#:~:text=Mongolia%20%2D%20because%20of%20its%20high,particularly%20in%20the%20Gobi%20Desert."},
               {"link": "https://climateknowledgeportal.worldbank.org/country/mongolia/climate-data-historical"},
               {"link": "https://stackoverflow.com/questions/24398302/bs4-featurenotfound-couldnt-find-a-tree-builder-with-the-features-you-requeste"}]

    print("Scraped Contents:")
    scraped_contents = scrape_contents("What is the weather like in Mongolia at winter?", [result["link"] for result in results])
    scraping = {result["link"]: content for result, content in zip(results, scraped_contents)}
    print(json.dumps(scraping, indent=4))

# print(json.dumps(search(request_builder()), indent=4))
# example output:
# {
#     ...
#    "queries": {
#        "request": [
#            {
#                "totalResults": "4420000000",
#                "count": 10,
#                "startIndex": 1,
#                "language": "lang_en",
#                "inputEncoding": "utf8",
#                "outputEncoding": "utf8",
#                "safe": "off",
#                "cx": "c41ac0548f58c4e56",
#                "sort": "date:d:s",
#                "exactTerms": "test"
#            }
#        ],
#        "nextPage": [
#            {...similar to request...}
#        ]
#    },
#    ...
#   "items": [
#        {
#            "kind": "customsearch#result",
#            "title": "Test to Treat\u200b | HHS/ASPR",
#            "htmlTitle": "<b>Test</b> to Treat\u200b | HHS/ASPR",
#            "link": "https://aspr.hhs.gov/TestToTreat/Pages/default.aspx",
#            "displayLink": "aspr.hhs.gov",
#            "snippet": "Learn about the Test to Treat initiative, which helps people get tested for COVID-19 and receive treatment, if appropriate, in one location.",
#            "htmlSnippet": "Learn about the <b>Test</b> to Treat initiative, which helps people get tested for COVID-19 and receive treatment, if appropriate, in one location.",
#            "formattedUrl": "https://aspr.hhs.gov/TestToTreat/Pages/default.aspx",
#            "htmlFormattedUrl": "https://aspr.hhs.gov/<b>Test</b>ToTreat/Pages/default.aspx",
# pagemap is optional
#            "pagemap": {
#                "cse_thumbnail": [
#                    {
#                        "src": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ6KXMTDLvAJgG72KYLonvtp76wy1WKVWCg0z5K-R6j3CgSTR-MtG_oztE&s",
#                        "width": "310",
#                        "height": "163"
#                    }
#                ],
#                "metatags": [
#                    {
#                        "og:image": "https://aspr.hhs.gov/_catalogs/masterpage/ASPR/images/Misc/aspr-socialmedia-splashscreen.jpg",
#                        "viewport": "width=device-width, initial-scale=1",
#                        "facebook-domain-verification": "3yr5dfpltk6cm014r6admo2mesw2jc"
#                    }
#                ],
#                "cse_image": [
#                    {
#                        "src": "https://aspr.hhs.gov/_catalogs/masterpage/ASPR/images/Misc/aspr-socialmedia-splashscreen.jpg"
#                    }
#                ]
#            }
#        },
