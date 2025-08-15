import os, sys

# edit your path below
sys.path.append("/flask.dkobrin.helioho.st/FlaskDeployTest/");

sys.path.insert(0, os.path.dirname(__file__))
from server import app as application

# set this to something harder to guess
application.secret_key = 'secret'