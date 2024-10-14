from .. import db
from ..db_class.db import User, Role
from ..utils.utils import generate_api_key

def get_all_roles():
    """Return all roles"""
    return Role.query.all()

def get_user(id):
    """Return the user"""
    return User.query.get(id)


def edit_user_core(form_dict, id):
    """Edit the user to the DB"""
    user = get_user(id)

    user.first_name=form_dict["first_name"]
    user.last_name=form_dict["last_name"]
    user.email=form_dict["email"]
    if "password" in form_dict and form_dict["password"]:
        user.password=form_dict["password"]

    db.session.commit()

def add_user_core(form_dict):
    """Add a user to the DB"""
    user = User(
        first_name=form_dict["first_name"],
        last_name=form_dict["last_name"],
        email=form_dict["email"],
        password=form_dict["password"],
        # role_id = form_dict["role"],
        api_key = generate_api_key()
    )
    db.session.add(user)
    db.session.commit()

    return user
