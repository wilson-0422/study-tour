from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.registration_service import RegistrationService
from app.services.route_service import RouteService

registrations_bp = Blueprint("registrations", __name__)


@registrations_bp.route("/registrations")
@login_required
def list_registrations():
    if current_user.is_admin or current_user.is_teacher:
        registrations = RegistrationService.get_all()
    else:
        registrations = RegistrationService.get_by_student(current_user.id)
    return render_template("registrations/list.html", registrations=registrations)


@registrations_bp.route("/registrations/create", methods=["GET", "POST"])
@login_required
def create_registration():
    if request.method == "POST":
        route_id = request.form.get("route_id")
        notes = request.form.get("notes")
        existing = RegistrationService.get_by_student(current_user.id)
        for reg in existing:
            if reg.route_id == int(route_id) and reg.status in ("pending", "approved"):
                flash("您已报名该线路", "warning")
                return redirect(url_for("registrations.list_registrations"))
        RegistrationService.create({
            "student_id": current_user.id,
            "route_id": int(route_id),
            "notes": notes,
        })
        flash("报名成功", "success")
        return redirect(url_for("registrations.list_registrations"))
    routes = RouteService.get_published()
    return render_template("registrations/create.html", routes=routes)


@registrations_bp.route("/registrations/<int:reg_id>")
@login_required
def registration_detail(reg_id):
    reg = RegistrationService.get_by_id(reg_id)
    if not reg:
        flash("报名记录不存在", "danger")
        return redirect(url_for("registrations.list_registrations"))
    if not (current_user.is_admin or current_user.is_teacher) and reg.student_id != current_user.id:
        flash("无权限查看", "danger")
        return redirect(url_for("registrations.list_registrations"))
    return render_template("registrations/detail.html", reg=reg)


@registrations_bp.route("/registrations/<int:reg_id>/approve", methods=["POST"])
@login_required
def approve_registration(reg_id):
    if not (current_user.is_admin or current_user.is_teacher):
        flash("无权限操作", "danger")
        return redirect(url_for("registrations.list_registrations"))
    RegistrationService.update_status(reg_id, "approved")
    flash("已批准报名", "success")
    return redirect(url_for("registrations.list_registrations"))


@registrations_bp.route("/registrations/<int:reg_id>/reject", methods=["POST"])
@login_required
def reject_registration(reg_id):
    if not (current_user.is_admin or current_user.is_teacher):
        flash("无权限操作", "danger")
        return redirect(url_for("registrations.list_registrations"))
    RegistrationService.update_status(reg_id, "rejected")
    flash("已拒绝报名", "success")
    return redirect(url_for("registrations.list_registrations"))


@registrations_bp.route("/registrations/<int:reg_id>/cancel", methods=["POST"])
@login_required
def cancel_registration(reg_id):
    reg = RegistrationService.get_by_id(reg_id)
    if not reg or (reg.student_id != current_user.id and not current_user.is_admin):
        flash("无权限操作", "danger")
        return redirect(url_for("registrations.list_registrations"))
    RegistrationService.update_status(reg_id, "cancelled")
    flash("已取消报名", "success")
    return redirect(url_for("registrations.list_registrations"))
