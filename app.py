""" Inicio do APP importando FLASK"""
from flask import Flask, redirect
import views


def create_app():
    """Classe Inicial """
    app = Flask(__name__)
    views.configure(app)
    return app
