from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from Target import Target
import threading
from time import sleep
class WebServer:
    def __init__(self, config):     
        self.flaskApp = Flask(config) # Config is __name__ in previous code
        self.flaskApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
        self.flaskApp.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.defineRoutes()

        self.db = SQLAlchemy(self.flaskApp)

        # self.mainThread = threading.Thread(target=self.startServer)
        # self.mainThread.start()
        self.startServer()

    def startServer(self):
        self.flaskApp.app_context().push()
        self.db.create_all()
        self.flaskApp.run(debug=True)

    def defineRoutes(self):
        @self.flaskApp.route('/')
        def index():
            # target_list = self.target.query.all() # SELECT * FROM target;
            # print(target_list)
            # return render_template('index.html', target_list=target_list)
            return render_template('index.html')

        @self.flaskApp.route('/add', methods=['POST'])
        def add(): # Add new target to the database
            sleep(3) # Delay useful to display form animation
            target_name = request.form.get('target_name')

            new_target = self.setupDatabase(text=target_name, x=0, y=0, theta=0)
            self.db.session.add(new_target)
            self.db.session.commit()
            return redirect(url_for('index'))

        @self.flaskApp.route('/delete/<int:id>')
        def delete(id):
            item = self.target.query.filter_by(id=id).first()
            self.db.session.delete(item)
            self.db.session.commit()
            return redirect(url_for('index'))
        
    def setupDatabase(self, text, x, y, theta):
        id = self.db.Column(self.db.Integer, primary_key=True)
        text = self.db.Column(self.db.String(100))
        x = self.db.Column(self.db.Integer)
        y = self.db.Column(self.db.Integer)
        theta = self.db.Column(self.db.Integer)