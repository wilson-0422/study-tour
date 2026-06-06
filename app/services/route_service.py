from app import db
from app.models.route import Route


class RouteService:
    @staticmethod
    def get_all():
        return Route.query.order_by(Route.created_at.desc()).all()

    @staticmethod
    def get_by_id(route_id):
        return db.session.get(Route, route_id)

    @staticmethod
    def create(data):
        route = Route(**data)
        db.session.add(route)
        db.session.commit()
        return route

    @staticmethod
    def update(route_id, data):
        route = db.session.get(Route, route_id)
        if not route:
            return None
        for key, value in data.items():
            setattr(route, key, value)
        db.session.commit()
        return route

    @staticmethod
    def delete(route_id):
        route = db.session.get(Route, route_id)
        if route:
            db.session.delete(route)
            db.session.commit()
        return route

    @staticmethod
    def get_published():
        return Route.query.filter_by(status="published").order_by(Route.created_at.desc()).all()

    @staticmethod
    def count_by_status(status):
        return Route.query.filter_by(status=status).count()
