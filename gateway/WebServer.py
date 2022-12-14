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

    def __init__(self):   
        self.defineRoutes()
        self.startServer()

    def startServer(self):
        # app.app_context().push()
        db.create_all()

        new_todo = Target(text="test", x=1, y=2, theta=3)
        db.session.add(new_todo)
        db.session.commit()

        app.run(debug=True, host='0.0.0.0', port=5000)

    def defineRoutes(self):
        # @app.route('/')
        # def index():
        #     # self.robot.say("Web server started")
        #     todos = Target.query.all()
        #     print(todos)
        #     return render_template('index.html')

        @app.route('/')
        def index():
            targetList = Target.query.all() # SELECT * FROM target;
            return render_template('index.html', targetList=targetList)
            # return render_template('index.html')

        @app.route('/add', methods=['POST'])
        def add():
            sleep(3) # Delay useful to display form animation
            target_name = request.form.get('target_name')

            item = Target(text=target_name, x=0, y=0, theta=0)
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('index'))

        @app.route('/delete/<int:id>')
        def delete(id):
            item = Target.query.filter_by(id=id).first()
            db.session.delete(item)
            db.session.commit()
            return redirect(url_for('index'))

    

    