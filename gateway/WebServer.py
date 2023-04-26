from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from robot import *
import config
import time
import json
import threading
from geventwebsocket import WebSocketApplication, WebSocketServer, Resource
from geventwebsocket.handler import WebSocketHandler
from gevent import pywsgi
from gevent.pywsgi import WSGIHandler

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
pepper = None

class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    theta = db.Column(db.Integer)

class WebSocketCommunication(WebSocketApplication):

    def on_open(self):
        print("Client connected!")

    def on_message(self, message):
        global pepper
        if message is None:
            return
        message = json.loads(message)
        print(message["data"])
        if pepper:
            if message['msg_type'] == 'move_forward':
                print("Linear Speed : ", message['data'])
                pepper.move_forward(message['data'])
            elif message['msg_type'] == 'rotate':
                print("Angular Speed : ",message['data'])
                pepper.turn_around(message['data'])

    def on_close(self, reason):
        print("Connection closed!")

class WebServer:
    def __init__(self, robot = None, GPT = None):
        global pepper
        pepper = robot

        self.GPT = GPT # Use this istance of GPT to handle text messages
        self.robot = robot
        self.defineRoutes()
        threading.Thread(target=self.startServer(), daemon=True).start()
        

    def startServer(self):
        app.app_context().push()
        db.create_all()
        WebSocketServer(
            ('0.0.0.0', 5000),
            Resource([
                ('^/ws', WebSocketCommunication),
                ('^/.*', app)
            ]),
            debug=False
        ).serve_forever()
        # app.run(debug=True, host='0.0.0.0', port=5000)
        
    def defineRoutes(self):
        @app.route('/')
        def index():
            targetList = Target.query.all() # SELECT * FROM target;
            return render_template('index.html', targetList=targetList)

        @app.route('/pointsOfInterest')
        def pointsOfInterests():
            return render_template('pointsOfInterest.html')
        
        @app.route('/Homepage')
        def getHomepage():
            return render_template('index.html')

        @app.route('/joypadMode')
        def joypadMode():
            return render_template('joypadMode.html')

        @app.route('/chatMode')
        def chatMode():
            return render_template('chatMode.html')
        
        @app.route('/explorationMode')
        def explorationMode():
            return render_template('explorationMode.html')

        @app.route('/settingsPage')
        def settingsPage():
            return render_template('settingsPage.html')
        
        @app.route('/tabletPage')
        def tabletPage():
            return render_template('tabletPage.html')

        # Points of Interest
        @app.route('/add', methods=['POST'])
        def add():
            target_name = json.loads(request.data)["data"]
            self.robot.say("Salvo il nuovo punto di interesse: " + str(target_name))
            print("[POINT] Add new point: " + str(target_name))
            self.robot.robot_localization() # Get robot localization in the map

            map = self.robot.getMap()
            if (map == None):
                print("[POINT] Error: Map not found")
            else:
                item = {"map": map,
                        "name": target_name, 
                        "x" : self.robot.localization[0], 
                        "y" : self.robot.localization[1], 
                        "theta" : self.robot.localization[2]}
                with open("points.txt", "a+") as f:
                    f.write(json.dumps(item) + "\n")
            return redirect(url_for('pointsOfInterests'))
        # @app.route('/add', methods=['POST'])
        # def add():
        #     target_name = request.form.get('target_name')

        #     self.robot.robot_localization()
        #     item = Target(text=target_name, 
        #         x=self.robot.localization[0], 
        #         y=self.robot.localization[1], 
        #         theta=self.robot.localization[2])
            
        #     db.session.add(item)
        #     db.session.commit()
        #     return redirect(url_for('pointsOfInterests'))

        @app.route('/delete/<int:id>')
        def delete(id):
            item = Target.query.filter_by(id=id).first()
            db.session.delete(item)
            db.session.commit()
            return redirect(url_for('pointsOfInterest'))

        @app.route('/get/<int:id>')
        def get(id):
            item = Target.query.filter_by(id=id).first()
            self.robot.say("Eseguo lo spostamento verso " + item.text)
            self.robot.robot_localization()
            self.robot.navigate_to(item.x, item.y, item.theta)
            return redirect(url_for('pointsOfInterest'))

        # Exploration Mode
        @app.route('/exploreEnv', methods=['POST'])
        def exploreEnv():
            radius = json.loads(request.data)["data"]
            self.robot.say("Eseguo l'esplorazione dell'ambiente")
            self.robot.exploration_mode(int(radius))
            self.robot.save_map()
            return "[INFO] Exploration completed"
        
        @app.route('/getMaps', methods=['GET'])
        def getMaps():
            return json.dumps(self.robot.get_maps())
        
        @app.route('/loadMap', methods=['POST'])
        def loadMap():            
            self.robot.load_map(request.data)
            self.robot.say("Mappa caricata correttamente")
            return "[INFO] Map loaded correctly"
        
        @app.route('/deleteMap', methods=['POST'])
        def deleteMap():
            self.robot.delete_map(request.data)
            self.robot.say("Mappa eliminata correttamente")
            return render_template('pointsOfInterest.html')
        
        # Settings Page
        @app.route('/getBattery', methods=['GET'])
        def getBattery():
            return self.robot.battery_status()
        
        @app.route('/setAutonomous', methods=['POST'])
        def setAutonomous():
            state = json.loads(request.data)
            return self.robot.setAutonomousLife(state["data"])
        
        @app.route('/getAutonomous', methods=['GET'])
        def getAutonomous():
            return self.robot.getAutonomousLife()

        # Chat Mode
        @app.route('/getAnswer', methods=['POST'])
        def getAnswer():
            data = json.loads(request.data)
            data = data.get("data") # {data : "message"}
            response = self.robot.getAnswer(data) # [LOOK] I change this from self.GPT.getAnswer(data) to self.robot.getAnswer(data)
            print("[INFO] Response from GPT : ", response)
            # self.robot.say(response) # [LOOK] Commented this line
            return {"data" : response}
        
        @app.route('/getSpeech', methods=['GET'])
        def getSpeech():
            return self.robot.speechToText(getAnswer = True)

        @app.route('/setStreamMode', methods=['GET'])
        def setStreamMode():
            self.robot.startStreamingSpeech()
            return "[INFO] Stream mode started"

        @app.route('/startListening', methods=['GET'])
        def startListening():
            return self.robot.startMicrophone()
        
        @app.route('/stopMicrophone', methods=['GET'])
        def stopMicrophone():
            return self.robot.stopMicrophone()
    
        @app.route('/stopListening', methods=['GET'])
        def stopListening():
            self.robot.stopMicrophone()
            return self.robot.speechToText("speech.wav")
        
        # @app.route('/liveListening', methods=['GET'])
        # def liveListening():
        #     # Alla fine dei giochi, live listening esegue solo lo script corrado.py all'interno del robot mediante ssh
        #     self.robot.say("Attivo modalita' Live!")
        #     self.robot.liveListening()
        #     return "[INFO] Live listening started"
        
        @app.route('/setLiveListening', methods=['POST'])
        def setLiveListening():
            print("[INFO] Test passed")
            isOpen = json.loads(request.data)["data"]
            if not isOpen:
                print("[INFO] Live listening started...")
                self.robot.say("Attivo modalita' Live!")
                self.robot.liveListening()
            else:
                print("[INFO] Live listening stopped...")
                self.robot.say("Disattivo modalita' Live!")
                self.robot.liveListening(isOpen = True)
            return "[SUCCESS] Live listening setted correctly"

             

        
    
    

    