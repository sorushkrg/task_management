import jdatetime
from flask import Blueprint, render_template , url_for ,request
from flask_login import login_required, current_user
from sqlalchemy import select
from werkzeug.utils import redirect

from task_app import SessionLocal
from task_app.forms import createTaskForm
from task_app.models.models import Tasks
from task_app.utils.hashid import decode_id

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



@task_bp.route('/edit/<task_id>', methods=['GET', 'POST'])
@login_required
def edit(task_id):

    real_id = decode_id(task_id)

    if not real_id:
        return redirect(url_for("task.list", edit=1))

    with SessionLocal() as session:
        stmt = select(Tasks).where(
            Tasks.id == real_id,
            Tasks.user_id == current_user.id
        )
        task = session.execute(stmt).scalar_one_or_none()

        if not task:
            return redirect(url_for('task.list'))

        form = createTaskForm(obj=task)

        if request.method == 'GET' and task.due_date:
            form.deadline.data = jdatetime.date.fromgregorian(date=task.due_date).isoformat().replace('-', '/')

        if form.validate_on_submit():

            deadline = form.deadline.data
            g_date = None
            if deadline:
                jalali_str = deadline.replace('/', '-')
                jalali_date = jdatetime.date.fromisoformat(jalali_str)
                g_date = jalali_date.togregorian()


            task.title = form.title.data
            task.description = form.description.data
            task.due_date = g_date

            session.commit()
            return redirect(url_for("task.list", edit=1))

    return render_template(
        "tasks/edit.html",
        page_title="ویرایش تسک",
        form=form,
        task=task
    )


@task_bp.route('/delete/<task_id>', methods=['POST', 'GET'])
@login_required
def delete(task_id):

    real_id = decode_id(task_id)

    if not real_id:
        return redirect(url_for("task.list"))


    with SessionLocal() as session:
        stmt = select(Tasks).where(Tasks.id == real_id, Tasks.user_id == current_user.id)
        task = session.execute(stmt).scalar_one_or_none()

        if not task:
            return redirect(url_for("task.list"))

        session.delete(task)
        session.commit()


    return redirect(url_for('task.list', delete=1))



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
