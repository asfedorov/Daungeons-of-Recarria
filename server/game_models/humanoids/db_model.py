from database import db


class Humanoid(db.Model):
    __tablename__ = 'humanoids'

    id = db.Column(db.Integer(), primary_key=True)

    kind = db.Column(db.Unicode())
    name = db.Column(db.Unicode())
    age = db.Column(db.Integer())
    experience = db.Column(db.Integer())
    free_points = db.Column(db.Integer())

    strength = db.Column(db.Integer())
    agility = db.Column(db.Integer())
    constitution = db.Column(db.Integer())
    intelligence = db.Column(db.Integer())
    charisma = db.Column(db.Integer())
    wizdom = db.Column(db.Integer())
