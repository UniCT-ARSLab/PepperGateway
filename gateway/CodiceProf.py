from ast import Global
import os
import json
import signal
import sys
import threading
from flask import Flask, Response, send_from_directory, render_template, send_file
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO
from waitress import serve
import datetime
import time

from classes.application.Globals import Globals
from classes.utils.Console import Console


class WebServer:
    def init(self, configuration) -> None:
        self.configuration = configuration # HOST, PORT
        self._logWhatString = "WebServer"
        self._directory = "build"
        self.flaskApp = Flask(
            name, 
            static_url_path='',
            static_folder=self._directory, 
            template_folder=self._directory)

        self.flaskApp.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
        self.cors = CORS(self.flaskApp)
        self.flaskApp.config['CORS_HEADERS'] = 'Content-Type'
        self.socketio = SocketIO(self.flaskApp, cors_allowed_origins = "*")


        self.defineRoutes()
        self.defineSocketIOEvents()

        self.sendTimeoutSocket = 0
        self.consoleMessages = []
        self.sendConsoleMessagesTimeout = 0

        self.mainThread = threading.Thread(target=self.startServer)
        try:
            self.mainThread.start()
        except KeyboardInterrupt:
            Console.info("Web Server closed", what="Web Server")
            try:
                exit(0)
            except SystemExit:
                os._exit(0)
        Console.success("Web Server Started", "[http://127.0.0.1:"+str(self.configuration.port)+"]", what=self._logWhatString)
    
    def stopServer(self):
        self.socketio.stop()
        sys.exit(0)

    def startServer(self):
        try:
            self.socketio.run(self.flaskApp, host= '0.0.0.0', port=self.configuration.port, debug=False)
            #serve(self.flaskApp, host= '0.0.0.0', port=self.configuration.port)
            # TODO MANAGE THE STOP OF SERVER
        except KeyboardInterrupt:
            Console.info("Web Server closed", what="Web Server")
            try:
                exit(0)
            except SystemExit:
                sys.exit(0)
        

    def defineSocketIOEvents(self):
        @self.socketio.on('connect')
        def onConnect():
            Console.info("Web Client Connected (socketIO)", what=self._logWhatString)

        @self.socketio.on('disconnect')
        def onDisconnect():
            Console.info("Web Client Disconnected (socketIO)", what=self._logWhatString)
        @self.socketio.on('ping')
        def onPing():
            self.socketio.emit("pong")
            Console.info("Web Client Disconnected (socketIO)", what=self._logWhatString)

    def defineRoutes(self):
        @self.flaskApp.route("/<path:path>")
        def staticDir(path):
            return send_from_directory(directory=self._directory, path=path)

        @self.flaskApp.route('/')
        def home():
            return render_template('index.html')


        @self.flaskApp.get("/version")
        @cross_origin()
        def getVersion():
            return Globals.applicationInstance.VERSION
