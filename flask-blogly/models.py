"""Models for Blogly."""
from msilib.schema import Property
from xmlrpc.client import DateTime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.kindpng.com/picc/m/24-248253_user-profile-default-image-png-clipart-png-download.png"

class User(db.Model):
    """User site, name and picture"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationships("Post", backref="user", cascade="all, delete-orphan")

    @Property
    def full_name(self):
       """returns your full name""" 
        
       return f"{self.first_name} {self.last_name}"

def connect_db(app):
    """connecting this db to the flask app"""

    db.app = app
    db.init_app(app)


class Post(db.model):
    """Blog Posts"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at= db.Column(db.DateTime, nullable=False, default=DateTime.datetime.now)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return date"""

        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")

    