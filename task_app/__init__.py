from flask import Flask
from flask_login import LoginManager
from task_app.db import engine , SessionLocal
from task_app.models.models import Users
from task_app.routes.auth import auth_bp
from task_app.routes.dashboard import dashboard_bp
from task_app.routes.index import main_bp
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from task_app.helpers.context_processors import inject_globals
from task_app.routes.task import task_bp

load_dotenv()
app = Flask(__name__)
app.config.from_object("config.Config")
app.context_processor(inject_globals)
csrf = CSRFProtect(app)


login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # مسیر صفحه لاگین
login_manager.init_app(app)
login_manager.login_message = ''



app.register_blueprint(main_bp , url_prefix='/')
app.register_blueprint(dashboard_bp)
app.register_blueprint(auth_bp,url_prefix='/auth')
app.register_blueprint(task_bp,url_prefix='/task')



@login_manager.user_loader
def load_user(user_id):
    with SessionLocal() as session:
        return session.get(Users, int(user_id))




