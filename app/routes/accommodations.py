from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app.services.accommodation_service import AccommodationService
from app.services.route_service import RouteService

accommodations_bp = Blueprint("accommodations", __name__)


@accommodations_bp.route("/accommodations")
@login_required
def list_accommodations():
    if current_user.is_admin or current_user.is_teacher:
        accommodations = AccommodationService.get_all()
    else:
        accommodations = AccommodationService.get_all()
    return render_template("accommodations/list.html", accommodations=accommodations)


@accommodations_bp.route("/accommodations/create", methods=["GET", "POST"])
@login_required
def create_accommodation():
    if not (current_user.is_admin or current_user.is_teacher):
        flash("无权限操作", "danger")
        return redirect(url_for("accommodations.list_accommodations"))
    if request.method == "POST":
        data = {
            "route_id": int(request.form.get("route_id")),
            "hotel_name": request.form.get("hotel_name"),
            "address": request.form.get("address"),
            "check_in": datetime.strptime(request.form.get("check_in"), "%Y-%m-%d").date(),
            "check_out": datetime.strptime(request.form.get("check_out"), "%Y-%m-%d").date(),
            "room_type": request.form.get("room_type"),
            "meals_included": request.form.get("meals_included") == "on",
            "cost_per_person": float(request.form.get("cost_per_person")),
        }
        AccommodationService.create(data)
        flash("食宿安排创建成功", "success")
        return redirect(url_for("accommodations.list_accommodations"))
    routes = RouteService.get_all()
    return render_template("accommodations/create.html", routes=routes)


@accommodations_bp.route("/accommodations/<int:acc_id>")
@login_required
def accommodation_detail(acc_id):
    acc = AccommodationService.get_by_id(acc_id)
    if not acc:
        flash("食宿记录不存在", "danger")
        return redirect(url_for("accommodations.list_accommodations"))
    return render_template("accommodations/detail.html", acc=acc)
