from flask import Flask, request
from dynaconf import settings             
from flask import jsonify
import views

def create_app():
    app = Flask(__name__)
    views.configure(app)
    return app