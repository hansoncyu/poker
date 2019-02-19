from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://local:password@127.0.0.1/poker'
db = SQLAlchemy(app)

from database import models

@app.route('/')
def hello_world():
    return 'hello world'
