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

        # It contains all saved point of interests
        self.point_of_interests = {}

        print("[INFO]: Robot is initialized at " + ip_address + ":" + str(port))
        self.set_security_distance(0.01)
        self.autonomous_life_service.setState("disabled")
        self.motion_service.wakeUp()
        # self.say("Il robot e' pronto")

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

    def move_forward(self, speed):
        """
        Move forward with certain speed

        :param speed: Positive values forward, negative backwards
        :type speed: float
        """
        self.motion_service.move(speed, 0, 0)

    def move_toward(self, x, y, theta):
        """
        Move forward with certain speed

        :param speed: Positive values forward, negative backwards
        :type speed: float
        """
        self.motion_service.moveToward(x, y, theta)

    def turn_around(self, speed):
        """
        Turn around its axis

        :param speed: Positive values to right, negative to left
        :type speed: float
        """
        self.motion_service.move(0, 0, speed)

    def stop_moving(self):
        """Stop robot from moving by `move_around` and `turn_around` methods"""
        self.motion_service.stopMove()

# ------------------------------------------

    # def start_stream(self):
    #     self.subscribe_camera(self.get_picked_camera(), 0, 30)
    #     #self.thread_alive = True
    #     while not self._stop_event.is_set():
    #         #print(self.thread_alive)
    #         if not self.stream_on == 1:
    #             self._stop_event.wait(1)
    #             continue
    #         image = self.robot.get_camera_frame(show=False)
    #         image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    #         image = cv2.resize(image, (320, 240))
    #         im = Image.fromarray(image)
    #         #name = "camera.jpg"
    #         #im.save(name)

    # def on_start_stream_clicked(self):
    #     self.output_text("[INFO]: Starting camera stream.")
    #     if self.stream_on == -1:
    #         self.stream_on = 1
    #         self.video_thread.start()
    #     else:
    #         self.stream_on = 1

    # def on_stop_stream_clicked(self):
    #     self.output_text("[INFO]: Stopping camera stream.")
    #     self.stream_on = 0

# ------------------------------------------

    def say(self, text):
        """
        Text to speech (robot internal engine)

        :param text: Text to speech
        :type text: string
        """
        self.tts_service.say(text)
        print("[INFO]: Robot says: " + text)

    def autonomous_life_off(self):
        """
        Switch autonomous life off

        .. note:: After switching off, robot stays in resting posture. After \
        turning autonomous life default posture is invoked
        """
        self.autonomous_life_service.setState("disabled")
        self.stand()
        print("[INFO]: Autonomous life is off")

    def autonomous_life_on(self):
        """Switch autonomous life on"""
        self.autonomous_life_service.setState("interactive")

        print("[AUTONOMOUS LIFE]", self.autonomous_life_service.getState())
        print("[INFO]: Autonomous life is on")

    def track_object(self, object_name, effector_name, diameter=0.05):
        """
        Track a object with a given object type and diameter. If `Face` is
        chosen it has a default parameters to 15 cm diameter per face. After
        staring tracking in will wait until user press ctrl+c.

        .. seealso:: For more info about tracking modes, object names and other:\
        http://doc.aldebaran.com/2-5/naoqi/trackers/index.html#tracking-modes

        :Example:

        >>> pepper.track_object("Face", "Arms")

        Or

        >>> pepper.track_object("RedBall", "LArm", diameter=0.1)

        :param object_name: `RedBall`, `Face`, `LandMark`, `LandMarks`, `People` or `Sound`
        :param effector_name: `LArm`, `RArm`, `Arms`
        :param diameter: Diameter of the object (default 0.05, for face default 0.15)
        """
        if object == "Face":
            self.tracker_service.registerTarget(object_name, 0.15)
        else:
            self.tracker_service.registerTarget(object_name, diameter)

        self.tracker_service.setMode("Move")
        self.tracker_service.track(object_name)
        self.tracker_service.setEffector(effector_name)

        self.say("Show me a " + object_name)
        print("[INFO]: Use Ctrl+c to stop tracking")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("[INFO]: Interrupted by user")
            self.say("Stopping to track a " + object_name)

        self.tracker_service.stopTracker()
        self.unsubscribe_effector()
        self.say("Let's do something else!")

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
            # self.tablet_show_web(remote_ip + ":8000/map.png")
            # print("[INFO]: Map is available at: " + str(remote_ip) + ":8000/map.png")
        else:
            map_name = "map.png"
            cv2.imwrite(map_name, robot_map)
            cv2.imshow("RobotMap", robot_map)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

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
        self.say("Starting exploration in " + str(radius) + " meters")
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

    def set_volume(self, volume):
        """
        Set robot volume in percentage

        :param volume: From 0 to 100 %
        :type volume: integer
        """
        self.audio_device.setOutputVolume(volume)
        self.say("Volume is set to " + str(volume) + " percent")

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

    def show_tablet_camera(self, text):
        """
        Show image from camera with SpeechToText annotation on the robot tablet

        .. note:: For showing image on robot you will need to share a location via HTTPS and \
        save the image to ./tmp.

        .. warning:: It has to be some camera subscribed and ./tmp folder in root directory \
        exists for showing it on the robot.

        :Example:

        >>> pepper = Pepper("10.37.1.227")
        >>> pepper.share_localhost("/Users/michael/Desktop/Pepper/tmp/")
        >>> pepper.subscribe_camera("camera_top", 2, 30)
        >>> while True:
        >>>     pepper.show_tablet_camera("camera top")
        >>>     pepper.tablet_show_web("http://10.37.2.241:8000/tmp/camera.png")

        :param text: Question of the visual question answering
        :type text: string
        """
        remote_ip = socket.gethostbyname(socket.gethostname())
        image_raw = self.camera_device.getImageRemote(self.camera_link)
        image = numpy.frombuffer(image_raw[6], numpy.uint8).reshape(image_raw[1], image_raw[0], 3)
        image = cv2.resize(image, (800, 600))
        cv2.putText(image, "Visual question answering", (30, 500), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.putText(image, "Question: " + text, (30, 550), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imwrite("./tmp/camera.png", image)

        self.tablet_show_web("http://" + remote_ip + ":8000/tmp/camera.png")

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

    def move_head_down(self):
        """Look down"""
        self.motion_service.setAngles("HeadPitch", 0.46, 0.2)

    def move_head_up(self):
        """Look up"""
        self.motion_service.setAngles("HeadPitch", -0.4, 0.2)

    def move_to_circle(self, clockwise, t=10):
        """
        Move a robot into circle for specified time

        .. note:: This example only count on time not finished circles.

        >>> pepper.move_to_circle(clockwise=True, t=5)

        :param clockwise: Specifies a direction to turn around
        :type clockwise: bool
        :param t: Time in seconds (default 10)
        :type t: float
        """
        if clockwise:
            self.motion_service.moveToward(0.5, 0.0, 0.6)
        else:
            self.motion_service.moveToward(0.5, 0.0, -0.6)
        time.sleep(t)
        self.motion_service.stopMove()

    def turn_off_leds(self):
        """Turn off the LEDs in robot's eyes"""
        self.blink_eyes([0, 0, 0])

    def unsubscribe_effector(self):
        """
        Unsubscribe a end-effector after tracking some object

        .. note:: It has to be done right after each tracking by hands.
        """
        self.tracker_service.unregisterAllTargets()
        self.tracker_service.setEffector("None")
        print("[INFO]: End-effector is unsubscribed")

    def pick_a_volunteer(self):
        """
        Complex movement for choosing a random people.

        If robot does not see any person it will automatically after several
        seconds turning in one direction and looking for a human. When it detects
        a face it will says 'I found a volunteer' and raise a hand toward
        her/him and move forward. Then it get's into a default 'StandInit'
        pose.

        :Example:

        >>> pepper.pick_a_volunteer()

        """
        volunteer_found = False
        self.unsubscribe_effector()
        self.stand()
        self.say("Ho bisogno di un volontario.")

        proxy_name = "FaceDetection" + str(numpy.random)

        print("[INFO]: Pick a volunteer mode started")

        while not volunteer_found:
            wait = numpy.random.randint(500, 1500) / 1000
            theta = numpy.random.randint(-10, 10)
            self.turn_around(theta)
            time.sleep(wait)
            self.stop_moving()
            self.stand()
            self.face_detection_service.subscribe(proxy_name, 500, 0.0)
            for memory in range(5):
                time.sleep(0.5)
                output = self.memory_service.getData("FaceDetected")
                print("...")
                if output and isinstance(output, list) and len(output) >= 2:
                    print("Face detected")
                    volunteer_found = True

        self.say("Ho trovato un volontario!")
        self.stand()
        try:
            self.tracker_service.registerTarget("Face", 0.15)
            self.tracker_service.setMode("Move")
            self.tracker_service.track("Face")
            self.tracker_service.setEffector("RArm")
            self.get_face_properties()
        
        except Exception as err:
            print("ERRORE VOLONTARIO: ", err)

        finally:
            time.sleep(2)
            self.unsubscribe_effector()
            self.stand()
            self.face_detection_service.unsubscribe(proxy_name)

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

    def start_animation(self, animation):
        """
        Starts a animation which is stored on robot

        .. seealso:: Take a look a the animation names in the robot \
        http://doc.aldebaran.com/2-5/naoqi/motion/alanimationplayer.html#alanimationplayer

        :param animation: Animation name
        :type animation: string
        :return: True when animation has finished
        :rtype: bool
        """
        try:
            animation_finished = self.animation_service.run("animations/[posture]/Gestures/" + animation, _async=True)
            animation_finished.value()
            return True
        except Exception as error:
            print(error)
            return False

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

    def get_face_properties(self):
        """
        Gets all face properties from the tracked face in front of
        the robot.

        It tracks:
        - Emotions (neutral, happy, surprised, angry and sad
        - Age
        - Gender

        .. note:: It also have a feature that it substracts a 5 year if it talks to a female.

        .. note:: If it cannot decide which gender the user is, it just greets her/him as "Hello human being"

        ..warning:: To get this feature working `ALAutonomousLife` process is needed. In this methods it is \
        called by default
        """
        self.autonomous_life_on()
        emotions = ["neutral", "happy", "surprised", "angry", "sad"]
        face_id = self.memory_service.getData("PeoplePerception/PeopleList")
        recognized = None
        try:
            recognized = self.face_characteristic.analyzeFaceCharacteristics(face_id[0])
        except Exception as error:
            print("[ERROR]: Cannot find a face to analyze.")
            self.say("I cannot recognize a face.")

        if recognized:
            properties = self.memory_service.getData("PeoplePerception/Person/" + str(face_id[0]) + "/ExpressionProperties")
            gender = self.memory_service.getData("PeoplePerception/Person/" + str(face_id[0]) + "/GenderProperties")
            age = self.memory_service.getData("PeoplePerception/Person/" + str(face_id[0]) + "/AgeProperties")

            # Gender properties
            if gender[1] > 0.4:
                if gender[0] == 0:
                    self.say("Hello lady!")
                elif gender[0] == 1:
                    self.say("Hello sir!")
            else:
                self.say("Hello human being!")

            # Age properties
            if gender[1] == 1:
                self.say("You are " + str(int(age[0])) + " years old.")
            else:
                self.say("You look like " + str(int(age[0])) + " oops, I mean " + str(int(age[0]-5)))

            # Emotion properties
            emotion_index = (properties.index(max(properties)))

            if emotion_index > 0.5:
                self.say("I am quite sure your mood is " + emotions[emotion_index])
            else:
                self.say("I guess your mood is " + emotions[emotion_index])

    def listen_to(self, vocabulary):
        """
        Listen and match the vocabulary which is passed as parameter.

        :Example:

        >>> words = pepper.listen_to(["what color is the sky", "yes", "no"]

        :param vocabulary: List of phrases or words to recognize
        :type vocabulary: string
        :return: Recognized phrase or words
        :rtype: string
        """
        
        self.set_language("Italian")
        self.speech_service.pause(True)
        try:
            self.speech_service.setVocabulary(vocabulary, True)
        except RuntimeError as error:
            print(error)
            self.speech_service.removeAllContext()
            self.speech_service.setVocabulary(vocabulary, True)
            self.speech_service.subscribe("Test_ASR")
        try:
            print("[INFO]: Robot is listening to you...")
            self.speech_service.pause(False)
            time.sleep(4)
            words = self.memory_service.getData("WordRecognized")
            print("[INFO]: Robot understood: '" + words[0] + "'")
            return words[0]
        except:
            pass

    def listen(self):
        """
        Wildcard speech recognition via internal Pepper engine

        .. warning:: To get this proper working it is needed to disable or uninstall \
        all application which can modify a vocabulary in a Pepper.

        .. note:: Note this version only rely on time but not its internal speak processing \
        this means that Pepper will 'bip' at the begining and the end of human speak \
        but it is not taken a sound in between the beeps. Search for 'Robot is listening to \
        you ... sentence in log console

        :Example:

        >>> words = pepper.listen()

        :return: Speech to text
        :rtype: string
        """
        self.speech_service.setAudioExpression(False)
        self.speech_service.setVisualExpression(False)
        self.audio_recorder.stopMicrophonesRecording()
        print("[INFO]: Speech recognition is in progress. Say something.")
        while True:
            print(self.memory_service.getData("ALSpeechRecognition/Status"))
            if self.memory_service.getData("ALSpeechRecognition/Status") == "SpeechDetected":
                self.audio_recorder.startMicrophonesRecording("/home/nao/speech.wav", "wav", 48000, (0, 0, 1, 0))
                print("[INFO]: Robot is listening to you")
                self.blink_eyes([255, 0, 0])
                break

        while True:
            if self.memory_service.getData("ALSpeechRecognition/Status") == "EndOfProcess":
                self.audio_recorder.stopMicrophonesRecording()
                print("[INFO]: Robot is not listening to you")
                self.blink_eyes([0, 0, 255])
                break

        self.download_file("speech.wav")
        self.speech_service.setAudioExpression(True)
        self.speech_service.setVisualExpression(True)

        return self.speech_to_text("speech.wav")

    def ask_wikipedia(self):
        """
        Ask for question and then robot will say first two sentences from Wikipedia

        ..warning:: Autonomous life has to be turned on to process audio
        """
        #self.self.autonomous_life_on()
        self.speech_service.setAudioExpression(False)
        self.speech_service.setVisualExpression(False)
        self.set_awareness(False)
        self.say("Fammi una domanda")
        question = self.listen()
        self.say("I will tell you")
        answer = tools.get_knowledge(question)
        self.say(answer)
        self.set_awareness(True)
        self.speech_service.setAudioExpression(True)
        self.speech_service.setVisualExpression(True)

    def rename_robot(self):
        """Change current name of the robot"""
        choice = raw_input("Are you sure you would like to rename a robot? (yes/no)\n")
        if choice == "yes":
            new_name = raw_input("Enter a new name for the robot. Then it will reboot itself.\nName: ")
            self.system_service.setRobotName(new_name)
            self.restart_robot()

    def upload_file(self, file_name):
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
        self.scp.get(file_name, local_path="/tmp/")
        print("[INFO]: File " + file_name + " downloaded")
        self.scp.close()

    # def speech_to_text(self, audio_file):
    #     """
    #     Translate speech to text via Google Speech API

    #     :param audio_file: Name of the audio (default `speech.wav`
    #     :type audio_file: string
    #     :return: Text of the speech
    #     :rtype: string
    #     """
    #     audio_file = speech_recognition.AudioFile("/tmp/" + audio_file)
    #     with audio_file as source:
    #         audio = self.recognizer.record(source)
    #         recognized = self.recognizer.recognize_google(audio, language="it_IT")
    #     return recognized

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

    def hand(self, hand, close):
        """
        Close or open hand

        :param hand: Which hand
            - left
            - right
        :type hand: string
        :param close: True if close, false if open
        :type close: boolean
        """
        hand_id = None
        if hand == "left":
            hand_id = "LHand"
        elif hand == "right":
            hand_id = "RHand"

        if hand_id:
            if close:
                self.motion_service.setAngles(hand_id, 0.0, 0.2)
                print("[INFO]: Hand " + hand + "is closed")
            else:
                self.motion_service.setAngles(hand_id, 1.0, 0.2)
                print("[INFO]: Hand " + hand + "is opened")
        else:
            print("[INFO]: Cannot move a hand")

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

    # @staticmethod
    # def listen():
    #     """Speech to text by Google Speech Recognition"""
    #     recognizer = speech_recognition.Recognizer()
    #     with speech_recognition.Microphone() as source:
    #         print("[INFO]: Say something...")
    #         audio = recognizer.listen(source)
    #         speech = recognizer.recognize_google(audio, language="it-IT")

    #         return speech