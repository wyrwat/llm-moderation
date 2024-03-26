import requests
from dotenv import load_dotenv
import os

load_dotenv()
OPEN_AI_KEY = os.getenv("OPENAI_API_KEY")
AI_DEVS_KEY = os.getenv("AIDEVS_API_KEY")

TOKEN = "https://tasks.aidevs.pl/token/moderation"
ANSWER = "https://tasks.aidevs.pl/answer"
TASK = "https://tasks.aidevs.pl/task"
MODERATOR = "https://api.openai.com/v1/moderations"

token_params = {
    "apikey": AI_DEVS_KEY
}

token_response = requests.post(url=TOKEN, json=token_params)
token_response.raise_for_status()
token_data = token_response.json()
token = token_data["token"]

get_task_response = requests.get(url=f"{TASK}/{token}")
token_response.raise_for_status()
task_data = get_task_response.json()
task_text = task_data['input']

results_table = []
def modarate_text(text_to_modarate):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPEN_AI_KEY}"
    }

    data = {
        "input": text_to_modarate
    }

    response = requests.post(url=MODERATOR, headers=headers, json=data)
    response.raise_for_status()
    response_data = response.json()
    result = response_data["results"][0]["flagged"]
    if result == True:
        results_table.append(1)
    else:
        results_table.append(0)


for text in task_text:
    modarate_text(text)

answer = {
    "answer": results_table
}

send_answer = requests.post(url=f"{ANSWER}/{token}", json=answer)
token_response.raise_for_status()

