import json
import logging

logging.basicConfig(
    filename="run.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


# return normal state with current date
def default_state(current_time):
    state = {
        "status": "normal",
        "date": str(current_time.date()),
        "time": current_time.strftime("%I:%M:%S %p"),
    }
    save_state(state["status"], current_time)
    return state


# load current state and time from json file
def load_state(current_time):
    try:
        with open("state.json", "r") as f:
            data = json.load(f)
            # compares date on file with today's date
            current_date = str(current_time.date())

            if data["date"] != current_date:
                return default_state(current_time)
            else:
                return data
    except FileNotFoundError:
        logging.warning("state.json Doesn't Exist!")
        return default_state(current_time)


# save current state and time to json file
def save_state(state, current_time):
    with open("state.json", "w") as f:
        state_time = {
            "status": state,
            "date": str(current_time.date()),
            "time": current_time.strftime("%I:%M:%S %p"),
        }
        json.dump(state_time, f)
