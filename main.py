import requests
from dotenv import load_dotenv
import os
import json
from datetime import datetime
import logging

#Other files
import notify
import state
import maps



logging.basicConfig(
    filename="run.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# google api key
GOOGLE_ROUTES_URL = "https://routes.googleapis.com/directions/v2:computeRoutes"



# max ratio of route time / route time with real traffic data
THRESHOLD = 1.25

# Load address
MY_HOME_ADDRESS = json.loads(os.getenv("MY_HOME_ADDRESS"))
MY_DESTINATION_ADDRESS = json.loads(os.getenv("MY_DESTINATION_ADDRESS"))

# api call parameters
headers = {
    "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
    "X-Goog-FieldMask": "routes.duration,routes.staticDuration,routes.distanceMeters",
}

body = {
    "origin": MY_HOME_ADDRESS,
    "destination": MY_DESTINATION_ADDRESS,
    "travelMode": "DRIVE",
    "computeAlternativeRoutes": True,
    "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
}

response = requests.post(GOOGLE_ROUTES_URL, headers=headers, json=body)


logging.info(f"API Call Response Code: {response.reason}")

# store google response
routes = response.json()["routes"][0]

# calculate route time with no traffic data and with traffic data
duration = int(routes["duration"].rstrip("s"))
staticDuration = int(routes["staticDuration"].rstrip("s"))

# convert to minutes
durationMin = round(duration / 60, 2)
staticDurationMin = round(staticDuration / 60, 2)

# calculate the ratio
delayRatio = round(duration / staticDuration, 3)
delayMinutes = round(durationMin - staticDurationMin, 1)

# delayRatio = 1.1 #for testing





# get state from file
current_state = state.load_state()
previous_status = current_state["status"]


logging.info(
    f"Delay Ratio is {delayRatio}, Total Delay is {delayMinutes}m, Duration To Destination is {durationMin}m, Distance To Destination is {routes['distanceMeters']/1000}km"
)


# calculate if there is traffic
if delayRatio > THRESHOLD:
    new_status = "bad"
else:
    new_status = "normal"

# if there is a change in state, bad to normal and normal to bad
if new_status != previous_status:
    state.save_state(new_status)
    if new_status == "bad":
        notify.send_notifications(f"High Traffic Alert, {delayMinutes}m delay")
        logging.warning(f"High Traffic Alert, {delayMinutes}m delay")
    else:
        notify.send_notifications("Traffic Back To Normal")
        logging.info("Back To Normal Traffic Alert")