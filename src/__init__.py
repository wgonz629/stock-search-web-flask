import os
from flask import Flask, send_from_directory

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/index.html')
    def landing_page():
        return send_from_directory('static','index.html')

    return app