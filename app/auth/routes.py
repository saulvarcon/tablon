#saul vargas condori 8393710
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..models import Usuario
bp = Blueprint("auth", __name__)

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = Usuario.query.filter_by(email=request.form["email"].strip()).first()
        if u and u.check_password(request.form["password"]):
            login_user(u)
            return redirect(request.args.get("next") or url_for("main.index"))
        flash("Credenciales incorrectas.", "danger")
    return render_template("auth/login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
