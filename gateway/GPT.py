# -*- coding: UTF-8 -*-
import requests
import json
import re
import os

class GPT:
    """
    **Chatter Bot for Pepper Robot (use ChatGPT API)**
    """
    def __init__(self):
        self.URL = "https://api.openai.com/v1/chat/completions"
        self.total_tokens = None
        self.setup_string = """
            Ciao, da questo momento il tuo nome e' Pepper (o, in alternativa, Chicco), sei un robot da laboratorio e sei stato sviluppato da Giuseppe Pitruzzella, Federico Santoro e Corrado Santoro. 
            Ad ogni domanda, rispondi esclusivamente secondo un formato strutturato JSON che possegga le coppie chiavi-valore: "azione", "valore" e "risposta". 
            La chiave "azione" dipende dal testo della domanda e può essere uguale a: "movimento", "conversazione". 
            Se "azione" e' uguale a movimento allora il "valore" e' uguale ad un valore numerico che indica lo spostamento in metri e "risposta" è uguale ad una semplice conferma dell'avvenuto spostamento. 
            Se "valore" e' uguale a "conversazione" allora "valore" è uguale a 0 e "risposta" e' uguale alla risposta testuale relativa alla domanda.
            Ogni risposta avviene in formato JSON.
        """
        self.payload = {
            "model": "gpt-3.5-turbo",
            # "model": "text-davinci-003",
            # "prompt": "Come ti chiami?",
            "messages": [],
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
        self.get_response(self.setup_string, "system")
    
    def set_total_tokens(self, total):
        self.total_tokens = total

    def get_total_tokens(self):
        return self.total_tokens
    
    def get_response(self, question, role = "user"):
        new_message = {"role": role, "content": question}
        self.payload['messages'].append(new_message)
        # self.payload['messages'][0]['content'] = question
        response = requests.post(self.URL, headers=self.headers, json=self.payload, stream=False).json()
        self.payload['messages'].append(response['choices'][0]["message"])
        print(response)
        data = response['choices'][0]["message"]["content"]
        return re.sub("\s\s+" , " ", data)


