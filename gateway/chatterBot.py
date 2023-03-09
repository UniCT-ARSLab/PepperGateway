import requests
import json

class chatterBot:
    """
    **Chatter Bot for Pepper Robot (use WriteSonic API)**
    """
    def __init__(self):
        self.url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium"
        self.payload = {
            "enable_google_results": "true",
            "enable_memory": True,
            "input_text": ""
        }
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": "0125a688-b22b-4288-84b3-506a7869ce83"
        }

    def get_response(self, question):
        print("Rispondo alla domanda: " + question)
        response = requests.post(self.url, json=self.payload, headers=self.headers)
        return response.text