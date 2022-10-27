from robot import *
import config

pepper = Pepper(config.IP_ADDRESS, config.PORT)

pepper.stop_all_behavior()
pepper.clean_tablet()
pepper.autonomous_life_on()

pepper.set_security_distance(0.01)
#pepper.exploration_mode(15)
pepper.load_map(file_name="2014-04-04T041209.886Z.explo")
pepper.show_map(False)
pepper.robot_localization()
pepper.navigate_to(-1, -1)
pepper.show_map(False)