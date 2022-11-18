from robot import *
import config
import time

pepper = Pepper(config.IP_ADDRESS, config.PORT)

pepper.stop_all_behavior()
# pepper.clean_tablet()
pepper.autonomous_life_on()

# TODAY
pepper.set_security_distance(0.01)
print("Inizio a tracciare la mappa")
pepper.exploration_mode(2) # Robot return to Origin at the end of exploration
pepper.show_map()
# ---------------------------------------


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
    