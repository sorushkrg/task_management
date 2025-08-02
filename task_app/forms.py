import re

import jdatetime
from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from task_app.db import SessionLocal
from task_app.models.models import Users


class RegisterForm(FlaskForm):
    username = StringField("نام کاربری", validators=[
        DataRequired(message="نام کاربری را وارد کنید."),
        Length(min=3, max=25, message="نام کاربری باید بین ۳ تا ۲۵ کاراکتر باشد.")
    ])

    email = StringField("ایمیل", validators=[
        DataRequired(message="ایمیل را وارد کنید."),
        Email(message="لطفاً یک ایمیل معتبر وارد کنید.")
    ])

    password = PasswordField("رمز عبور", validators=[
        DataRequired(message="رمز عبور را وارد کنید."),
        Length(min=6, message="رمز عبور باید حداقل ۶ کاراکتر باشد.")
    ])

    confirm_password = PasswordField("تکرار رمز عبور", validators=[
        DataRequired(message="تکرار رمز عبور را وارد کنید."),
        EqualTo('password', message=".رمز عبور و تکرار آن یکسان نیستند.")
    ])

    submit = SubmitField("ثبت‌نام")

    def validate_username(self, field):
     with SessionLocal() as session:

        stmt = select(Users).where(Users.name == field.data)
        result = session.execute(stmt).scalars().first()
        if result:
            raise ValidationError("این نام کاربری قبلاً ثبت شده است.")

    def validate_email(self, field):
        with SessionLocal() as session:

            stmt = select(Users).where(Users.email == field.data)
            result = session.execute(stmt).scalars().first()
            if result:
                raise ValidationError("این ایمیل قبلاً ثبت شده است.")





class LoginForm(FlaskForm):

    email = StringField("ایمیل", validators=[
        DataRequired(message="ایمیل را وارد کنید."),
        Email(message="لطفاً یک ایمیل معتبر وارد کنید.")
    ])

    password = PasswordField("رمز عبور", validators=[
        DataRequired(message="رمز عبور را وارد کنید."),
        Length(min=6, message="رمز عبور باید حداقل ۶ کاراکتر باشد.")
    ])

    submit = SubmitField("ورود")



class createTaskForm(FlaskForm):
    title = StringField("موضوع کار", validators=[
        DataRequired(message="موضوع کار را وارد کنید."),
        Length( max=51, message="موضوع کار  تا 50 کاراکتر باشد.")
    ])

    description = TextAreaField("توضیحات", validators=[
        DataRequired(message="توضیحات را وارد کنید."),
        Length( min=3, message="توضیحات  بیشتر از 3  کاراکتر باشد.")
    ])

    deadline = StringField("تاریخ اتمام کار")

    submit = SubmitField("درج کار")


    def validate_deadline(form, field):
        if field.data:
            if not re.match(r'^\d{4}/\d{2}/\d{2}$', field.data):
                raise ValidationError('فرمت تاریخ باید YYYY/MM/DD باشد.')

            try:
                jdatetime.date.fromisoformat(field.data.replace('/', '-'))
            except ValueError:
                raise ValidationError('تاریخ معتبر نیست.')

