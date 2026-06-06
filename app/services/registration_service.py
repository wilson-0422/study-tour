from app import db
from app.models.registration import Registration


class RegistrationService:
    @staticmethod
    def get_all():
        return Registration.query.order_by(Registration.registered_at.desc()).all()

    @staticmethod
    def get_by_id(reg_id):
        return db.session.get(Registration, reg_id)

    @staticmethod
    def create(data):
        reg = Registration(**data)
        db.session.add(reg)
        db.session.commit()
        return reg

    @staticmethod
    def update_status(reg_id, status):
        reg = db.session.get(Registration, reg_id)
        if reg:
            reg.status = status
            db.session.commit()
        return reg

    @staticmethod
    def get_by_student(student_id):
        return Registration.query.filter_by(student_id=student_id).order_by(
            Registration.registered_at.desc()
        ).all()

    @staticmethod
    def get_by_route(route_id):
        return Registration.query.filter_by(route_id=route_id).all()

    @staticmethod
    def count_by_status(status):
        return Registration.query.filter_by(status=status).count()

    @staticmethod
    def delete(reg_id):
        reg = db.session.get(Registration, reg_id)
        if reg:
            db.session.delete(reg)
            db.session.commit()
        return reg
