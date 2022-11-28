# coding=utf-8

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from time import sleep
# from PepperGateway import robot
# import config
# import time

# FIX: Affinché possa inizializzare il robot, devo importare il modulo robot.py
# Per importare robot.py, devo considerare di copiare l'intera directory PepperGateway all'interno del container 
# e.g. -v /Users/giuseppepitruzzella/PepperGateway:/PepperGateway OR COPY ../ .

# pepper = Pepper(config.IP_ADDRESS, config.PORT)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100))
    x = db.Column(db.Integer)
    y = db.Column(db.Integer)
    theta = db.Column(db.Integer)


@app.route('/')
def index():
    target_list = target.query.all() # SELECT * FROM target;
    print(target_list)

    return render_template('index.html', target_list=target_list)

@app.route('/add', methods=['POST'])
def add():
    # Add new target to the database

    sleep(3) # Delay useful to display form animation
    target_name = request.form.get('target_name')

    # values = pepper.setup_point(target_name)

    # target_x = values[0]
    # target_y = values[1]
    # target_theta = values[2]

    # new_target = target(text = target_name, x = target_x, y = target_y, theta = target_theta)
    new_target = target(text = target_name, x = 0, y = 0, theta = 0)
    db.session.add(new_target)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    # Add new target to the database
    item = target.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))

if (__name__ == "__main__"):
    app.app_context().push()
    db.create_all()
    app.run(debug=True)