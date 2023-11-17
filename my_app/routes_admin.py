from flask import Blueprint, render_template
from flask_login import login_required, current_user
from .models import User
from .helper_role import require_editor_role, require_admin_or_moderator_role, require_admin_role   # Assegura't d'importar el nou permís
from . import db_manager as db

# Blueprint
admin_bp = Blueprint(
    "admin_bp", __name__, template_folder="templates/admin", static_folder="static"
)

@admin_bp.route('/admin')
@login_required
@require_admin_or_moderator_role.require(http_exception=403)  # Permetre accés a "admin" i "moderator"
def admin_index():
    show_users_button = current_user.role in ['admin', 'moderator']
    return render_template('index.html', show_users_button=show_users_button)

@admin_bp.route('/admin/users')
@login_required
@require_admin_role.require(http_exception=403)  # Només permetre accés a "admin"
def admin_users():
    users = db.session.query(User).all()
    return render_template('users_list.html', users=users, show_users_button=current_user.role == 'admin')