__author__ = "Grant Martin"

import os
from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from error_log_email import  TlsSMTPHandler

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# setup login system
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

# set up email capabilities

mail = Mail(app)

# set up logging
if not app.debug and MAIL_SERVER !='':
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_PASSWORD or MAIL_USERNAME:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = TlsSMTPHandler((MAIL_SERVER, 587), "Errors@CYNY_Vid_Server.com", ADMINS, "CYNY Vid Server Error!", credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('tmp/CYNY_server.log', 'a', 1*1024*1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info("CYNY Video Server Startup")

from app import views, models