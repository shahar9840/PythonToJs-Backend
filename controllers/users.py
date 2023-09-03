
from flask_restful import Resource
from flask import jsonify,request
from models.users import Users
from datetime import datetime, timedelta
from db import db
from flask_jwt_extended import jwt_required,create_access_token,get_jwt_identity,current_user,create_refresh_token

class UsersAll(Resource):
    
    
    def get(self):
        users = Users.query.all()
        return [user.serialize() for user in users]



class CreateToken(Resource):
    def post(self):
        name = request.json.get('name', None)
        user = Users.query.filter_by(name=name).first()
        if user:
            now = datetime.now()  # Get the current UTC time
            expires_delta = timedelta(seconds=3600)  # Adjust the expiration time as needed

            access_token = create_access_token(identity=name, expires_delta=expires_delta)
            refresh_token = create_refresh_token(identity=name, expires_delta=expires_delta)
            return jsonify(access_token=access_token, refresh_token=refresh_token, expires_in=3600)
        else:
            data = request.get_json()
            new_user = Users(**data)
            db.session.add(new_user)
            db.session.commit()
            now = datetime.now()  # Get the current UTC time
            expires_delta = timedelta(seconds=3600)  # Adjust the expiration time as needed

            access_token = create_access_token(identity=name, expires_delta=expires_delta)
            refresh_token = create_refresh_token(identity=name, expires_delta=expires_delta)
            return jsonify(access_token=access_token, refresh_token=refresh_token, expires_in=3600)


class CheckAuth(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        print('current user:',current_user)
        return {"user":current_user}
