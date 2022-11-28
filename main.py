from robot import *
import config
import time

pepper = Pepper(config.IP_ADDRESS, config.PORT)

pepper.stop_all_behavior()
# pepper.clean_tablet()
pepper.autonomous_life_on()
pepper.start_behavior("miry-01/behavior_1")
pepper.list_behavior()
# pepper.share_localhost("/Users/giuseppepitruzzella/PepperGateway/images/")
# while True:
#     pepper.show_tablet_camera("camera top")
#     pepper.tablet_show_web("http://192.168.1.20:8000/logo.png")

# # Set security distance (lower distance for passing doors)
# pepper.set_security_distance(0.01)
# print("[+] Starting exploration mode...")
# pepper.exploration_mode(5) # N.B. Robot return to Origin at the end of exploration
# pepper.show_map() # show_map() open saved map in a new window using OpenCV

"""
# 1
pepper.set_security_distance(0.01)
print("[INFO] Loading SLAM Map...")
pepper.say("Carico la mappa")
pepper.load_map("2014-04-04T012659.586Z.explo")
# 2

pepper.say("Salvo il punto di interesse");
# Save current position
pose = pepper._robot_localization("endpoint") # Rename _robot_localization to set_point_of_interest(self, name)
# Navigate in O
pepper.navigate_to(0.2, 0.2)
# Navigate in map to point of interest called "endpoint"
pepper.say("Navigo verso il punto di interesse")
pepper.navigate_to(
    pepper.point_of_interests["endpoint"][0],
    pepper.point_of_interests["endpoint"][1]) 
"""