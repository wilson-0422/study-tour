from app import db
from app.models.insurance import Insurance


class InsuranceService:
    @staticmethod
    def get_all():
        return Insurance.query.all()

    @staticmethod
    def get_by_id(ins_id):
        return db.session.get(Insurance, ins_id)

    @staticmethod
    def create(data):
        ins = Insurance(**data)
        db.session.add(ins)
        db.session.commit()
        return ins

    @staticmethod
    def get_by_registration(reg_id):
        return Insurance.query.filter_by(registration_id=reg_id).first()

    @staticmethod
    def update(ins_id, data):
        ins = db.session.get(Insurance, ins_id)
        if not ins:
            return None
        for key, value in data.items():
            setattr(ins, key, value)
        db.session.commit()
        return ins

    @staticmethod
    def delete(ins_id):
        ins = db.session.get(Insurance, ins_id)
        if ins:
            db.session.delete(ins)
            db.session.commit()
        return ins

    @staticmethod
    def total_coverage():
        result = db.session.query(db.func.sum(Insurance.coverage_amount)).scalar()
        return result or 0.0
