#saul vargas condori 8393710
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from ..extensions import db
from ..models import Categoria
bp = Blueprint("categorias", __name__)

@bp.route("/")
@login_required
def listar():
    return render_template("categorias/lista.html", categorias=Categoria.query.all())

@bp.route("/nueva", methods=["GET", "POST"])
@login_required
def crear():
    if request.method == "POST":
        db.session.add(Categoria(nombre=request.form["nombre"], descripcion=request.form["descripcion"]))
        db.session.commit(); flash("Categoría creada.", "success")
        return redirect(url_for("categorias.listar"))
    return render_template("categorias/form.html", c=None)

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar(id):
    c = db.get_or_404(Categoria, id)
    if request.method == "POST":
        c.nombre = request.form["nombre"]; c.descripcion = request.form["descripcion"]
        db.session.commit(); flash("Categoría actualizada.", "success")
        return redirect(url_for("categorias.listar"))
    return render_template("categorias/form.html", c=c)

@bp.route("/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar(id):
    c = db.get_or_404(Categoria, id)
    if c.anuncios:
        flash("No se puede eliminar: tiene anuncios asociados.", "warning")
    else:
        db.session.delete(c); db.session.commit(); flash("Categoría eliminada.", "success")
    return redirect(url_for("categorias.listar"))
