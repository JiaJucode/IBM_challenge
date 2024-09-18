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
        resp = requests.post(PLACES_URL, data=json.dumps(data), headers=headers)
        print(resp.text)

if __name__ == "__main__":
    ts = TextSearch()
    ts.query = "mexican restaurant cambridge"
    ts.get_response()

    # sample response
    {
  "places": [
    {
      "formattedAddress": "The, Grafton Centre, Cambridge CB1 1PS, UK",
      "displayName": {
        "text": "La Latina Bustaurante",
        "languageCode": "en"
      }
    },
    {
      "formattedAddress": "21 Hills Rd, Cambridge CB2 1NW, UK",
      "displayName": {
        "text": "The Emperor",
        "languageCode": "en"
      }
    },
    {
      "formattedAddress": "68A Mill Rd, Petersfield, Cambridge CB1 2AS, UK",
      "displayName": {
        "text": "Mr Taco",
        "languageCode": "en"
      }
    },
    {
      "formattedAddress": "Station Sq, Cambridge CB1 2GA, UK",
      "displayName": {
        "text": "Alchile Mexican Gourmet",
        "languageCode": "es"
      }
    },
    {
      "formattedAddress": "33 Regent St, Cambridge CB2 1AB, UK",
      "displayName": {
        "text": "Urban Butterfly",
        "languageCode": "en"
      }
    },
    {
      "formattedAddress": "Quayside, Bridge St, Cambridge CB5 8AB, UK",
      "displayName": {
        "text": "Las Iguanas - Cambridge",
        "languageCode": "en"
      }
    },
    {
      "formattedAddress": "29 Petty Cury, Cambridge CB2 3NB, UK",
      "displayName": {
        "text": "Nanna Mexico",
        "languageCode": "en"
      }
    },
    {
      "formattedAddress": "24 Green St, Cambridge CB2 3JX, UK",
      "displayName": {
        "text": "Mercado Central",
        "languageCode": "en"
      }
    },
    {
      "formattedAddress": "3 Thompsons Ln, Cambridge CB5 8AQ, UK",
      "displayName": {
        "text": "La Mimosa",
        "languageCode": "en"
      }
    },
    {
      "formattedAddress": "18 Market Hill, Cambridge CB2 3NR, UK",
      "displayName": {
        "text": "Tortilla Cambridge",
        "languageCode": "en"
      }
    },
    {
      "formattedAddress": "4-6 Rose Cres, Cambridge CB2 3LL, UK",
      "displayName": {
        "text": "La Raza",
        "languageCode": "en"
      }
    },
    {
      "formattedAddress": "Extra Services, Cambridge CB23 4WU, UK",
      "displayName": {
        "text": "El Mexicana",
        "languageCode": "en"
      }
    },
    {
      "formattedAddress": "10 Market Passage, Cambridge CB2 3PA, UK",
      "displayName": {
        "text": "Taco Bell",
        "languageCode": "en"
      }
    }
  ]
}


