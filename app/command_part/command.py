from flask import Blueprint, render_template, redirect, url_for, request, flash, session
# from .form import LoginForm, EditUserFrom
from flask_login import current_user

from . import command_core as CommandModel
from ..utils.utils import form_to_dict

command_blueprint = Blueprint(
    'command',
    __name__,
    template_folder='templates',
    static_folder='static'
)



@command_blueprint.route("/")
def index():
    session["active_category"] = ""
    return render_template("command/command_index.html")

@command_blueprint.route("/create_page")
def create_page():
    return render_template("command/create_command.html")

@command_blueprint.route("/create_command", methods=['POST'])
def create_command():
    if "command" in request.json:
        if "title" in request.json:
            if "category_id" in request.json:
                if "lang" in request.json:
                    if CommandModel.create_command(request.json):
                        return {"message": "All good", "toast_class": "success-subtle"}, 200
                    return {"message": "Something goes wrong", "toast_class": "danger-subtle"}, 400
                return {"message": "Give a lang, Python forever !", "toast_class": "danger-subtle"}, 400
            return {"message": "Give a category_id, No choice !", "toast_class": "danger-subtle"}, 400
        return {"message": "Give a title, so I can find you !", "toast_class": "danger-subtle"}, 400
    return {"message": "Give a command, now !", "toast_class": "danger-subtle"}, 400

@command_blueprint.route("/add_category", methods=['POST'])
def add_category():
    if "name" in request.json:
        if CommandModel.add_category(request.json):
            return {"message": "All good", "toast_class": "success-subtle"}, 200
        return {"message": "Something goes wrong", "toast_class": "danger-subtle"}, 400
    return {"message": "Give a name, now !", "toast_class": "danger-subtle"}, 400

@command_blueprint.route("/root_categories", methods=['GET'])
def categories():
    return {"categories":CommandModel.get_root_categories_json()}, 200

@command_blueprint.route("/category/<cid>", methods=['GET'])
def category_page(cid):
    if CommandModel.get_category(cid):
        session["active_category"] = cid
        return render_template("command/category.html")
    return render_template("404.html")


@command_blueprint.route("/category/current", methods=['GET'])
def current_category():
    cat = CommandModel.get_category(session["active_category"])
    cat_json = cat.to_json()

    command_list = []
    for command in cat.commands:
        command_list.append(command.to_json())

    cat_json["commands"] = command_list

    subcat_list = CommandModel.get_subcategory_json(cat.id)

    cat_json["subcats"] = subcat_list

    return {"category": cat_json}

@command_blueprint.route("/category/<cid>/add_sub_category", methods=['POST'])
def add_sub_category(cid):
    if "name" in request.json:
        if CommandModel.add_sub_category(cid, request.json):
            return {"message": "All good", "toast_class": "success-subtle"}, 200
        return {"message": "Something goes wrong", "toast_class": "danger-subtle"}, 400
    return {"message": "Give a name, now !", "toast_class": "danger-subtle"}, 400


@command_blueprint.route("/category/<cid>/subcategory/<sid>", methods=['GET'])
def subcategory_page(cid, sid):
    if CommandModel.get_category(cid):
        if CommandModel.get_category(sid):
            session["active_category"] = sid
            return render_template("command/subcategory.html")
        return render_template("404.html")
    return render_template("404.html")


@command_blueprint.route("/subcategory/current", methods=['GET'])
def current_subcategory():
    cat = CommandModel.get_category(session["active_category"])
    cat_json = cat.to_json()

    command_list = []
    for command in cat.commands:
        command_list.append(command.to_json())

    cat_json["commands"] = command_list

    parent_cat = CommandModel.get_parent_category(cat.id)

    cat_json["parent_category"] = parent_cat.to_json()

    return {"category": cat_json}


@command_blueprint.route("/prism-lang", methods=['GET'])
def prism_lang():
    return CommandModel.get_prism_lang()
