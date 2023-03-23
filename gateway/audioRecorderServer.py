import os
import socket
import wave
import time
import threading

LOCALIP = "192.168.1.20"
LOCALPORT = 8009
REMOTEIP = "192.168.1.153"
REMOTEPORT = 8008

class audioRecorder:
    def __init__(self, audioFile, duration):
        self.COUNTER = 0  

    def audioRecorder(self, audioFile, duration = 5):
        os.system('arecord  -d ' + str(duration) + ' -f cd -t wav -r 44100 ' + audioFile)

    def toClient(self, audioFile):
        self.TCPSenderSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        # self.TCPSenderSocket.bind((LOCALIP, LOCALPORT))
        # self.TCPSenderSocket.listen(1)
        self.TCPSenderSocket.connect((REMOTEIP, REMOTEPORT))
        with open(audioFile, "rb") as f:
            self.TCPSenderSocket.send(f.read())
        os.system("rm " + audioFile)
        self.TCPSenderSocket.close()

    def run(self):
        while True:
            try:
                AUDIO_FILE = "record" + str(self.COUNTER) + ".wav"
                self.audioRecorder(AUDIO_FILE)
                audioThread = threading.Thread(target=self.toClient, args=[AUDIO_FILE])
                audioThread.daemon = True
                audioThread.start()
                # self.toClient(AUDIO_FILE)
                self.COUNTER += 1
            except KeyboardInterrupt:
                print("KeyboardInterrupt")
                self.TCPSenderSocket.close()
                break

if __name__ == "__main__":
    audioFile = "record.wav"
    duration = 10
    audioRecorder = audioRecorder(audioFile, duration)
    audioRecorder.run()
