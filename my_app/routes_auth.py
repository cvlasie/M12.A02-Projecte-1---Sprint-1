from flask import Blueprint, redirect, render_template, url_for, flash, request
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from .models import User
from .forms import LoginForm, RegisterForm, ResendVerificationForm
from .helper_role import notify_identity_changed
from . import db_manager as db
from . import mail_manager as mail
import secrets

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

        # Verificar si el correo electrónico ya está en uso
        existing_user = db.session.query(User).filter_by(email=email).first()
        if existing_user:
            flash("El correo electrónico ya está en uso. Por favor, utiliza otro.", "danger")  # Mensaje de error
        else:
            # Generar un token para la verificación del correo electrónico
            token = secrets.token_urlsafe(20)

            # Crear un nuevo usuario en la base de datos con el token y sin verificar
            new_user = User(name=name, email=email, password=generate_password_hash(password, method="sha256"), role="wanner", email_token=token, verified=False)
            db.session.add(new_user)
            db.session.commit()

            # Enviar correo de bienvenida con el enlace de verificación al nuevo usuario
            mail.send_verification_msg(name, email, token)

            flash("Te has registrado con éxito. Se ha enviado un correo electrónico de verificación.", "success")  # Mensaje de éxito
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

@auth_bp.route('/verify/<name>/<email_token>')
def verify_user(name, email_token):
    # Buscar el usuario en la base de datos por nombre y token
    user = User.query.filter_by(name=name, email_token=email_token, verified=False).first()

    if user:
        # Actualizar el campo 'verified' a True
        user.verified = True
        db.session.commit()
        flash('El teu correu electrònic s\'ha verificat correctament. Pots iniciar la sessió ara.', 'success')
        return redirect(url_for('auth_bp.login'))
    else:
        flash('Error en la verificació del correu electrònic. Verifica l\'enllaç o torna a registrar-te.', 'error')
        return redirect(url_for('auth_bp.login'))

@auth_bp.route('/resend', methods=['GET', 'POST'])
def resend_verification():
    form = ResendVerificationForm()

    if form.validate_on_submit():
        email = form.email.data
        user = db.session.query(User).filter_by(email=email).first()

        if user and not user.verified:
            # Si el usuario existe y no está verificado, reenviar el correo de verificación
            mail.send_verification_msg(user.name, user.email, user.email_token)
            flash("Se ha reenviado el correo de verificación.", "success")
            return redirect(url_for('auth_bp.login'))
        else:
            flash("El usuario no existe o ya está verificado.", "danger")

    return render_template('resend_verification.html', form=form)
