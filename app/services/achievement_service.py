from app import db
from app.models.achievement import Achievement


class AchievementService:
    @staticmethod
    def get_all():
        return Achievement.query.order_by(Achievement.submitted_at.desc()).all()

    @staticmethod
    def get_by_id(ach_id):
        return db.session.get(Achievement, ach_id)

    @staticmethod
    def create(data):
        ach = Achievement(**data)
        db.session.add(ach)
        db.session.commit()
        return ach

    @staticmethod
    def get_by_student(student_id):
        return Achievement.query.filter_by(student_id=student_id).order_by(
            Achievement.submitted_at.desc()
        ).all()

    @staticmethod
    def get_by_route(route_id):
        return Achievement.query.filter_by(route_id=route_id).all()

    @staticmethod
    def grade(ach_id, score, feedback):
        ach = db.session.get(Achievement, ach_id)
        if ach:
            ach.score = score
            ach.feedback = feedback
            db.session.commit()
        return ach

    @staticmethod
    def delete(ach_id):
        ach = db.session.get(Achievement, ach_id)
        if ach:
            db.session.delete(ach)
            db.session.commit()
        return ach

    @staticmethod
    def average_score():
        result = db.session.query(db.func.avg(Achievement.score)).filter(
            Achievement.score.isnot(None)
        ).scalar()
        return round(result, 1) if result else 0.0
