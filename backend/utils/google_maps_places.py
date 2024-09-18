import os, requests, json

# Google Maps places API: https://developers.google.com/maps/documentation/places/web-service/text-search?hl=en
PLACES_URL = "https://places.googleapis.com/v1/places:searchText"
api_key = os.getenv("MAPS_API")

class TextSearch:
    def __init__(self) -> None:
        self.query = ""
        self.masks = ["displayName", "formattedAddress"]

    def get_response(self):
        data = {"textQuery": self.query}
        headers = {"Content-Type": "application/json", "X-Goog-Api-Key": api_key}
        all_masks = ""
        for mask in self.masks:
            all_masks += f"places.{mask},"
        headers["X-Goog-FieldMask"] = all_masks[:-1]
        resp = requests.post(PLACES_URL, data=data, headers=headers)
        print(resp.text)

if __name__ == "__main__":
    ts = TextSearch()
    ts.query = "mexican restaurant cambridge"
    ts.get_response()

