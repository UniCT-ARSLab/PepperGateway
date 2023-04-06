# -*- coding: UTF-8 -*-
import qi
import time
import numpy
import cv2
import speech_recognition
import gtts
import playsound
import subprocess
import socket
import paramiko
from scp import SCPClient
from GPT import *
import threading
import config
import subprocess
import os
import requests
import json
import functools

AUDIO_TRACK_DURATION = 4
DEFAULT_AUDIO_FILE_NAME = "speech.wav"

class Pepper:
    """
    **Real robot controller**

    Create an instance of real robot controller by specifying
    a robot's IP address and port. IP address can be:

    - hostname (hostname like `pepper.local`)
    - IP address (can be obtained by pressing robot's *chest button*)

    Default port is usually used, e.g. `9559`.

    :Example:

    >>> pepper = Pepper("pepper.local")
    >>> pepper = Pepper("192.169.0.1", 1234)

    """
    def __init__(self, ip_address, port=9559, GPT = None):
        # Connection to Pepper Robot
        self.session = qi.Session()
        self.session.connect("tcp://" + ip_address + ":" + str(port))

        # Setting Up IP ADDRESS and PORT for Pepper
        self.ip_address = ip_address
        self.port = port

        # Setting Up SSH Connection
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.load_system_host_keys()
        self.ssh.connect(hostname=self.ip_address, username=config.USERNAME, password=config.PASSWORD)
        self.scp = SCPClient(self.ssh.get_transport())

        # Setting Up Services
        self.posture_service = self.session.service("ALRobotPosture")
        self.motion_service = self.session.service("ALMotion")
        self.tracker_service = self.session.service("ALTracker")
        self.tts_service = self.session.service("ALAnimatedSpeech")
        self.tablet_service = self.session.service("ALTabletService")
        self.autonomous_life_service = self.session.service("ALAutonomousLife")
        self.system_service = self.session.service("ALSystem")
        self.navigation_service = self.session.service("ALNavigation")
        self.battery_service = self.session.service("ALBattery")
        self.awareness_service = self.session.service("ALBasicAwareness")
        self.led_service = self.session.service("ALLeds")
        self.audio_device = self.session.service("ALAudioDevice")
        self.camera_device = self.session.service("ALVideoDevice")
        self.face_detection_service = self.session.service("ALFaceDetection")
        self.memory_service = self.session.service("ALMemory")
        self.audio_service = self.session.service("ALAudioPlayer")
        self.animation_service = self.session.service("ALAnimationPlayer")
        self.behavior_service = self.session.service("ALBehaviorManager")
        self.face_characteristic = self.session.service("ALFaceCharacteristics")
        self.people_perception = self.session.service("ALPeoplePerception")
        self.speech_service = self.session.service("ALSpeechRecognition")
        self.dialog_service = self.session.service("ALDialog")
        self.audio_recorder = self.session.service("ALAudioRecorder")
        self.slam_map = None
        self.localization = None
        self.camera_link = None
        self.recognizer = speech_recognition.Recognizer()
        self.point_of_interests = {}
        self.set_security_distance(0.5)
        self.autonomousLifeState = True # Init Autonomous Life State
        self.PID = None
        self.setAutonomousLife(True)
        self.setupTouch() # Setup React to Touch Event

        self.GPT = GPT # Use this istance of GPT to handle vocal messages
        self.uploadOnRobot("liveListening.py")

        print("[INFO]: Robot is initialized at " + ip_address + ":" + str(port))

    def liveListening(self, isOpen = False):
        if not isOpen:
            stdin, stdout, stderr = self.ssh.exec_command('python /home/nao/liveListening.py')
        else: self.ssh.exec_command(chr(3))

    def getAnswer(self, message):
        return self.say(self.GPT.getAnswer(message))

    def setupTouch(self):
        self.touch = self.memory_service.subscriber("TouchChanged")
        self.id = self.touch.signal.connect(functools.partial(self.onTouched, "TouchChanged"))

    def onTouched(self, strVarName, bodyValues):
        # Disconnect to the event when talking, to avoid repetitions
        self.touch.signal.disconnect(self.id)
        touchedBodies = []
        for partValues in bodyValues:
            if partValues[0] == "Head": 
                if partValues[1]: # If touched
                    self.startMicrophone()
                else: # If released
                    self.stopMicrophone()
                    self.getAnswer(self.speechToText(DEFAULT_AUDIO_FILE_NAME))
            touchedBodies.append(partValues[0])
        # Reconnect again to the event
        self.id = self.touch.signal.connect(functools.partial(self.onTouched, "TouchChanged"))

    def startMicrophone(self):
        self.speech_service.setAudioExpression(False) # Disable audio expression
        self.speech_service.setVisualExpression(False) # Disable visual expression
        self.audio_recorder.stopMicrophonesRecording() # Stop any previous recording
        self.audio_recorder.startMicrophonesRecording("/home/nao/speech.wav", "wav", 48000, (0, 0, 1, 0))
        return "[INFO] Starting Microphone..."
    
    def stopMicrophone(self, download = True):
        self.audio_recorder.stopMicrophonesRecording()
        if download: self.download_file("speech.wav") # look at this!!!
        self.speech_service.setAudioExpression(True)
        self.speech_service.setVisualExpression(True)
        return "[INFO] Stopping Microphone..."
    
    def speechToText(self, audio_file = "speech.wav", getAnswer = False):
        audio_file = speech_recognition.AudioFile("tmp/" + audio_file)
        with audio_file as source:
            audio = self.recognizer.record(source)
            recognized = self.recognizer.recognize_google(audio, language="it-IT", show_all=True)
        if recognized:
            recognizedText = recognized["alternative"][0]["transcript"]
            print("[INFO] Google Speech Recognition : " + recognizedText)
            if getAnswer: return self.getAnswer(recognizedText)
        else: recognizedText = "[ERROR]"
        return recognizedText
    
    def setLiveListening(self, isOpen = False):
        if not isOpen:
            self.setAutonomousLife(False)
            CMD ="python /home/nao/liveListening.py & echo $!"
            stdin, stdout, stderr = self.ssh.exec_command(CMD)
            self.PID = stdout.readline()
            print("[START] PID: " + self.PID)
        else:
            print("[KILL] PID: " + self.PID)
            stdin, stdout, stderr = self.ssh.exec_command("kill " + self.PID)

    def videoStream(self, isOpen = False):
        if not isOpen:
            self.setAutonomousLife(False)
            CMD ="gst-launch-0.10 -v v4l2src device=/dev/video0 ! video/x-raw-yuv,width=640,height=480,framerate=30/1 ! ffmpegcolorspace ! jpegenc ! multipartmux! tcpserversink port=3000"
            stdin, stdout, stderr = self.ssh.exec_command(CMD)
        else: 
            stdin, stdout, stderr = self.ssh.exec_command("ps ax | grep corrado.py")
            print(stdout)
        # os.system("vlc tcp://192.168.1.20:3000")


    def pointAt(self, x, y, z, effector_name, frame):
        """
        Point end-effector in cartesian space

        :Example:

        >>> pepper.point_at(1.0, 1.0, 0.0, "RArm", 0)

        :param x: X axis in meters
        :type x: float
        :param y: Y axis in meters
        :type y: float
        :param z: Z axis in meters
        :type z: float
        :param effector_name: `LArm`, `RArm` or `Arms`
        :type effector_name: string
        :param frame: 0 = Torso, 1 = World, 2 = Robot
        :type frame: integer
        """
        speed = 0.1     # 50 % of speed
        self.tracker_service.pointAt(effector_name, [x, y, z], frame, speed)

    def move_toward(self, x, y, theta):
        """
        Move toward to certain direction

        :param x: X axis in meters
        :param y: Y axis in meters
        :param theta: Rotation around Z axis in radians
        :type x: float
        :type y: float
        :type theta: float
        """
        self.motion_service.moveToward(x, y, theta)

    def turn_around(self, speed):
        """
        Turn around its axis

        :param speed: Positive values to right, negative to left
        :type speed: float
        """
        self.motion_service.move(0, 0, speed)

    def say(self, text):
        """
        Text to speech (robot internal engine)

        :param text: Text to speech
        :type text: string
        """
        self.tts_service.say(text)
        print("[INFO]: Robot says: " + text)
        return text

    def getAutonomousLife(self):
        return self.autonomousLifeState

    def setAutonomousLife(self, STATE):
        """
        Set autonomous life on or off

        .. note:: After switching off, robot stays in resting posture. After \
        turning autonomous life default posture is invoked
        """
        if STATE:
            self.autonomous_life_service.setState("interactive")
            self.autonomousLifeState = True
        else:
            self.autonomous_life_service.setState("disabled")
            self.motion_service.wakeUp()
            self.autonomousLifeState = False
        print("[AUTONOMOUS LIFE]", self.autonomous_life_service.getState())
        return "Autonomous Life is " + self.autonomous_life_service.getState()
    
    def getAutonomousLife(self):
        print("[AUTONOMOUS] " + str(self.autonomousLifeState))
        return str(self.autonomousLifeState)

    def save_map(self):
        """
        Shows a map from robot based on previously loaded one
        or explicit exploration of the scene. It can be viewed on
        the robot or in the computer by OpenCV.

        :param on_robot: If set shows a map on the robot
        :type on_robot: bool
        :param remote_ip: IP address of remote (default None)
        :type remote_ip: string

        .. warning:: Showing map on the robot is not fully supported at the moment.
        """
        result_map = self.navigation_service.getMetricalMap()
        map_width = result_map[1]
        map_height = result_map[2]
        img = numpy.array(result_map[4]).reshape(map_width, map_height)
        img = (100 - img) * 2.55  # from 0..100 to 255..0
        img = numpy.array(img, numpy.uint8)

        resolution = result_map[0]

        self.robot_localization()

        offset_x = result_map[3][0]
        offset_y = result_map[3][1]
        x = self.localization[0]
        y = self.localization[1]

        goal_x = (x - offset_x) / resolution
        goal_y = -1 * (y - offset_y) / resolution

        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        cv2.circle(img, (int(goal_x), int(goal_y)), 3, (0, 0, 255), -1)

        robot_map = cv2.resize(img, None, fx=1, fy=1, interpolation=cv2.INTER_CUBIC)

        print("[INFO]: Showing the map")
        cv2.imwrite("./static/img/latest_map.png", robot_map)

    def move_forward(self, speed):
        """
        Move forward with certain speed
        :param speed: Positive values forward, negative backwards
        :type speed: float
        """
        self.motion_service.move(speed, 0, 0)

    def turn_around(self, speed):
        """
        Turn around its axis
        :param speed: Positive values to right, negative to left
        :type speed: float
        """
        self.motion_service.move(0, 0, speed)

    def setup_point(self, name):
        """
        Setup point of interest in a map.
        Any saved point can be reached by the robot 
        through its name (e.g. navigato_to(name[0], name[1]))

        .. note:: If the point to be reached is too far away, 
        it may be useful to include intermediate points

        :param name: Key of key:value pair in point_of_interest dictionary
        :type name: string
        :return: [x, y, theta]
        :rtype: list

        :Example:

        >>> pepper._robot_localization("endpoint")
        >>> pepper.navigate_to(
            pepper.point_of_interests["endpoint"][0],
            pepper.point_of_interests["endpoint"][1]) 
        """
        
        try:
            self.navigation_service.startLocalization()
            localization = self.navigation_service.getRobotPositionInMap() # Returns an ALValue containing a Localized Pose.
            self.point_of_interests[name] = localization[0] # localization[0] should be equals to [x, y, Theta]
            print("[INFO]: Localization complete")
            self.navigation_service.stopLocalization()
        except Exception as error:
            print(error)
            print("[ERROR]: Localization failed")
        return self.point_of_interests[name]

    def navigate_to(self, x, y, theta = 0):
        """
        Navigate robot in map based on exploration mode
        or load previously mapped enviroment.

        .. note:: Before navigation you have to run localization of the robot.

        .. warning:: Navigation to 2D point work only up to 3 meters from robot.

        :Example:

        >>> pepper.robot_localization()
        >>> pepper.navigate_to(1.0, 0.3)

        :param x: X axis in meters
        :type x: float
        :param y: Y axis in meters
        :type y: float
        :param theta: Theta angle in meters
        :type theta: float
        """
        print("[INFO]: Trying to navigate into specified location")
        try:
            self.navigation_service.startLocalization()
            self.navigation_service.navigateToInMap([x, y, theta])
            self.navigation_service.stopLocalization()
            print("[INFO]: Successfully got into location")
            self.say("At your command")
        except Exception as error:
            print(error)
            print("[ERROR]: Failed to got into location")
            self.say("I cannot move in that direction")

    def robot_localization(self):
        """
        Localize a robot in a map

        .. note:: After loading a map into robot or after new exploration \
        robots always need to run a self localization. Even some movement in \
        cartesian space demands localization.
        """
        # TODO: There should be localizeInMap() with proper coordinates
        try:
            self.navigation_service.startLocalization()
            localization = self.navigation_service.getRobotPositionInMap() # Returns an ALValue containing a Localized Pose.
            self.localization = localization[0]
            print("[INFO]: Localization complete")
            self.navigation_service.stopLocalization()
        except Exception as error:
            print(error)
            print("[ERROR]: Localization failed")

    def stop_localization(self):
        """Stop localization of the robot"""
        self.navigation_service.stopLocalization()
        print("[INFO]: Localization stopped")
    
    def exploration_mode(self, radius):
        """
        Start exploration mode when robot it performing a SLAM
        in specified radius. Then it saves a map into robot into
        its default folder.
        .. seealso:: When robot would not move maybe it only needs \
        to set smaller safety margins. Take a look and `set_security_distance()`
        .. note:: Default folder for saving maps on the robot is: \
        `/home/nao/.local/share/Explorer/`
        :param radius: Distance in meters
        :type radius: integer
        :return: image
        :rtype: cv2 image
        """
        print("Starting exploration")
        self.navigation_service.explore(radius)
        map_file = self.navigation_service.saveExploration()

        print("[INFO]: Map file stored: " + map_file)

        self.navigation_service.startLocalization()
        self.navigation_service.navigateToInMap([0., 0., 0.])
        self.navigation_service.stopLocalization()

        # Retrieve and display the map built by the robot
        result_map = self.navigation_service.getMetricalMap()
        map_width = result_map[1]
        map_height = result_map[2]
        img = numpy.array(result_map[4]).reshape(map_width, map_height)
        img = (100 - img) * 2.55  # from 0..100 to 255..0
        img = numpy.array(img, numpy.uint8)

        self.slam_map = img
        return img

    def load_map(self, file_name, file_path="/home/nao/.local/share/Explorer/"):
        """
        Load stored map on a robot. It will find a map in default location,
        in other cases alternative path can be specifies by `file_name`.

        .. note:: Default path of stored maps is `/home/nao/.local/share/Explorer/`

        .. warning:: If file path is specified it is needed to have `\` at the end.

        :param file_name: Name of the map
        :type file_name: string
        :param file_path: Path to the map
        :type file_path: string
        """
        self.slam_map = self.navigation_service.loadExploration(file_path + file_name)
        print("[INFO]: Map '" + file_name + "' loaded")

    def delete_map(self, file_name, file_path="/home/nao/.local/share/Explorer/"):
        """
        Delete stored map on a robot. It will find a map in default location,
        in other cases alternative path can be specifies by `file_name`.

        .. note:: Default path of stored maps is `/home/nao/.local/share/Explorer/`

        .. warning:: If file path is specified it is needed to have `\` at the end.

        :param file_name: Name of the map
        :type file_name: string
        :param file_path: Path to the map
        :type file_path: string
        """
        self.ssh.exec_command('rm ' + file_path + file_name)
        print("[INFO]: Map '" + file_name + "' deleted")
    
    # def set_volume(self, volume):
    #     """
    #     Set robot volume in percentage

    #     :param volume: From 0 to 100 %
    #     :type volume: integer
    #     """
    #     self.audio_device.setOutputVolume(volume)
    #     self.say("Volume is set to " + str(volume) + " percent")

    def battery_status(self):
        """Say a battery status"""
        battery = self.battery_service.getBatteryCharge()
        # self.say("I have " + str(battery) + " percent of battery")
        return str(battery)

    def set_awareness(self, state):
        """
        Turn on or off the basic awareness of the robot,
        e.g. looking for humans, self movements etc.

        :param state: If True set on, if False set off
        :type state: bool
        """
        if state:
            self.awareness_service.resumeAwareness()
            print("[INFO]: Awareness is turned on")
        else:
            self.awareness_service.pauseAwareness()
            print("[INFO]: Awareness is paused")

    def subscribe_camera(self, camera, resolution, fps):
        """
        Subscribe to a camera service. You need to subscribe a camera
        before you reach a images from it. If you choose `depth_camera`
        only 320x240 resolution is enabled.

        .. warning:: Each subscription has to have a unique name \
        otherwise it will conflict it and you will not be able to \
        get any images due to return value None from stream.

        :Example:

        >>> pepper.subscribe_camera(0, 1, 15)
        >>> image = pepper.get_camera_frame(False)
        >>> pepper.unsubscribe_camera()

        :param camera: `camera_depth`, `camera_top` or `camera_bottom`
        :type camera: string
        :param resolution:
            0. 160x120
            1. 320x240
            2. 640x480
            3. 1280x960
        :type resolution: integer
        :param fps: Frames per sec (5, 10, 15 or 30)
        :type fps: integer
        """
        color_space = 13

        camera_index = None
        if camera == "camera_top":
            camera_index = 0
        elif camera == "camera_bottom":
            camera_index = 1
        elif camera == "camera_depth":
            camera_index = 2
            resolution = 1
            color_space = 11

        self.camera_link = self.camera_device.subscribeCamera("Camera_Stream" + str(numpy.random.random()),
                                                              camera_index, resolution, color_space, fps)
        if self.camera_link:
            print("[INFO]: Camera is initialized")
        else:
            print("[ERROR]: Camera is not initialized properly")

    def unsubscribe_camera(self):
        """Unsubscribe to camera after you don't need it"""
        self.camera_device.unsubscribe(self.camera_link)
        print("[INFO]: Camera was unsubscribed")

    def get_camera_frame(self, show):
        """
        Get camera frame from subscribed camera link.

        .. warning:: Please subscribe to camera before getting a camera frame. After \
        you don't need it unsubscribe it.

        :param show: Show image when recieved and wait for `ESC`
        :type show: bool
        :return: image
        :rtype: cv2 image
        """
        image_raw = self.camera_device.getImageRemote(self.camera_link)
        image = numpy.frombuffer(image_raw[6], numpy.uint8).reshape(image_raw[1], image_raw[0], 3)

        if show:
            cv2.imshow("Pepper Camera", image)
            cv2.waitKey(-1)
            cv2.destroyAllWindows()

        return image

    def get_depth_frame(self, show):
        """
        Get depth frame from subscribed camera link.

        .. warning:: Please subscribe to camera before getting a camera frame. After \
        you don't need it unsubscribe it.

        :param show: Show image when recieved and wait for `ESC`
        :type show: bool
        :return: image
        :rtype: cv2 image
        """
        image_raw = self.camera_device.getImageRemote(self.camera_link)
        image = numpy.frombuffer(image_raw[6], numpy.uint8).reshape(image_raw[1], image_raw[0], 3)

        if show:
            cv2.imshow("Pepper Camera", image)
            cv2.waitKey(-1)
            cv2.destroyAllWindows()

        return image

    def set_security_distance(self, distance=0.05):
        """
        Set security distance. Lower distance for passing doors etc.

        .. warning:: It is not wise to turn `security distance` off.\
        Robot may fall from stairs or bump into any fragile objects.

        :Example:

        >>> pepper.set_security_distance(0.01)

        :param distance: Distance from the objects in meters
        :type distance: float
        """
        self.motion_service.setOrthogonalSecurityDistance(distance)
        print("[INFO]: Security distance set to " + str(distance) + " m")

    def turn_off_leds(self):
        """Turn off the LEDs in robot's eyes"""
        self.blink_eyes([0, 0, 0])
    
    # SSH Modules
    def uploadOnRobot(self, file_name):
        """
        Upload file to the home directory of the robot

        :param file_name: File name with extension (or path)
        :type file_name: string
        """
        self.scp.put(file_name)
        print("[INFO]: File " + file_name + " uploaded")
        self.scp.close()

    def download_file(self, file_name):
        """
        Download a file from robot to ./tmp folder in root.

        ..warning:: Folder ./tmp has to exist!
        :param file_name: File name with extension (or path)
        :type file_name: string
        """
        self.scp.get(file_name, local_path="tmp/" + file_name)
        print("[INFO]: File " + file_name + " downloaded")
        self.scp.close()

    def get_maps(self, path = "/home/nao/.local/share/Explorer/"):
        """
        Get all maps from robot.

        :param path: Path to the map folder
        :type path: string
        """
        stdin, stdout, stderr = self.ssh.exec_command('ls /home/nao/.local/share/Explorer/')
        all_maps = stdout.readlines()
        all_maps = [map.replace("\n", "") for map in all_maps]
        return all_maps

    def get_robot_name(self):
        """
        Gets a current name of the robot

        :return: Name of the robot
        :rtype: string
        """
        name = self.system_service.robotName()
        if name:
            self.say("Il mio nome e' " + name)
        return name
    
    def resetRecognition():
        self.speech_service.unsubscribe("ASR_Engine")
        self.speech_service.subscribe("ASR_Engine")
        
        # if ALS==False:
        #     reset()
    
    def recognize_keyword(self, keyword):
        """
        Recognize a keyword from the vocabulary

        :param keyword: Keyword to recognize
        :type keyword: string
        :return: True if keyword is recognized, False otherwise
        :rtype: boolean
        """
        # Configurazione delle parole chiave da riconoscere
        # vocabulary = ["Hello"]
        # speech_recognition.setVocabulary(vocabulary, False)
        self.set_awareness(True)
        

        ALS = self.memory_service.getData("ALSpeechRecognition/ActiveListening")
        print("Active Listening before: " + str(ALS))

        self.speech_service.pause(True)
        self.speech_service.setLanguage("English")
        self.speech_service.setLanguage("Italian")
        self.speech_service.setVocabulary([keyword], True)
        self.speech_service.subscribe("Test_ASR")
        # speech_recognition.onWordRecognized.connect(on_word_recognized)

        ALS = self.memory_service.getData("ALSpeechRecognition/ActiveListening")
        print("Active Listening after: " + str(ALS))

        print("[INFO]: Robot is listening to you...")
        time.sleep(4)
        words = self.memory_service.getData("WordRecognized")
        for w in words: print(w)
        word_recognized = ''.join(e for e in words[0] if e.isalnum())

        ALS = self.memory_service.getData("ALSpeechRecognition/ActiveListening")
        print(ALS)

        print("[INFO]: Robot understood: '" + word_recognized + "'")
        if word_recognized == keyword:
            self.say("Ho capito la parola chiave " + word_recognized)
        self.speech_service.pause(False)
        self.speech_service.unsubscribe("Test_ASR")

class VirtualPepper:
    """Virtual robot for testing"""

    def __init__(self):
        """Constructor of virtual robot"""
        print("[INFO]: Using virtual robot!")

    @staticmethod
    def say(text):
        """
        Say some text trough text to speech

        :param text: Text to speech
        :type text: string
        """
        tts = gtts.gTTS(text, lang="en")
        tts.save("./tmp_speech.mp3")
        playsound.playsound("./tmp_speech.mp3")

    @staticmethod
    def listen():
        """Speech to text by Google Speech Recognition"""
        recognizer = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            print("[INFO]: Say something...")
            audio = recognizer.listen(source)
            speech = recognizer.recognize_google(audio, language="it-IT")
