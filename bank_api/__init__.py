import os

from flask import Flask
from flask_migrate import Migrate

from config import config

from .models import db

from bank_api.api.v1 import api_v1_bp, API_VERSION_V1



def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('BANK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(
        api_v1_bp,
        url_prefix=f"{app.config['URL_PREFIX']}/v{API_VERSION_V1}"
    )

    @app.route('/')
    def index():
        from bank_api.api.v1 import get_catelog as v1_catelog
        return {'version': {'v1': v1_catelog()}}
    return app
    