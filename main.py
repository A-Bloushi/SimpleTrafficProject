import logging
from datetime import datetime

# Other files
import notify
import state
import maps
import settings
import db

logging.basicConfig(
    filename="run.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
current_time = datetime.now()

# create sqlite table if it doesn't already exist
db.create_table()

# store google response
routes = maps.get_route()

# calculate route time with no traffic data and with traffic data
duration = int(routes["duration"].rstrip("s"))
static_duration = int(routes["staticDuration"].rstrip("s"))

# convert to minutes
duration_min = round(duration / 60, 2)
static_duration_min = round(static_duration / 60, 2)

# calculate the ratio
delay_ratio = round(duration / static_duration, 3)
delay_minutes = round(duration_min - static_duration_min, 1)

# delay_ratio = 1.1 #for testing

# get state from file
current_state = state.load_state(current_time)
previous_status = current_state["status"]


logging.info(
    f"Delay Ratio is {delay_ratio}, Total Delay is {delay_minutes}m, Duration To Destination is {duration_min}m, Distance To Destination is {routes['distanceMeters']/1000}km"
)

# calculate if there is traffic
if delay_ratio > settings.THRESHOLD:
    new_status = "bad"
else:
    new_status = "normal"

# if there is a change in state, bad to normal and normal to bad
if new_status != previous_status:
    state.save_state(new_status, current_time)
    if new_status == "bad":
        notify.send_notification(f"High Traffic Alert, {delay_minutes}m delay")
        logging.warning(f"High Traffic Alert, {delay_minutes}m delay")
    else:
        notify.send_notification("Traffic Back To Normal")
        logging.info("Back To Normal Traffic Alert")

db.log_check(
    f"{current_time.date()} {current_time.strftime('%I:%M:%S %p')}",
    delay_ratio,
    delay_minutes,
    new_status,
)