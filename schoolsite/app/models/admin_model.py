from sqlalchemy import JSON
from schoolsite.app import db
from datetime import datetime
from flask_login import UserMixin


class Admin(db.Model, UserMixin):
    username = db.Column(db.String(100), primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    phonenumber = db.Column(db.String(20), nullable=True)
    access = db.Column(db.Boolean, nullable=True)
    key = db.Column(db.String(200), nullable=True)
    role = db.Column(db.String(50), default="Admin")
    image_link = db.Column(db.String(100),
                           default='default.png')

    def __repr__(self):
        return f"{self.lastname} {self.firstname}"

    def get_id(self):
        return self.username


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"Event('{self.name}', '{self.date}')"


class Announcement(db.Model):
    __tablename__ = 'announcements'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)

    def __repr__(self):
        return f"Announcement(title='{self.title}', content='{self.content}', created_at='{self.created_at}')"
