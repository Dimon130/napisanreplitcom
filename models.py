from app import db
from datetime import datetime

class RSVP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    guests = db.Column(db.Integer, default=1)
    attending = db.Column(db.Boolean, nullable=False)
    message = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
