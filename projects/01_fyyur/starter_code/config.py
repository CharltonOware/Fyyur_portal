import os
from dotenv import load_dotenv

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir,'.env'))

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

class BaseConfig(object):
    SECRET_KEY = os.urandom(32)
    # Enable debug mode.
    DEBUG = True

    # Connect to the database
    # IMPLEMENT DATABASE URL
    SQLALCHEMY_DATABASE_URI = 'postgresql://'+DB_USER+':'+DB_PASSWORD+'@localhost:5432/'+DB_NAME

    #Disable alerts to app on db changes
    SQLALCHEMY_TRACK_MODIFICATIONS = False