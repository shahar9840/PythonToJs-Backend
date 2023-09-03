FROM amd64/python:3.10-slim

WORKDIR /python_to_js

RUN pip install Flask Flask-RESTful Flask-SQLAlchemy Flask-Cors Flask_jwt_extended Flask_socketio psycopg2-binary pscript

COPY . .

CMD python server.py
