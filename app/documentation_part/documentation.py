from ..db_class.db import User
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
# from .form import LoginForm, EditUserFrom
from flask_login import current_user

from . import documentation_core as DocModel
from .. import category_common as CategoryModel
from ..utils.utils import form_to_dict

documentation_blueprint = Blueprint(
    'documentation',
    __name__,
    template_folder='templates',
    static_folder='static'
)



@documentation_blueprint.route("/")
def index():
    session["active_category_doc"] = ""
    session["current_doc"] = ""
    return render_template("documentation/documentation_index.html")

@documentation_blueprint.route("/add_documentation")
def add_documentation():
    session["current_doc"] = ""
    return render_template("documentation/add_documentation.html")

@documentation_blueprint.route("/<did>/edit_view")
def edit_documentation(did):
    session["current_doc"] = did
    return render_template("documentation/add_documentation.html")

@documentation_blueprint.route("/view/<did>")
def view(did):
    session["current_doc"] = did
    return render_template("documentation/documentation_view.html")

@documentation_blueprint.route("/create", methods=['POST'])
def create():
    if "text" in request.json:
        if "title" in request.json:
            d = DocModel.create_doc(request.json)
            if d:
                return {"message": "All good", "toast_class": "success-subtle", "doc_id": d.id}, 200
            return {"message": "Give a category_id, No choice !", "toast_class": "danger-subtle"}, 400
        return {"message": "Give a title, so I can find you !", "toast_class": "danger-subtle"}, 400
    return {"message": "Give a text, now !", "toast_class": "danger-subtle"}, 400

@documentation_blueprint.route("/<did>/edit", methods=['POST'])
def edit(did):
    if DocModel.get_doc(did):
        if "text" in request.json:
            if "title" in request.json:
                d = DocModel.edit_doc(did, request.json)
                if d:
                    return {"message": "All good with modifications", "toast_class": "success-subtle"}, 200
                return {"message": "Give a category_id, No choice !", "toast_class": "danger-subtle"}, 400
            return {"message": "Give a title, so I can find you !", "toast_class": "danger-subtle"}, 400
        return {"message": "Give a text, now !", "toast_class": "danger-subtle"}, 400
    return {"message": "Doc not found", "toast_class": "danger-subtle"}, 404


@documentation_blueprint.route("/add_category", methods=['POST'])
def add_category():
    if "name" in request.json:
        if DocModel.add_category(request.json):
            return {"message": "All good", "toast_class": "success-subtle"}, 200
        return {"message": "Something goes wrong", "toast_class": "danger-subtle"}, 400
    return {"message": "Give a name, now !", "toast_class": "danger-subtle"}, 400

@documentation_blueprint.route("/root_categories", methods=['GET'])
def categories():
    return {"categories": CategoryModel.get_root_categories_json(DocModel.get_categories)}, 200

@documentation_blueprint.route("/category/<cid>", methods=['GET'])
def category_page(cid):
    if DocModel.get_category(cid):
        session["active_category_doc"] = cid
        session["current_doc"] = ""
        return render_template("documentation/category.html")
    return render_template("404.html")

@documentation_blueprint.route("/category/current", methods=['GET'])
def current_category():
    cat = DocModel.get_category(session["active_category_doc"])
    cat_json = cat.to_json()

    command_list = []
    for command in cat.documentations:
        command_list.append(command.to_json())

    cat_json["documentations"] = command_list

    subcat_list = CategoryModel.get_subcategory_json(cat.id, DocModel.get_category)

    cat_json["subcats"] = subcat_list

    return {"category": cat_json}

@documentation_blueprint.route("/category/<cid>/add_sub_category", methods=['POST'])
def add_sub_category(cid):
    if "name" in request.json:
        if DocModel.add_sub_category(cid, request.json):
            return {"message": "All good", "toast_class": "success-subtle"}, 200
        return {"message": "Something goes wrong", "toast_class": "danger-subtle"}, 400
    return {"message": "Give a name, now !", "toast_class": "danger-subtle"}, 400


@documentation_blueprint.route("/category/<cid>/subcategory/<sid>", methods=['GET'])
def subcategory_page(cid, sid):
    if DocModel.get_category(cid):
        if DocModel.get_category(sid):
            session["active_category_doc"] = sid
            session["current_doc"] = ""
            return render_template("command/subcategory.html")
        return render_template("404.html")
    return render_template("404.html")


@documentation_blueprint.route("/subcategory/current", methods=['GET'])
def current_subcategory():
    cat = DocModel.get_category(session["active_category_doc"])
    cat_json = cat.to_json()

    command_list = []
    for command in cat.documentations:
        command_list.append(command.to_json())

    cat_json["documentations"] = command_list

    parent_cat = CategoryModel.get_parent_category(cat.id, DocModel.get_category)

    cat_json["parent_category"] = parent_cat.to_json()

    return {"category": cat_json}



@documentation_blueprint.route("/<did>", methods=['GET'])
def current_doc(did):
    doc = DocModel.get_doc(did)
    if doc:
        return {"doc": doc.to_json()}, 200
    return {"message": "Doc not found", "toast_class": "danger-subtle"}, 404


@documentation_blueprint.route("/current", methods=['GET'])
def current_doc_session():
    doc = DocModel.get_doc(session["current_doc"])
    if doc:
        return {"doc": doc.to_json()}, 200
    return {"message": "Doc not found", "toast_class": "danger-subtle"}, 404


@documentation_blueprint.route("/<did>/delete", methods=['GET'])
def delete(did):
    doc = DocModel.get_doc(did)
    if doc:
        if DocModel.delete_doc(did):
            return {"message": "Doc deleted", "toast_class": "success-subtle"}, 200
        return {"message": "Error Doc deleted", "toast_class": "warning-subtle"}, 400
    return {"message": "Doc not found", "toast_class": "danger-subtle"}, 404

#########
# Files #
#########

@documentation_blueprint.route("/<did>/get_files", methods=['GET'])
def get_files(did):
    doc = DocModel.get_doc(did)
    if doc:
        return {"files": [file.to_json() for file in doc.files]}, 200
    return {"message": "Doc not found", "toast_class": "danger-subtle"}, 404

@documentation_blueprint.route("/<did>/add_files", methods=['POST'])
def add_files(did):
    """Add files to a task"""
    if DocModel.get_doc(did):
        if len(request.files) > 0:
            if DocModel.add_file_core(doc_id=did, files_list=request.files):
                return {"message":"Files added", "toast_class": "success-subtle"}, 200
            return {"message":"Something goes wrong adding files", "toast_class": "danger-subtle"}, 400
        return {"message":"No Files given", "toast_class": "warning-subtle"}, 400
    return {"message":"Doc not found", "toast_class": "danger-subtle"}, 404

@documentation_blueprint.route("/<did>/delete_file/<fid>", methods=['GET'])
def delete_file(did, fid):
    """Delete the file"""
    doc = DocModel.get_doc(did)
    file = DocModel.get_file(fid)
    if file and file in doc.files:
        if DocModel.delete_file(file):
            return {"message": "File Deleted", "toast_class": "success-subtle"}, 200
        return {"message": "Error deleting file", "toast_class": "warning-subtle"}, 400
    return {"message": "File not found", "toast_class": "danger-subtle"}, 404

@documentation_blueprint.route("/<did>/download_file/<fid>", methods=['GET'])
def download_file(did, fid):
    """Download the file"""
    doc = DocModel.get_doc(did)
    file = DocModel.get_file(fid)
    if file and file in doc.files:
        return DocModel.download_file(file)
    return {"message": "File not found", "toast_class": "danger-subtle"}, 404
