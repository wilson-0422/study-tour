from app import db


class Insurance(db.Model):
    __tablename__ = "insurances"

    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(
        db.Integer, db.ForeignKey("registrations.id"), nullable=False, unique=True
    )
    provider = db.Column(db.String(100), nullable=False)
    policy_number = db.Column(db.String(100), unique=True, nullable=False)
    coverage_amount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    premium = db.Column(db.Float, nullable=False)
