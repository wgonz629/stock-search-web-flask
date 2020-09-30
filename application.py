import os
from flask import Flask, send_from_directory
import parse_data

application = Flask(__name__)

application.register_blueprint(parse_data.bp)

@application.route('/')
def landing_page():
    return send_from_directory('static','index.html')

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()