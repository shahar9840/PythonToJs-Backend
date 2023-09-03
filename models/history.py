
from db import db 
from datetime import datetime as dt

class History(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime,default=dt.now)
    python_code = db.Column(db.Text)
    js_code=db.Column(db.Text)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def serialize (self):
        return {
            "id" : self.id,
            'date':self.date.strftime("%d-%m-%Y %H:%M"),
            'python_code':self.python_code,
            'js_code':self.js_code,
            'user_id':self.user_id
        }