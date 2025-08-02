import jdatetime
from flask import Blueprint, render_template , url_for ,request
from flask_login import login_required, current_user
from sqlalchemy import select
from werkzeug.utils import redirect

from task_app import SessionLocal
from task_app.forms import createTaskForm
from task_app.models.models import Tasks

task_bp = Blueprint('task', __name__)


@task_bp.route('/create',methods=['POST','GET'])
@login_required
def create():
    form = createTaskForm()
    if form.validate_on_submit():
        deadline = form.deadline.data
        g_date = None
        if deadline:
            g_date = jdatetime.date.fromisoformat(deadline.replace('/', '-')).togregorian()

        new_task = Tasks(user_id=current_user.id,title=form.title.data,description=form.description.data,due_date=g_date)
        with SessionLocal() as session:
            session.add(new_task)
            session.commit()
            session.refresh(new_task)


        return  redirect(url_for("task.list",create=1))

    return render_template("tasks/create.html", page_title="درح کار", form=form)


@task_bp.route('/list')
@login_required
def list():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    with SessionLocal() as session:
        stmt = select(Tasks).where(Tasks.user_id == current_user.id)
        total_tasks = session.execute(stmt).scalars().all()  # لیست کامل تسک‌ها
        total_count = len(total_tasks)
        total_pages = (total_count + per_page - 1) // per_page  # محاسبه تعداد صفحات

        start = (page - 1) * per_page
        end = start + per_page
        result = total_tasks[start:end]

    return render_template(
        "tasks/index.html",
        page_title="لیست کار",
        result=result,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )
