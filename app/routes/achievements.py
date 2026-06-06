from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.achievement_service import AchievementService
from app.services.route_service import RouteService

achievements_bp = Blueprint("achievements", __name__)


@achievements_bp.route("/achievements")
@login_required
def list_achievements():
    if current_user.is_admin or current_user.is_teacher:
        achievements = AchievementService.get_all()
    else:
        achievements = AchievementService.get_by_student(current_user.id)
    return render_template("achievements/list.html", achievements=achievements)


@achievements_bp.route("/achievements/create", methods=["GET", "POST"])
@login_required
def create_achievement():
    if request.method == "POST":
        data = {
            "student_id": current_user.id,
            "route_id": int(request.form.get("route_id")),
            "title": request.form.get("title"),
            "content": request.form.get("content"),
        }
        AchievementService.create(data)
        flash("成果提交成功", "success")
        return redirect(url_for("achievements.list_achievements"))
    regs = RegistrationService.get_by_student(current_user.id) if not (current_user.is_admin or current_user.is_teacher) else []
    routes = RouteService.get_all() if (current_user.is_admin or current_user.is_teacher) else [r.route for r in regs if r.status == "approved"]
    return render_template("achievements/create.html", routes=routes)


@achievements_bp.route("/achievements/<int:ach_id>")
@login_required
def achievement_detail(ach_id):
    ach = AchievementService.get_by_id(ach_id)
    if not ach:
        flash("成果记录不存在", "danger")
        return redirect(url_for("achievements.list_achievements"))
    if not (current_user.is_admin or current_user.is_teacher) and ach.student_id != current_user.id:
        flash("无权限查看", "danger")
        return redirect(url_for("achievements.list_achievements"))
    return render_template("achievements/detail.html", ach=ach)


@achievements_bp.route("/achievements/<int:ach_id>/grade", methods=["POST"])
@login_required
def grade_achievement(ach_id):
    if not (current_user.is_admin or current_user.is_teacher):
        flash("无权限操作", "danger")
        return redirect(url_for("achievements.list_achievements"))
    score = float(request.form.get("score"))
    feedback = request.form.get("feedback")
    AchievementService.grade(ach_id, score, feedback)
    flash("评分成功", "success")
    return redirect(url_for("achievements.achievement_detail", ach_id=ach_id))


from app.services.registration_service import RegistrationService
