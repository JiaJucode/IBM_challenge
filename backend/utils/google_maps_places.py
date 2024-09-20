import os, requests, json
import numpy as np

# Google Maps places API: https://developers.google.com/maps/documentation/places/web-service/text-search?hl=en
PLACES_URL = "https://places.googleapis.com/v1/places:searchText"
EARTH_RADIUS = 6371
api_key = os.getenv("MAPS_API")

def to_rad(degree):
    return np.pi * degree/180

def earth_distance(lon1, lat1, lon2, lat2):
    # In kilometer, the distance between 2 geo-coordinates
    lats = [to_rad(lat) for lat in (lat1, lat2)]
    lons = [to_rad(lon) for lon in (lon1, lon2)]
    rise2 = pow(np.sin(lats[0])-np.sin(lats[1]), 2)
    ra = np.cos(lats[0])
    rb = np.cos(lats[1])
    run2 = ra*ra + rb*rb - 2*ra*rb*np.cos(lons[0] - lons[1])
    ang = 2*np.arcsin(min(np.sqrt(rise2+run2)/2, 1))
    return EARTH_RADIUS * ang

class MapsTextSearch:
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
        return resp.text

if __name__ == "__main__":
    ts = MapsTextSearch()
    ts.query = "mexican restaurant cambridge"
    ts.get_response()
    # print(earth_distance(0, 35, 110, 55))

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


