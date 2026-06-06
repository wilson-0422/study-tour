from app import db
from datetime import datetime


class Registration(db.Model):
    __tablename__ = "registrations"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    route_id = db.Column(db.Integer, db.ForeignKey("routes.id"), nullable=False)
    status = db.Column(db.String(20), default="pending")
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)

    insurance = db.relationship("Insurance", backref="registration", uselist=False)
