from flask_sqlalchemy import SQLAlchemy

class Target:
    def __init__(self, db):
        id = db.Column(db.Integer, primary_key=True)
        text = db.Column(db.String(100))
        x = db.Column(db.Integer)
        y = db.Column(db.Integer)
        theta = db.Column(db.Integer)
