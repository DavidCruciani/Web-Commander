from flask import Blueprint, render_template, redirect, url_for, request, flash, session
# from .form import LoginForm, EditUserFrom
from flask_login import login_required

from . import command_core as CommandModel
from .. import category_common as CategoryModel

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

@command_blueprint.route("/<cid>/edit_command", methods=['POST'])
def edit_command(cid):
    if "command" in request.json:
        if "title" in request.json:
            if "lang" in request.json:
                if CommandModel.edit_command(cid, request.json):
                    return {"message": "All good", "toast_class": "success-subtle"}, 200
                return {"message": "Something goes wrong", "toast_class": "danger-subtle"}, 400
            return {"message": "Give a lang, Python forever !", "toast_class": "danger-subtle"}, 400
        return {"message": "Give a title, so I can find you !", "toast_class": "danger-subtle"}, 400
    return {"message": "Give a command, now !", "toast_class": "danger-subtle"}, 400

@command_blueprint.route("/<cid>/delete", methods=['GET'])
def delete_command(cid):
    if CommandModel.get_command(cid):
        if CommandModel.delete_command(cid):
            return {"message": "Command deleted", "toast_class": "success-subtle"}, 200
        return {"message": "Command not deleted, Error...Error...", "toast_class": "warning-subtle"}, 400
    return {"message": "Command not found", "toast_class": "danger-subtle"}, 404

@command_blueprint.route("/category/<cid>/commands", methods=['GET'])
def commands(cid):
    cat = CategoryModel.get_category(cid, is_doc=False)
    if cat:
        return {"commands": [c.to_json() for c in cat.commands]}
    return {"message": "Category not found", "toast_class": "danger-subtle"}, 404


############
# Category #
############

@command_blueprint.route("/category/<cid>/edit", methods=['POST'])
def edit_category(cid):
    if CategoryModel.get_category(cid, is_doc=False):
        if "name" in request.json:
            if CategoryModel.edit_category(cid, request.json, is_doc=False):
                return {"message": "All good", "toast_class": "success-subtle"}, 200
            return {"message": "Something went wrong", "toast_class": "danger-subtle"}, 400
        return {"message": "Give a name, now !", "toast_class": "danger-subtle"}, 400
    return {"message": "Category not found", "toast_class": "danger-subtle"}, 404

@command_blueprint.route("/category/<cid>/delete", methods=['GET'])
def delete_category(cid):
    if CategoryModel.get_category(cid, is_doc=False):
        if CategoryModel.delete_category(cid, is_doc=False):
            return {"message": "All good", "toast_class": "success-subtle"}, 200
        return {"message": "Something went wrong", "toast_class": "danger-subtle"}, 400
    return {"message": "Category not found", "toast_class": "danger-subtle"}, 404

@command_blueprint.route("/add_category", methods=['POST'])
def add_category():
    if "name" in request.json:
        if CategoryModel.add_category(request.json, is_doc=False):
            return {"message": "All good", "toast_class": "success-subtle"}, 200
        return {"message": "Something goes wrong", "toast_class": "danger-subtle"}, 400
    return {"message": "Give a name, now !", "toast_class": "danger-subtle"}, 400

@command_blueprint.route("/root_categories", methods=['GET'])
def categories():
    return {"categories":CategoryModel.get_root_categories_json(is_doc=False)}, 200

@command_blueprint.route("/category/<cid>", methods=['GET'])
def category_page(cid):
    if CategoryModel.get_category(cid, is_doc=False):
        session["active_category"] = cid
        return render_template("command/category.html")
    return render_template("404.html")


@command_blueprint.route("/category/current", methods=['GET'])
def current_category():
    cat = CategoryModel.get_category(session["active_category"], is_doc=False)
    cat_json = cat.to_json()

    command_list = []
    for command in cat.commands:
        command_list.append(command.to_json())

    cat_json["commands"] = command_list

    subcat_list = CategoryModel.get_subcategory_json(cat.id, is_doc=False)
    cat_json["subcats"] = subcat_list

    return {"category": cat_json}

@command_blueprint.route("/category/<cid>/add_sub_category", methods=['POST'])
def add_sub_category(cid):
    if "name" in request.json:
        if CategoryModel.add_sub_category(cid, request.json, is_doc=False):
            return {"message": "All good", "toast_class": "success-subtle"}, 200
        return {"message": "Something went wrong", "toast_class": "danger-subtle"}, 400
    return {"message": "Give a name, now !", "toast_class": "danger-subtle"}, 400

@command_blueprint.route("/prism-lang", methods=['GET'])
def prism_lang():
    return CommandModel.get_prism_lang()
