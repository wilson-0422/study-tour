from app import db


class Accommodation(db.Model):
    __tablename__ = "accommodations"

    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey("routes.id"), nullable=False)
    hotel_name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    room_type = db.Column(db.String(50), nullable=False)
    meals_included = db.Column(db.Boolean, default=False)
    cost_per_person = db.Column(db.Float, nullable=False)
