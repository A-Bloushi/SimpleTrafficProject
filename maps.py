import os
from dotenv import load_dotenv
import requests
import logging

import settings

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# google api key
GOOGLE_ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"

# api call parameters
headers = {
    "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
    "X-Goog-FieldMask": "routes.duration,routes.staticDuration,routes.distanceMeters",
}

body = {
    "origin": settings.MY_HOME_ADDRESS,
    "destination": settings.MY_DESTINATION_ADDRESS,
    "travelMode": "DRIVE",
    "computeAlternativeRoutes": True,
    "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
}


def get_route():
    response = requests.post(GOOGLE_ROUTES_URL, headers=headers, json=body,timeout=10)
    logging.info(f"API Call Response Code: {response.reason}")
    return response.json()["routes"][0]