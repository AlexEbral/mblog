from flask import Flask
import logging
from mblog_web.frontend.views import mod as main_views
from mblog_web import db_utils
from mblog_web import json_utils


def create_app():
    app = Flask(__name__)
    app.config.from_object('mblog_web.config')
    db_utils.init_db(app)

    if not app.debug:
        app.logger.setLevel(logging.DEBUG)
        del app.logger.handlers[:]
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
        app.logger.addHandler(handler)

    app.secret_key = 'verysecretkey'
    app.register_blueprint(main_views)
    app.json_encoder = json_utils.MyJsonEncoder

    print('Created app')
    return app

