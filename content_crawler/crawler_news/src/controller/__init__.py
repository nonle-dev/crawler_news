from flask import Flask, Blueprint


def create_app():
    app = Flask(__name__)

    from .ggnews import ggnews
    app.register_blueprint(ggnews)

    return app
