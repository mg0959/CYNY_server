import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'app.db')+'?check_same_thread=False'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

CSRF_ENABLED = True
SECRET_KEY = 'really_secret_key_you_wont_guess'

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = "no.reply.mmissionconnect@gmail.com" #os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = "mc2014mc" #os.environ.get('MAIL_PASSWORD')

# administrator list
ADMINS = ['mg0959@gmail.com']

# records times of db calls
SQLALCHEMY_RECORD_QUERIES = True
DATABASE_QUERY_TIMEOUT = 0.5 # slow database quuery threshold (in seconds)

