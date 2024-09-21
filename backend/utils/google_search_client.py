import requests
import os

api_key = os.getenv("GOOGLE_API_KEY")
search_engine_id = os.getenv("GOOGLE_SEARCH_ENGINE_ID") 

url = f"https://www.googleapis.com/customsearch/v1?"

def search(search_query):
    params = f"key={api_key}&exactTerms={(search_query).replace(" ", "%20")}&cx={search_engine_id}&lr=lang_en&sort=date:d:s&start=1"
    print("searching for: ", search_query)
    return requests.get(url + params).json()

def extract_content(search_query):
    results = search(search_query)
    contents = []
    if "items" not in results:
        print("error: no items in results")
        print(results)
        return {}
    for item in results["items"]:
        link = item["link"]
        title = item["title"]
        # some websites may block the request
        try:
            html = requests.get(link, timeout=5)
        except requests.exceptions.Timeout:
            print("website: ", link, " Timeout")
            continue
        except Exception as e:
            print("website: ", link, " Error: ", e)
            continue
        if html.status_code != 200:
            print("website: ", link, " Error: ", html.status_code)
            continue
        contents.append({"title": title, "content": html.text, "link": link})
    return contents

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
#pagemap is optional
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
