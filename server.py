
from flask import Flask , request
from db import db
from flask_cors import CORS
from flask_socketio import SocketIO,emit
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from controllers.history import HistoryOne,HistoryAll,HistoryByUser
from controllers.users import CreateToken,UsersAll,CheckAuth
from models.history import History
from flask_jwt_extended import JWTManager,create_access_token,jwt_required , get_jwt_identity
from config import DBHOST,DBPASS,DBUSER

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{DBUSER}:{DBPASS}@{DBHOST}/postgres'
db.init_app(app)
app.config['SECRET_KEY'] = 'ddbgsdbsddadvfgsfagewt44'
jwt= JWTManager(app)
api = Api(app)

CORS(app, resources={r"/*": {"origins": "*"}})



with app.app_context():
    db.create_all()


api.add_resource(HistoryAll,'/history')
api.add_resource(UsersAll,'/users')
api.add_resource(CheckAuth,'/check_token')
api.add_resource(CreateToken,'/token')
api.add_resource(HistoryOne,'/history/<int:id>')
api.add_resource(HistoryByUser,'/history_by_user/<name>')


if __name__ == "__main__":
    app.run(debug=True, port=50000, host='0.0.0.0')
