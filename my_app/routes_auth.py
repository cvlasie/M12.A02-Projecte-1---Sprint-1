from flask import Blueprint, redirect, render_template, url_for
from flask_login import current_user, login_user, login_required, logout_user
from flask import flash
from . import login_manager
from .models import User
from .forms import LoginForm, RegisterForm
from .helper_role import notify_identity_changed
from . import db_manager as db
from werkzeug.security import generate_password_hash, check_password_hash

# Blueprint
auth_bp = Blueprint(
    "auth_bp", __name__, template_folder="templates", static_folder="static"
)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        plain_text_password = form.password.data

        user = load_user(email)
        if user and check_password_hash(user.password, plain_text_password):
            login_user(user)

            # aquí s'actualitzen els rols que té l'usuari
            notify_identity_changed()
            
            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("main_bp.init"))
        else:
            flash("Credenciales incorrectas. Por favor, inténtelo de nuevo.", "danger")
            return redirect(url_for("auth_bp.login"))

    return render_template('login.html', form=form)

@login_manager.user_loader
def load_user(email):
    if email is not None:
        user_or_none = db.session.query(User).filter(User.email == email).one_or_none()
        return user_or_none
    return None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_bp.login"))

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        existing_user = db.session.query(User).filter_by(name=name).first()
        if existing_user:
            flash("El nombre de usuario ya está en uso. Por favor, elige otro.", "danger")  # Mensaje de error
        else:
            new_user = User(name=name, email=email, password=generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash("Te has registrado con éxito.", "success")  # Mensaje de éxito
            return redirect(url_for("auth_bp.login"))

    return render_template('register.html', form=form)

@auth_bp.route('/profile')
@login_required
def profile():
    # Suposant que 'current_user' és un objecte usuari amb atributs com 'name', 'email', i 'role'
    user_info = {
        "name": current_user.name,
        "email": current_user.email,
        "role": current_user.role
    }
    return render_template('profile.html', user_info=user_info)
