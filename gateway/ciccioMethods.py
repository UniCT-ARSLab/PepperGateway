
        # # [TODO] Setting Up Useless Variables
        # self.saveMessage = False # Flag to start to save message
        # self.MAX_BLOCK_RECOGNIZED = 3 # Max number of text blocks recognized
        # self.messageCounter = self.MAX_BLOCK_RECOGNIZED # Dinamically updated counter
        # self.finalMessage = "" # Final message recognized after keyword
        # self.COUNTER = 0
# def startListeningThread(self):
    #     startStreamThread = threading.Thread(target=self.startStream, args=())
    #     startStreamThread.setDaemon(True)
    #     startStreamThread.start()

    # def startMicrophone(self, isStreaming = False):
    #     self.speech_service.setAudioExpression(False) # Disable audio expression
    #     self.speech_service.setVisualExpression(False) # Disable visual expression
    #     self.audio_recorder.stopMicrophonesRecording() # Stop any previous recording
        
    #     print("[INFO]: Robot is listening to you...")
    #     # self.audio_recorder.startMicrophonesRecording("/home/nao/speech.wav", "wav", 48000, (0, 0, 1, 0))
    #     if (isStreaming):
    #         AUDIO_FILE = "speech" + str(self.COUNTER) + ".wav"
    #     else: AUDIO_FILE = "speech.wav"
    #     try:
    #         os.system("rm tmp/" + AUDIO_FILE) # Remove previous audio file
    #     except:
    #         pass
    #     print("[INFO] Inizio registrazione file : " + AUDIO_FILE)
    #     self.audio_recorder.startMicrophonesRecording(AUDIO_FILE, "wav", 48000, (0, 0, 1, 0))
        
    #     return "[INFO] Starting Microphone..."

    # def stopMicrophone(self, isStreaming = False):
    #     self.audio_recorder.stopMicrophonesRecording()
    #     print("[INFO]: Robot is not listening to you...")

    #     if (isStreaming):
    #         AUDIO_FILE = "speech" + str(self.COUNTER) + ".wav"
    #     else: AUDIO_FILE = "speech.wav"
    #     print("[INFO] Termino registrazione file : " + AUDIO_FILE)
    #     self.download_file(AUDIO_FILE)        
    #     print("[INFO] Effettuo download del file : " + AUDIO_FILE)
    
    #     if (isStreaming):
    #         self.ssh.exec_command('rm /home/nao/' + AUDIO_FILE)
    #         print("[INFO] Elimino il file : " + AUDIO_FILE)

    #         self.speech_service.setAudioExpression(True)
    #         self.speech_service.setVisualExpression(True)
    #         streamThread = threading.Thread(target=self.streamSpeechToText, args=[AUDIO_FILE])
    #         streamThread.setDaemon(True)
    #         streamThread.start()
    #         self.COUNTER += 1
    #     return "[INFO] Stopping Microphone..."
        
    
    # def startStream(self):
    #     while True:
    #         self.startMicrophone()
    #         time.sleep(2)
    #         self.stopMicrophone()

    # def speechToText(self, AUDIO_FILE):
    #     audio_file = speech_recognition.AudioFile("tmp/" + AUDIO_FILE)
    #     with audio_file as source:
    #         audio = self.recognizer.record(source)
    #         recognized = self.recognizer.recognize_google(audio, language="it-IT", show_all=True)
    #     print(recognized)
    #     os.system("rm tmp/" + AUDIO_FILE)
    #     return self.say(GPT.getResponse(recognized["alternative"][0]["transcript"])) if recognized else "[ERROR]"

    # def streamSpeechToText(self, audio_file):
    #     textRecognized = self.speechToText(audio_file)
    #     textRecognized = textRecognized.lower()
    #     keywordsList = ["mario", "alexa", "pepper", "peppe", "beppe", "chicco"]
    #     if not self.saveMessage:
    #         for keyword in keywordsList:
    #             if keyword in textRecognized:
    #                 print("[INFO]: Keyword recognized!]")
    #                 self.messageCounter = self.MAX_BLOCK_RECOGNIZED
    #                 self.saveMessage = True
    #     else:
    #         if self.messageCounter == 0: 
    #             self.saveMessage = False
    #             print("[INFO] FINAL Recognized : " + self.finalMessage)
    #             # r = requests.post(url = "http://0.0.0.0:5000/getAnswer", data = {"message" : self.finalMessage})
    #             self.say(GPT.getResponse(self.finalMessage))
    #             self.finalMessage = ""
    #         else:
    #             print("[INFO] TEMP Recognized : " + textRecognized)
    #             self.messageCounter -= 1
    #             self.finalMessage += textRecognized