import json
import os
from dotenv import load_dotenv

load_dotenv()

# max ratio of route time / route time with real traffic data
THRESHOLD = 1.25

# Load address
MY_HOME_ADDRESS = json.loads(os.getenv("MY_HOME_ADDRESS"))
MY_DESTINATION_ADDRESS = json.loads(os.getenv("MY_DESTINATION_ADDRESS"))