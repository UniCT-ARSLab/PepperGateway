import requests
import json
import os

class GPT:
    """
    **Chatter Bot for Pepper Robot (use ChatGPT API)**
    """
    def __init__(self):
        self.URL = "https://api.openai.com/v1/chat/completions"
        self.payload = {
            "model": "code-davinci-002",
            "messages": [{"role": "user", "content": "Dove si trova Catania?"}],
            "temperature" : 1.0,
            "top_p":1.0,
            "n" : 1,
            "stream": False,
            "presence_penalty":0,
            "frequency_penalty":0,
        }
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer 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"
        }
        # response = requests.post(self.URL, headers=self.headers, json=self.payload, stream=False)
        # print(response.content)
    
    def get_response(self, question):
        return "OK"
    


