import os

from flask import Flask

from config import config



def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('BANK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    @app.route('/')
    def index():
        return {'hello': 'world'}
    return app
    