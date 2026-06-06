from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.services.mentor_service import MentorService

mentors_bp = Blueprint("mentors", __name__)


@mentors_bp.route("/mentors")
@login_required
def list_mentors():
    mentors = MentorService.get_all()
    return render_template("mentors/list.html", mentors=mentors)


@mentors_bp.route("/mentors/<int:mentor_id>")
@login_required
def mentor_detail(mentor_id):
    mentor = MentorService.get_by_id(mentor_id)
    if not mentor:
        flash("导师不存在", "danger")
        return redirect(url_for("mentors.list_mentors"))
    return render_template("mentors/detail.html", mentor=mentor)


@mentors_bp.route("/mentors/<int:mentor_id>/evaluate", methods=["GET", "POST"])
@login_required
def evaluate_mentor(mentor_id):
    mentor = MentorService.get_by_id(mentor_id)
    if not mentor:
        flash("导师不存在", "danger")
        return redirect(url_for("mentors.list_mentors"))
    if request.method == "POST":
        score = float(request.form.get("score"))
        if score < 0 or score > 10:
            flash("评分范围为0-10", "danger")
            return render_template("mentors/evaluate.html", mentor=mentor)
        MentorService.evaluate(mentor_id, score)
        flash("考核评分成功", "success")
        return redirect(url_for("mentors.mentor_detail", mentor_id=mentor_id))
    return render_template("mentors/evaluate.html", mentor=mentor)
