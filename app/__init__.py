from flask import Flask
from flask_apscheduler import APScheduler
from config import FlaskConfig

scheduler = APScheduler()

def create_app():
    """
    Create flask app
    :return: app
    """
    app = Flask(__name__)
    app.config.from_object(FlaskConfig)
    # Init scheduler
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    with app.app_context():
        from . import tasks
        return app
