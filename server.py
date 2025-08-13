from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from flask_talisman import Talisman
from os import environ as env
from pathlib import Path

# load environment variables
#env_path = Path('/home/dkobrin.helioho.st/flask.dkobrin.helioho.st/Flask_Deploy_test')/'.env'
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)
ORIGINS = env.get('ORIGINS')
PORT = env.get('PORT', 5000)
FLASK_ENV = env.get('FLASK_ENV')
DEBUG = FLASK_ENV == 'development'

app = Flask(__name__)

# HTTP security headers
csp = {
    'default-src': ['\'self\''],
    'frame-ancestors': ['\'none\'']
}

Talisman(app,
         frame_options='DENY',
         content_security_policy=csp,
         referrer_policy='no-referrer'
         )

# Code run before each request - good to open database connection
@app.before_request
def before_request():
    print('Before Request - connect to data')

# Code to run after request - set response headers and close database connection
@app.after_request
def after_request(response):
    response.headers['X-XSS-Protection'] = '0'
    response.headers['Cache-Control'] = 'no-store, max-age=0'
    response.headers['Pragma'] = 'no-chache'
    response.headers['Expires'] = '0'
    response.headers['Content-Type'] = 'application/json; charset=utf-8'
    return response

# CORS policy
CORS(app,
     resources={'/*': {'origins':ORIGINS}},
     allow_headers=['Authorization', 'Content-Type'],
     methods=['GET', 'POST', 'PUT', 'DELETE'],
     supports_credentials=True,
     max_age=86400
     )

# Add Routes or Blueprints Here

# default route for testing
@app.route('/')
def hello():
    print('Hit the default route!')
    return jsonify(data={'result': 'Successfully Hit Default Route!'}, status={'code': 200, 'message': 'SUCCESS!'}), 200


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)