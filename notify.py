import os
import requests
from dotenv import load_dotenv

load_dotenv()

# url for notification app
NTFY_URL = os.getenv("ntfy_url")


def send_notifications(data):
    requests.post(NTFY_URL, data)