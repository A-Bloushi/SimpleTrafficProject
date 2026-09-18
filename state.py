from datetime import datetime
import json
import logging

logging.basicConfig(
    filename="run.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

current_datetime = datetime.now()


# return normal state with current date
def default_state():
    state = {
        "status": "normal",
        "date": str(current_datetime.date()),
        "time": current_datetime.strftime("%I:%M:%S %p"),
    }
    save_state(state["status"])
    return state


# load current state and time from json file
def load_state():
    try:
        with open("state.json", "r") as f:
            data = json.load(f)
            # compares date on file with today's date
            if data["date"] != str(current_datetime.date()):
                return default_state()
            else:
                return data
    except FileNotFoundError:
        logging.warning("state.json Doesn't Exist!")
        return default_state()


# save current state and time to json file
def save_state(state):
    with open("state.json", "w") as f:
        stateTime = {
            "status": state,
            "date": str(current_datetime.date()),
            "time": current_datetime.strftime("%I:%M:%S %p"),
        }
        json.dump(stateTime, f)