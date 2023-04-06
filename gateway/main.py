from WebServer import *
from robot import *
import config
import time
from gevent import pywsgi
import requests

if __name__ == "__main__":
	# GPT = GPT()
	GPT = None
	pepper = Pepper(config.IP_ADDRESS, config.PORT, GPT)
	webServer = WebServer(pepper, GPT)
	# pepper.makeRequest("http://192.168.1.153:5000/")
	# webServer = WebServer()