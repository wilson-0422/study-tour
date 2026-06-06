from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from app.services.insurance_service import InsuranceService
from app.services.registration_service import RegistrationService

insurances_bp = Blueprint("insurances", __name__)


@insurances_bp.route("/insurances")
@login_required
def list_insurances():
    if current_user.is_admin or current_user.is_teacher:
        insurances = InsuranceService.get_all()
    else:
        regs = RegistrationService.get_by_student(current_user.id)
        insurances = []
        for reg in regs:
            ins = InsuranceService.get_by_registration(reg.id)
            if ins:
                insurances.append(ins)
    return render_template("insurances/list.html", insurances=insurances)


@insurances_bp.route("/insurances/create", methods=["GET", "POST"])
@login_required
def create_insurance():
    if not (current_user.is_admin or current_user.is_teacher):
        flash("无权限操作", "danger")
        return redirect(url_for("insurances.list_insurances"))
    if request.method == "POST":
        data = {
            "registration_id": int(request.form.get("registration_id")),
            "provider": request.form.get("provider"),
            "policy_number": request.form.get("policy_number"),
            "coverage_amount": float(request.form.get("coverage_amount")),
            "start_date": datetime.strptime(request.form.get("start_date"), "%Y-%m-%d").date(),
            "end_date": datetime.strptime(request.form.get("end_date"), "%Y-%m-%d").date(),
            "premium": float(request.form.get("premium")),
        }
        InsuranceService.create(data)
        flash("保险创建成功", "success")
        return redirect(url_for("insurances.list_insurances"))
    registrations = RegistrationService.get_all()
    return render_template("insurances/create.html", registrations=registrations)


@insurances_bp.route("/insurances/<int:ins_id>")
@login_required
def insurance_detail(ins_id):
    ins = InsuranceService.get_by_id(ins_id)
    if not ins:
        flash("保险记录不存在", "danger")
        return redirect(url_for("insurances.list_insurances"))
    return render_template("insurances/detail.html", ins=ins)
