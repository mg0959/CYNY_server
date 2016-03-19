from app import app, db
from hashlib import md5
import uuid
import hashlib

# Uers Roles
ROLE_FULL_ADMIN = 1

codeLink = db.Table('codeLink',
                    db.Column('code_id', db.Integer, db.ForeignKey('location_code.id')),
                    db.Column('video_id', db.Integer, db.ForeignKey('video.id')))

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(89))
    role = db.Column(db.SmallInteger)
    last_seen = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return unicode(self.id)

    # password management

    def set_password(self, password):
        self.password = Admin.hash_password(password)

    def check_password(self, given_password):
        password, salt = self.password.split(":")
        return password == hashlib.sha224(salt.encode()+given_password.encode()).hexdigest()

    def get_reset_password_token(self):
        return Admin.hash_reset_password(self.last_seen, self.password)

    def check_reset_password_token(self,token):
        salt = token[-32:]
        return token[:-32] == hashlib.sha256(salt.encode()+str(self.last_seen).encode()+self.password.encode()).hexdigest()

    def __repr__(self):
        return '<Admin %r>' % (self.name)

    @staticmethod
    def hash_password(password):
        # uuid is used to generate a random number
        salt = uuid.uuid4().hex
        return hashlib.sha224(salt.encode() + password.encode()).hexdigest() + ":"+salt

    @staticmethod
    def hash_reset_password(lastLogin, password):
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode()+str(lastLogin).encode()+password.encode()).hexdigest()+salt

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime)
    description = db.Column(db.String(240), default="")

    def __repr__(self):
        return '<Video %r>' % (self.fname)

class Location_code(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), index=True, unique=True)
    date_added = db.Column(db.DateTime)
    videos = db.relationship('Video',
                             secondary = codeLink,
                             primaryjoin = (codeLink.c.code_id == id),
                             secondaryjoin = (codeLink.c.video_id == Video.id),
                             backref = db.backref('location_codes', lazy='dynamic'),
                             lazy = 'dynamic')

    def __repr__(self):
        return '<Location Code: %r>' % (self.code)
