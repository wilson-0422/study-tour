from app import db
from app.models.mentor import Mentor


class MentorService:
    @staticmethod
    def get_all():
        return Mentor.query.all()

    @staticmethod
    def get_by_id(mentor_id):
        return db.session.get(Mentor, mentor_id)

    @staticmethod
    def create(data):
        mentor = Mentor(**data)
        db.session.add(mentor)
        db.session.commit()
        return mentor

    @staticmethod
    def evaluate(mentor_id, score):
        mentor = db.session.get(Mentor, mentor_id)
        if not mentor:
            return None
        total = mentor.rating * mentor.total_evaluations + score
        mentor.total_evaluations += 1
        mentor.rating = round(total / mentor.total_evaluations, 1)
        db.session.commit()
        return mentor

    @staticmethod
    def update(mentor_id, data):
        mentor = db.session.get(Mentor, mentor_id)
        if not mentor:
            return None
        for key, value in data.items():
            setattr(mentor, key, value)
        db.session.commit()
        return mentor

    @staticmethod
    def delete(mentor_id):
        mentor = db.session.get(Mentor, mentor_id)
        if mentor:
            db.session.delete(mentor)
            db.session.commit()
        return mentor

    @staticmethod
    def average_rating():
        result = db.session.query(db.func.avg(Mentor.rating)).filter(
            Mentor.total_evaluations > 0
        ).scalar()
        return round(result, 1) if result else 0.0
