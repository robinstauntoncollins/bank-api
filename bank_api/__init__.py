import os

from flask import Flask, make_response
from flask_migrate import Migrate

from config import config

from .models import db

from bank_api.api.v1 import api_v1_bp, API_VERSION_V1
from bank_api.intentapi import intent_api



def create_app(config_name: str=None) -> Flask:
    if config_name is None:
        config_name = os.environ.get('BANKAPI_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(
        api_v1_bp,
        url_prefix=f"{app.config['URL_PREFIX']}/v{API_VERSION_V1}"
    )

    app.register_blueprint(
        intent_api,
        url_prefix=f"{app.config['URL_PREFIX']}/v{API_VERSION_V1}"
    )

    @app.route('/')
    def index():
        from bank_api.api.v1 import get_catelog as v1_catelog
        return {'version': {'v1': v1_catelog()}}

    @app.errorhandler(404)
    def not_found(error):
        return make_response({'error': 'Not found'}, 404)

    @app.errorhandler(405)
    def not_found(error):
        return make_response({'error': 'Method not allowed'}, 405)

    @app.errorhandler(500)
    def not_found(error):
        return make_response({'error': 'Internal Server Error'}, 500)
    
    return app
    