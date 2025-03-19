import requests
import uuid
from datetime import datetime, timezone
import time
import json
import re 
import sys
import random

sys.stdout.reconfigure(encoding='utf-8')


accesstoken = "" 
api_base_url = "https://stanfordohs.pronto.io/"
user_id = "0000000"
bubbleID = "3436833" #our dms


headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {accesstoken}",
}


warning_message = ""
last_message_id = ""



        

def fetch_latest_message():
    """Fetch only the most recent message"""
    url = f"{api_base_url}api/v1/bubble.history"
    data = {"bubble_id": bubbleID}
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        messages = response.json().get("messages", [])
        return messages[0]  
    else:
        print(f"HTTP error occurred: {response.status_code} - {response.text}")

    return None  

def monitor_messages():
    """Continuously fetch the latest message and check for flagged words."""
    global warning_message  
    global last_message_id

    while True:
        msg = fetch_latest_message()

        if msg and isinstance(msg, dict) and "message" in msg and "user_id" in msg and "id" in msg:
            msg_id = msg["id"]
            msg_text = msg["message"].lower()

            if msg_id != last_message_id:  #only process if it's a new message
                last_message_id = msg_id  #update last seen message

                words = msg_text.lower()
                if "@tod" in words:
                    tod(words)

        time.sleep(1)  #can change if necessary



def fetch_tod(tod):
    if tod == 1:
        url = "https://api.truthordarebot.xyz/v1/truth"
    else:
        url = "https://api.truthordarebot.xyz/v1/dare"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()["question"]
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except json.JSONDecodeError:
         print("Failed to decode JSON. Check the response content.")
         return None




def send_message(message):
    unique_uuid = str(uuid.uuid4())
    messageCreatedat = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


    data = {
        "id": "Null",
        "uuid": unique_uuid,
        "bubble_id": bubbleID,
        "message": message,
        "created_at": messageCreatedat,
        "user_id": user_id,
        "messagemedia": []
    }


    url = f"{api_base_url}api/v1/message.create"
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()


def tod(message):
    if "truth" in message:
        send_message("Truth: " + fetch_tod(1))
    elif "dare" in message:
        send_message("Dare: " + fetch_tod(2))
    else:
        send_message("Random: " + fetch_tod(random.randint(1,2)))



monitor_messages()
