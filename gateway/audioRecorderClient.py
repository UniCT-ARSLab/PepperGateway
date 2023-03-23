import os
import socket
import wave
import time
import threading
import struct

SERVER_ADDRESS = ("192.168.1.153", 8008)

class audioRecorder:
    def __init__(self):
        self.COUNTER = 0
        print("[INFO] Setup socket...")
        self.setupSocket()
    
    def setupSocket(self):
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
            print("[INFO] Binding to port...")
            s.bind(SERVER_ADDRESS)
            print("[INFO] Listening for connections...")
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print('[INFO] Connected by', addr)
                    AUDIO_FILE = "record" + str(self.COUNTER) + ".wav"
                    with open(AUDIO_FILE, "wb") as f:
                        while True:
                            data = conn.recv(1024)
                            f.write(data)
                            if not data:
                                self.COUNTER += 1
                                conn.close()
                                break
                

if __name__ == "__main__":
    audioRecorder = audioRecorder()
