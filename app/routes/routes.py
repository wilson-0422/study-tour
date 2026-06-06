from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app.services.route_service import RouteService
from app.services.registration_service import RegistrationService

routes_bp = Blueprint("routes", __name__)


@routes_bp.route("/routes")
def list_routes():
    routes = RouteService.get_published()
    return render_template("routes/list.html", routes=routes)


@routes_bp.route("/routes/manage")
@login_required
def manage_routes():
    if not (current_user.is_admin or current_user.is_teacher):
        flash("无权限访问", "danger")
        return redirect(url_for("main.index"))
    routes = RouteService.get_all()
    return render_template("routes/list.html", routes=routes, manage=True)


@routes_bp.route("/routes/<int:route_id>")
def route_detail(route_id):
    route = RouteService.get_by_id(route_id)
    if not route:
        flash("线路不存在", "danger")
        return redirect(url_for("routes.list_routes"))
    registrations = RegistrationService.get_by_route(route_id)
    return render_template("routes/detail.html", route=route, registrations=registrations)


@routes_bp.route("/routes/create", methods=["GET", "POST"])
@login_required
def create_route():
    if not (current_user.is_admin or current_user.is_teacher):
        flash("无权限访问", "danger")
        return redirect(url_for("routes.list_routes"))
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "destination": request.form.get("destination"),
            "description": request.form.get("description"),
            "duration": int(request.form.get("duration")),
            "price": float(request.form.get("price")),
            "max_students": int(request.form.get("max_students")),
            "start_date": datetime.strptime(request.form.get("start_date"), "%Y-%m-%d").date(),
            "end_date": datetime.strptime(request.form.get("end_date"), "%Y-%m-%d").date(),
            "status": request.form.get("status", "draft"),
            "created_by": current_user.id,
        }
        RouteService.create(data)
        flash("线路创建成功", "success")
        return redirect(url_for("routes.manage_routes"))
    return render_template("routes/create.html")


@routes_bp.route("/routes/<int:route_id>/edit", methods=["GET", "POST"])
@login_required
def edit_route(route_id):
    if not (current_user.is_admin or current_user.is_teacher):
        flash("无权限访问", "danger")
        return redirect(url_for("routes.list_routes"))
    route = RouteService.get_by_id(route_id)
    if not route:
        flash("线路不存在", "danger")
        return redirect(url_for("routes.manage_routes"))
    if request.method == "POST":
        data = {
            "name": request.form.get("name"),
            "destination": request.form.get("destination"),
            "description": request.form.get("description"),
            "duration": int(request.form.get("duration")),
            "price": float(request.form.get("price")),
            "max_students": int(request.form.get("max_students")),
            "start_date": datetime.strptime(request.form.get("start_date"), "%Y-%m-%d").date(),
            "end_date": datetime.strptime(request.form.get("end_date"), "%Y-%m-%d").date(),
            "status": request.form.get("status", "draft"),
        }
        RouteService.update(route_id, data)
        flash("线路更新成功", "success")
        return redirect(url_for("routes.manage_routes"))
    return render_template("routes/edit.html", route=route)


@routes_bp.route("/routes/<int:route_id>/delete", methods=["POST"])
@login_required
def delete_route(route_id):
    if not current_user.is_admin:
        flash("无权限操作", "danger")
        return redirect(url_for("routes.manage_routes"))
    RouteService.delete(route_id)
    flash("线路已删除", "success")
    return redirect(url_for("routes.manage_routes"))
