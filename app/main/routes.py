#saul vargas condori 8393710
from flask import Blueprint, render_template, request
from ..models import Anuncio, Categoria
bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    cat = request.args.get("categoria", type=int)
    q = Anuncio.query.order_by(Anuncio.fecha.desc())
    if cat: q = q.filter_by(categoria_id=cat)
    return render_template("index.html", anuncios=q.all(), categorias=Categoria.query.all(), cat=cat)
