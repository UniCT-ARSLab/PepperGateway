from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from robot import *
import config
import time

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/db.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# class Target(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(100))
#     x = db.Column(db.Integer)
#     y = db.Column(db.Integer)
#     theta = db.Column(db.Integer)

class WebServer:
    def __init__(self, robot):
        self.robot = robot    
        self.defineRoutes()
        self.startServer()
        

    def startServer(self):
        # app.app_context().push()
        # db.create_all()
        app.run(debug=True, host='0.0.0.0', port=5000)

    def defineRoutes(self):
        @app.route('/')
        def index():
            self.robot.say("Web server started")
            return render_template('index.html')

    

    