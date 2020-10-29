# Import the os module
import os

# creation of base directory for application
basedir = os.path.abspath(os.path.dirname(__file__))

# Mac & Linux = Documents/chicodes_sept2020/week_5/homework3



# Config Class
# Configure the database (when we have one) AND configure
# secret key for the encryption of our submitted forms
class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you will never guess this....'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATATBASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
