from flask import current_app
from flask_login import current_user
from flask_principal import identity_loaded, identity_changed, RoleNeed, Permission, Identity, AnonymousIdentity
from enum import Enum

# Custom roles
class Role(str, Enum):
    admin = "admin"
    wanner = "wanner"

# Needs
__admin_role_need = RoleNeed(Role.admin)
__wanner_role_need = RoleNeed(Role.wanner)

# Permissions
require_admin_role = Permission(__admin_role_need)
require_wanner_role = Permission(__wanner_role_need)

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    identity.user = current_user
    set_user_role(identity)

def set_user_role(identity):
    if hasattr(current_user, 'role'):
        if current_user.role == Role.admin:
            # Role needs
            identity.provides.add(__admin_role_need)
        elif current_user.role == Role.wanner:
            # Role needs
            identity.provides.add(__wanner_role_need)
        else:
            current_app.logger.debug("Unknown role")

def notify_identity_changed():
    if hasattr(current_user, 'email'):
        identity = Identity(current_user.email)
    else:
        identity = AnonymousIdentity()

    set_user_role(identity)
    identity_changed.send(current_app._get_current_object(), identity=identity)
