import qi
import argparse
import sys
import time
import numpy as np
import requests
import time

THRESHOLD = 5
MAX_FRAME_TO_PROCESS = 20
MAX_FRAME_LESS_THAN_THRESHOLD = 10

class SoundProcessingModule(object):
    """
    A simple get signal from the front microphone of Nao & calculate its rms power.
    It requires numpy.
    """

    def __init__( self, app):
        """
        Initialise services and variables.
        """
        super(SoundProcessingModule, self).__init__()
        app.start()
        self.session = app.session

        # Get the service ALAudioDevice.
        self.audio_service = self.session.service("ALAudioDevice")
        self.speech_service = self.session.service("ALSpeechRecognition")
        self.audio_recorder = self.session.service("ALAudioRecorder")
        self.isProcessingDone = False
        self.nbOfFramesToProcess = 20
        self.framesCount=0
        self.micFront = []
        self.module_name = "SoundProcessingModule"

        self.isRecording = False
        self.timeOut = 0
        self.COUNTER = 0

    def startProcessing(self):
        """
        Start processing
        """
        # ask for the front microphone signal sampled at 16kHz
        # if you want the 4 channels call setClientPreferences(self.module_name, 48000, 0, 0)
        self.audio_service.setClientPreferences(self.module_name, 16000, 3, 0)
        self.audio_service.subscribe(self.module_name)

        while True:
            time.sleep(1)

        self.audio_service.unsubscribe(self.module_name)

    def processRemote(self, nbOfChannels, nbOfSamplesByChannel, timeStamp, inputBuffer):
        """
        Compute RMS from mic.
        """
        self.micFront=self.convertStr2SignedInt(inputBuffer)
        rmsMicFront = self.calcRMSLevel(self.micFront)
        if rmsMicFront > THRESHOLD: self.COUNTER = 0

        if (rmsMicFront > THRESHOLD
            and not self.isRecording 
            and self.timeOut < MAX_FRAME_TO_PROCESS):
            self.isRecording = True
            print("[INFO] Start recording...")
            requests.get("http://192.168.1.153:5000/startListening")

        if (self.timeOut == MAX_FRAME_TO_PROCESS or self.COUNTER == MAX_FRAME_LESS_THAN_THRESHOLD and self.isRecording):
            print("[INFO] Reset values...")
            self.timeOut = 0 if self.timeOut == MAX_FRAME_TO_PROCESS else self.timeOut + 1
            self.COUNTER = 0 if self.timeOut == MAX_FRAME_LESS_THAN_THRESHOLD or rmsMicFront <= THRESHOLD else self.COUNTER + 1
            self.isRecording = False
            print("[INFO] Stop recording...")

            requests.get("http://192.168.1.153:5000/stopListening")
            time.sleep(1)
            textRecognized = requests.get("http://192.168.1.153:5000/getSpeech")

        elif self.isRecording: self.timeOut += 1

        print("RMS: " + str(rmsMicFront) + " COUNTER: " + str(self.COUNTER) + " TIMEOUT: " + str(self.timeOut) + " ISRECORDING: " + str(self.isRecording))

    def calcRMSLevel(self,data) :
        """
        Calculate RMS level
        """
        RMS = 100 * (np.sqrt(np.mean(np.square(data))))
        return RMS

    def convertStr2SignedInt(self, data) :
        """
        This function takes a string containing 16 bits little endian sound
        samples as input and returns a vector containing the 16 bits sound
        samples values converted between -1 and 1.
        """
        signedData=[]
        ind=0;
        for i in range (0,len(data)/2) :
            signedData.append(data[ind]+data[ind+1]*256)
            ind=ind+2

        for i in range (0,len(signedData)) :
            if signedData[i]>=32768 :
                signedData[i]=signedData[i]-65536

        for i in range (0,len(signedData)) :
            signedData[i]=signedData[i]/32768.0

        return signedData


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    try:
        # Initialize qi framework.
        connection_url = "tcp://" + args.ip + ":" + str(args.port)
        app = qi.Application(["SoundProcessingModule", "--qi-url=" + connection_url])
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    MySoundProcessingModule = SoundProcessingModule(app)
    app.session.registerService("SoundProcessingModule", MySoundProcessingModule)
    MySoundProcessingModule.startProcessing()