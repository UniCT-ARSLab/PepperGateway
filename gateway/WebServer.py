from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from robot import *
import config
import time
from time import sleep

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    theta = db.Column(db.Integer)

class WebServer:
    def __init__(self, robot):
        self.robot = robot    
        self.defineRoutes()
        self.startServer()

    # def __init__(self):   
    #     self.defineRoutes()
    #     self.startServer()

    def startServer(self):
        app.app_context().push()
        db.create_all()
        app.run(debug=True, host='0.0.0.0', port=5000)

    def defineRoutes(self):
        @app.route('/')
        def index():
            # self.robot.load_map("/home/nao/.local/share/Explorer/2014-04-04T030832.649Z.explo")
            # self.robot.exploration_mode(10)
            targetList = Target.query.all() # SELECT * FROM target;
            return render_template('index.html', targetList=targetList)

        @app.route('/environment/')
        def environment():
            return render_template('environment.html')

        @app.route('/add', methods=['POST'])
        def add():
            sleep(3) # Delay useful to display form animation
            target_name = request.form.get('target_name')

            # item = Target(text=target_name, x=0, y=0, theta=0)

            self.robot.robot_localization()
            item = Target(text=target_name, 
                x=self.robot.localization[0], 
                y=self.robot.localization[1], 
                theta=self.robot.localization[2])
            
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('index'))

        @app.route('/delete/<int:id>')
        def delete(id):
            item = Target.query.filter_by(id=id).first()
            db.session.delete(item)
            db.session.commit()
            return redirect(url_for('index'))

        @app.route('/get/<int:id>')
        def get(id):
            item = Target.query.filter_by(id=id).first()
            
            # self.robot.say("Eseguo lo spostamento verso " + item.text)
            # self.robot.robot_localization()
            # self.robot.navigate_to(item.x, item.y, item.theta)
            return redirect(url_for('index'))

        @app.route('/say', methods=['POST'])
        def say():
            self.robot.say(request.form.get('text'))
            return redirect(url_for('index'))

        @app.route('/awareness_on', methods=['POST'])
        def awareness_on():
            self.robot.set_awareness(True)
            return redirect(url_for('index'))
        
        @app.route('/awareness_off', methods=['POST'])
        def awareness_off():
            self.robot.set_awareness(False)
            return redirect(url_for('index'))
        
        @app.route('/rotate')
        def rotate():
            self.robot.say("Avvio rotazione")
            self.robot.turn_around(0.1)
            return redirect(url_for('index'))
    

    