from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.route import Route
from app.models.registration import Registration
from app.models.achievement import Achievement
from app.models.mentor import Mentor
from app import db

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return render_template("index.html")
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    route_count = Route.query.count()
    reg_count = Registration.query.count()
    ach_count = Achievement.query.count()
    mentor_count = Mentor.query.count()
    pending_reg = Registration.query.filter_by(status="pending").count()
    avg_score = db.session.query(db.func.avg(Achievement.score)).filter(
        Achievement.score.isnot(None)
    ).scalar()
    avg_score = round(avg_score, 1) if avg_score else 0

    recent_regs = Registration.query.order_by(
        Registration.registered_at.desc()
    ).limit(5).all()

    return render_template(
        "dashboard/overview.html",
        route_count=route_count,
        reg_count=reg_count,
        ach_count=ach_count,
        mentor_count=mentor_count,
        pending_reg=pending_reg,
        avg_score=avg_score,
        recent_regs=recent_regs,
    )
