from flask import current_app
from flask_login import current_user
from flask_principal import identity_loaded, identity_changed, ActionNeed, Permission, Identity, AnonymousIdentity
from enum import Enum

# Custom roles and actions
class Role(str, Enum):
    editor = "editor"
    viewer = "viewer"
    moderator = "moderator"
    admin = "admin"
    wanner = "wanner"

class Action(str, Enum):
    edit = "create, update and delete"
    view = "list and read"

# Needs
__editor_role_need = ActionNeed(Role.editor)
__viewer_role_need = ActionNeed(Role.viewer)
__moderator_role_need = ActionNeed(Role.moderator)
__admin_role_need = ActionNeed(Role.admin)
__wanner_role_need = ActionNeed(Role.wanner)

__edit_action_need = ActionNeed(Action.edit)
__view_action_need = ActionNeed(Action.view)

require_admin_or_moderator_role = Permission(__admin_role_need, __moderator_role_need, __edit_action_need, __view_action_need)

# Permissions
require_editor_role = Permission(__editor_role_need)
require_viewer_role = Permission(__viewer_role_need)
require_admin_role = Permission(__admin_role_need)
require_wanner_role = Permission(__wanner_role_need)

require_edit_permission = Permission(__edit_action_need)
require_view_permission = Permission(__view_action_need)

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    identity.user = current_user
    set_user_role(identity)

def set_user_role(identity):
    if hasattr(current_user, 'role'):
        if current_user.role == Role.editor:
            # Role needs
            identity.provides.add(__editor_role_need)
            # Action needs
            identity.provides.add(__edit_action_need)
            identity.provides.add(__view_action_need)
        elif current_user.role == Role.viewer:
            # Role needs
            identity.provides.add(__viewer_role_need)
            # Action needs
            identity.provides.add(__view_action_need)
        elif current_user.role == Role.moderator:
            identity.provides.add(__moderator_role_need)
            identity.provides.add(__edit_action_need)
            identity.provides.add(__view_action_need)
        elif current_user.role == Role.admin:
            identity.provides.add(__admin_role_need)
            identity.provides.add(__edit_action_need)
            identity.provides.add(__view_action_need)
        elif current_user.role == Role.wanner:
            identity.provides.add(__wanner_role_need)
            # Add any additional needs for the 'wanner' role
        else:
            current_app.logger.debug("Unknown role")

def notify_identity_changed():
    if hasattr(current_user, 'email'):
        identity = Identity(current_user.email)
    else:
        identity = AnonymousIdentity()

    set_user_role(identity)
    identity_changed.send(current_app._get_current_object(), identity=identity)
