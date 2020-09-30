import os
from flask import Flask, send_from_directory

def create_app():
    application = Flask(__name__, instance_relative_config=True)
    try:
        os.makedirs(application.instance_path)
    except OSError:
        pass

    from src import parse_data
    application.register_blueprint(parse_data.bp)

    @application.route('/')
    def landing_page():
        return send_from_directory('static','index.html')

    return application