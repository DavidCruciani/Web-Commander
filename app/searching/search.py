from flask import Blueprint, render_template, request
from flask_login import login_required

from . import search_core as SearchModel


search_blueprint = Blueprint(
    'search',
    __name__,
    template_folder='templates',
    static_folder='static'
)



@search_blueprint.route("/")
@login_required
def index():
    return render_template("searching/search_page.html")

@search_blueprint.route("/doc", methods=["POST"])
@login_required
def doc():
    title = request.json["title"]
    docs = SearchModel.search_in_docs_title(title)
    return {"results": {"docs": docs}}, 200

@search_blueprint.route("/command", methods=["POST"])
@login_required
def command():
    title = request.json["title"]
    commands = SearchModel.search_in_commands_title(title)
    return {"results": {"commands": commands}}, 200

@search_blueprint.route("/all", methods=["POST"])
@login_required
def all():
    title = request.json["title"]
    docs = SearchModel.search_in_docs_title(title)
    commands = SearchModel.search_in_commands_title(title)
    return {"results": {"docs": docs, "commands": commands}}, 200

