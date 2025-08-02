from flask import Blueprint, render_template , url_for ,request

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return render_template("index.html")

