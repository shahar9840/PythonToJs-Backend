
from flask_restful import Resource
from flask import jsonify
from models.history import History
from db import db
from pscript import py2js
from flask_jwt_extended import jwt_required,create_access_token,get_jwt_identity 
from flask import request
from models.users import Users

class HistoryAll(Resource):
    def get(self):
        histories = History.query.all()
        return [history.serialize()for history in histories]
    def post(self):
        data = request.get_json()
        user=Users.query.filter_by(name=data['user_name']).first()
        new_code = History(python_code=data['python_code'], user_id=user.id)
        db.session.add(new_code)
        db.session.commit()
        return {"message":'New code added succsesfully ',"id":new_code.id},201
    

class HistoryOne(Resource):
    
    @jwt_required()
    def get(self,id):
        current_user = get_jwt_identity()
        print(current_user)
        user = Users.query.filter_by(name=current_user).first()
        history=History.query.get(id)
        
        if history and user.id == history.user_id:
            return [history.serialize()]
        else:
            return{'Error':'Somthing went wrong'},404
    @jwt_required()
    def put(self,id): 
        current_user = get_jwt_identity()
        print(current_user)
        user = Users.query.filter_by(name=current_user).first() 
        history = History.query.get(id)
        data = request.get_json()
        code_id = data['id']
        print('code_id',code_id,'id',id)
        if history and user.id == history.user_id:
            new_code = data.get("python_code")
            convert = py2js(new_code)
            history.python_code = new_code
            history.js_code = convert
            db.session.commit()
            return {'message':"code has been update","convert":convert}
    @jwt_required()
    def delete(self,id):
        current_user = get_jwt_identity()
        user = Users.query.filter_by(name=current_user).first()
        history = History.query.get(id)
        print(history)
        print(user)
        data = request.get_json()
        print('before the if')
        if history :
            print('in the if ')
            db.session.delete(history)
            db.session.commit()
            return {'message': "Code block has been deleted"}
        else:
             return {'message': "Code block not found or unauthorized to delete"}, 404
        
class HistoryByUser(Resource):
    @jwt_required()
    def get(self,name):
        current_user = get_jwt_identity()
        print('user:',current_user)
        user = Users.query.filter_by(name=current_user).first()
        print(user)
        print(current_user)
        if user.name == current_user:
            hisories = History.query.filter_by(user_id=str(user.id)).all()
            return [history.serialize()for history in hisories]
        else:
            return {
                'message': 'the token doesnt exist'
            }


