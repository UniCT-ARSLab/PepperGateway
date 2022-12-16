import qi
import time
import numpy
import cv2
# import speech_recognition
import gtts
import playsound
import subprocess
# import dance
import socket
import paramiko
from scp import SCPClient

class Pepper:
    """
    Crea un istanza del robot secondo il suo indirizzo IP e la sua porta.
    L'indirizzo IP può essere ottenuto premendo il bottone del petto del robot.
    Tipicamente la porta di default è uguale a `9559`.
    """
    def __init__(self, ip_address, port=9559):
        self.session = qi.Session()
        self.session.connect("tcp://" + ip_address + ":" + str(port))

        self.ip_address = ip_address
        self.port = port

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()
        ssh.connect(hostname=self.ip_address, username="nao", password="RoyRoy2009")
        self.scp = SCPClient(ssh.get_transport())

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

        # self.recognizer = speech_recognition.Recognizer()
        # self.set_language("Italian") To fix!!!

        # self.autonomous_life_on()

        print("[INFO]: Robot è inizializzato all'indirizzo " + ip_address + ", " + str(port))

    def point_at(self, x, y, z, effector_name, frame):
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
        speed = 0.5     # 50 % of speed
        self.tracker_service.pointAt(effector_name, [x, y, z], frame, speed)

    def stop_moving(self):
        """Stop robot from moving by `move_around` and `turn_around` methods"""
        self.motion_service.stopMove()

    def say(self, text):
        """
        Permette al robot di parlare pronunciando il testo (i.e. text) passato come parametro.

        :param text: Text to speech
        :type text: string
        """
        self.tts_service.say(text)
        print("[INFO]: Robot says: " + text)

    # def autonomous_life_off(self):
    #     """
    #     Switch autonomous life off

    #     .. note:: After switching off, robot stays in resting posture. After \
    #     turning autonomous life default posture is invoked
    #     """
    #     self.autonomous_life_service.setState("disabled")
    #     self.stand()
    #     print("[INFO]: Autonomous life is off")

    # def autonomous_life_on(self):
    #     """Switch autonomous life on"""
    #     self.autonomous_life_service.setState("interactive")

    #     print("[AUTONOMOUS LIFE]", self.autonomous_life_service.getState())
    #     print("[INFO]: Autonomous life is on")

    def show_map(self, on_robot=False, remote_ip=None):
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

        if on_robot:
            # TODO: It requires a HTTPS server running. This should be somehow automated.
            cv2.imwrite("./tmp/map.png", robot_map)
            self.tablet_show_web(remote_ip + ":8000/map.png")
            print("[INFO]: Map is available at: " + str(remote_ip) + ":8000/map.png")
        else:
            map_name = "map.png"
            cv2.imwrite(map_name, robot_map)
            cv2.imshow("RobotMap", robot_map)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def navigate_to(self, x, y, theta = 0):
        """
        Navigate robot in map based on exploration mode
        or load previously mapped enviroment.

        .. note:: Prima di effettuare una chiamata a questo metodo è necessario eseguire robot_localization()

        .. warning:: Si noti che la navigazione rispetto un punto bidimensionale
        è permessa se distante al più tre metri dal robot.

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

    @staticmethod
    def share_localhost(folder):
        """
        Shares a location on localhost via HTTPS to Pepper be
        able to reach it by subscribing to IP address of this
        computer.

        :Example:

        >>> pepper.share_localhost("/Users/pepper/Desktop/web/")

        :param folder: Root folder to share
        :type folder: string
        """
        # TODO: Add some elegant method to kill a port if previously opened
        subprocess.Popen(["cd", folder])
        try:
            subprocess.Popen(["python", "-m", "SimpleHTTPServer"])
        except Exception as error:
            subprocess.Popen(["python", "-m", "SimpleHTTPServer"])
        print("[INFO]: HTTPS server successfully started")

    def play_sound(self, sound):
        """
        Play a `mp3` or `wav` sound stored on Pepper

        .. note:: This is working only for songs stored in robot.

        :param sound: Absolute path to the sound
        :type sound: string
        """
        print("[INFO]: Playing " + sound)
        self.audio_service.playFile(sound)

    def stop_sound(self):
        """Stop sound"""
        print("[INFO]: Stop playing the sound")
        self.audio_service.stopAll()

    def start_behavior(self, behavior):
        """
        Starts a behavior stored on robot

        :param behavior: Behavior name
        :type behavior: string
        """
        self.behavior_service.startBehavior(behavior)

    def stop_behavior(self, behavior):
        """
        Stop a behavior stored on robot

        :param behavior: Behavior name
        :type behavior: string
        """
        self.behavior_service.stopBehavior(behavior)

    def stop_all_behavior(self):
        self.behavior_service.stopAllBehaviors()

    def list_behavior(self):
        """Prints all installed behaviors on the robot"""
        print(self.behavior_service.getBehaviorNames())

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