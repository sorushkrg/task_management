from flask import Blueprint, render_template , url_for ,request
from flask_login import login_required

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", page_title="داشبرد")

