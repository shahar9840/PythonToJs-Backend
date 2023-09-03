from db import db
from uuid import uuid4


class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable= False ,unique=True)
    histories= db.relationship('History',backref='users')


    def serialize(self):
        return {
            'id':self.id,
            'name':self.name
            }
    