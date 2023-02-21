from WebServer import *
from robot import *
import config
import time
from gevent import pywsgi



if __name__ == "__main__":
	pepper = Pepper(config.IP_ADDRESS, config.PORT)
	webServer = WebServer(pepper)
	# webServer = WebServer()
