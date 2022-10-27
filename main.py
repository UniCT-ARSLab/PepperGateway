from robot import *
import config

pepper = Pepper(config.IP_ADDRESS, config.PORT)



# pepper.track_object("Face", "Arms") It works
# while True:
#     pepper.show_tablet_camera("camera top")
#pepper.stop_behavior("System/boot-config")
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

# while True:
#     pepper.say("Give me a question")
#     try:
#         pepper.ask_wikipedia()
#     except Exception as error:
#         print(error)
#         pepper.say("I am not sure what to say")
