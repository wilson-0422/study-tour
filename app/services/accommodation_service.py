from app import db
from app.models.accommodation import Accommodation


class AccommodationService:
    @staticmethod
    def get_all():
        return Accommodation.query.all()

    @staticmethod
    def get_by_id(acc_id):
        return db.session.get(Accommodation, acc_id)

    @staticmethod
    def create(data):
        acc = Accommodation(**data)
        db.session.add(acc)
        db.session.commit()
        return acc

    @staticmethod
    def get_by_route(route_id):
        return Accommodation.query.filter_by(route_id=route_id).all()

    @staticmethod
    def update(acc_id, data):
        acc = db.session.get(Accommodation, acc_id)
        if not acc:
            return None
        for key, value in data.items():
            setattr(acc, key, value)
        db.session.commit()
        return acc

    @staticmethod
    def delete(acc_id):
        acc = db.session.get(Accommodation, acc_id)
        if acc:
            db.session.delete(acc)
            db.session.commit()
        return acc

    @staticmethod
    def total_cost():
        result = db.session.query(db.func.sum(Accommodation.cost_per_person)).scalar()
        return result or 0.0
