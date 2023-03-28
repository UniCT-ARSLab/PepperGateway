# -*- coding: UTF-8 -*-
import requests
import json
import re
import os
import config
import robot

class GPT():
    """
    **Chatter Bot for Pepper Robot (use ChatGPT API)**
    """
    def __init__(self):
        self.URL = "https://api.openai.com/v1/chat/completions"
        self.setup_string = config.SETUP
        self.payload = {
            "model": "gpt-3.5-turbo",
            "messages": [],
            "temperature" : 1.0,
            "top_p":1.0,
            "n" : 1,
            "stream": False,
            "presence_penalty":0,
            "frequency_penalty":0,
            "max_tokens": 40,
        }
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + config.CHATGPT_API_KEY
        }
        print("[INFO]: Loading session...")
        self.getAnswer(question=self.setup_string, role="user")
        print("[INFO]: Init GPT-3.5 Turbo completed!")
    
    def getAnswer(self, question, role = "user"):
        """
        Get all answers from robot using ChatGPT API.

        :param question: Question to the robot
        :type path: string
        """
        new_message = {"role": role, "content": question}
        self.payload['messages'].append(new_message)
        self.payload['messages'][0]['content'] = question
        response = requests.post(self.URL, headers=self.headers, json=self.payload, stream=False).json()
        self.payload['messages'].append(response['choices'][0]["message"])
        data = response['choices'][0]["message"]["content"]
        cleanResponse = re.sub("\s\s+" , " ", data)
        return cleanResponse


