import os
from flask import Flask, send_from_directory


application = Flask(__name__, instance_relative_config=True)
try:
    os.makedirs(application.instance_path)
except OSError:
    pass

import parse_data
application.register_blueprint(parse_data.bp)

@application.route('/')
def landing_page():
    return send_from_directory('static','index.html')

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()