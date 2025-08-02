from flask import Blueprint, render_template, url_for, request, flash, redirect
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from task_app.db import SessionLocal
from task_app.forms import RegisterForm, LoginForm
from task_app.models.models import Users

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        with SessionLocal() as session:

            stmt = select(Users).where(Users.email == form.email.data)
            user = session.execute(stmt).scalars().first()

            if not check_password_hash(user.password, form.password.data):
                flash("ایمیل یا رمز عبور اشتباه است", "danger")
                return redirect(request.url)

        login_user(user)

        return redirect(url_for('dashboard.dashboard'))

    return render_template("auth/login.html", page_title="ورود", form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = Users(name=form.username.data, email=form.email.data, password=hashed_password)
        with SessionLocal() as session:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)

        login_user(new_user)

        return redirect(url_for('dashboard.dashboard'))
    return render_template('auth/register.html', form=form, page_title='ثبت نام')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
