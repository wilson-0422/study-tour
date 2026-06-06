from app import db


class Mentor(db.Model):
    __tablename__ = "mentors"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(200))
    rating = db.Column(db.Float, default=0.0)
    total_evaluations = db.Column(db.Integer, default=0)
    bio = db.Column(db.Text)

    user = db.relationship("User", backref=db.backref("mentor_profile", uselist=False))
