#saul vargas condori 8393710
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from ..extensions import db
from ..models import Anuncio, Categoria
bp = Blueprint("anuncios", __name__)

@bp.route("/")
@login_required
def listar():
    return render_template("anuncios/lista.html", anuncios=Anuncio.query.order_by(Anuncio.fecha.desc()).all())

@bp.route("/<int:id>")
def ver(id):
    return render_template("anuncios/detalle.html", a=db.get_or_404(Anuncio, id))

@bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def crear():
    if request.method == "POST":
        f = request.form
        db.session.add(Anuncio(titulo=f["titulo"], descripcion=f["descripcion"],
                               categoria_id=int(f["categoria_id"]), usuario_id=current_user.id))
        db.session.commit(); flash("Anuncio publicado.", "success")
        return redirect(url_for("anuncios.listar"))
    return render_template("anuncios/form.html", a=None, categorias=Categoria.query.all())

@bp.route("/<int:id>/editar", methods=["GET", "POST"])
@login_required
def editar(id):
    a = db.get_or_404(Anuncio, id)
    if request.method == "POST":
        f = request.form
        a.titulo = f["titulo"]; a.descripcion = f["descripcion"]; a.categoria_id = int(f["categoria_id"])
        db.session.commit(); flash("Anuncio actualizado.", "success")
        return redirect(url_for("anuncios.listar"))
    return render_template("anuncios/form.html", a=a, categorias=Categoria.query.all())

@bp.route("/<int:id>/eliminar", methods=["POST"])
@login_required
def eliminar(id):
    db.session.delete(db.get_or_404(Anuncio, id)); db.session.commit()
    flash("Anuncio eliminado.", "success")
    return redirect(url_for("anuncios.listar"))
