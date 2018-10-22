from flask import Flask


app = Flask(__name__)

app.config['SECRET_KEY']='Hello'

from blog import routes