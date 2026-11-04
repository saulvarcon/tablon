from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Usuario
bp = Blueprint("usuarios", __name__)

@bp.route("/")
@login_required
def listar():
    return render_template("usuarios/lista.html", usuarios=Usuario.query.all())

@bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def crear():
    if request.method == "POST":
        f = request.form
        if Usuario.query.filter_by(email=f["email"]).first():
            flash("Ese correo ya está registrado.", "danger")
        else:
            u = Usuario(nombre=f["nombre"], email=f["email"]); u.set_password(f["password"])
            db.session.add(u); db.session.commit()
            flash("Usuario creado.", "success")
            return redirect(url_for("usuarios.listar"))
    return render_template("usuarios/form.html", u=None)

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar(id):
    u = db.get_or_404(Usuario, id)
    if request.method == "POST":
        u.nombre = request.form["nombre"]; u.email = request.form["email"]
        if request.form.get("password"): u.set_password(request.form["password"])
        db.session.commit(); flash("Usuario actualizado.", "success")
        return redirect(url_for("usuarios.listar"))
    return render_template("usuarios/form.html", u=u)

@bp.route("/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar(id):
    u = db.get_or_404(Usuario, id)
    if u.id == current_user.id:
        flash("No puedes eliminar tu propia cuenta.", "warning")
    else:
        db.session.delete(u); db.session.commit(); flash("Usuario eliminado.", "success")
    return redirect(url_for("usuarios.listar"))
