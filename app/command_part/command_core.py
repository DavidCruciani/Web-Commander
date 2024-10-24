import json
import os
from ..db_class.db import *
from .. import db 

def get_command(cid):
    return Command.query.get(cid)


def create_command(request_json):
    description = ""
    if "description" in request_json:
        description = request_json["description"]

    c = Command(
        text=request_json["command"],
        description = description,
        title=request_json["title"],
        category_id=request_json["category_id"],
        lang=request_json["lang"]
    )

    db.session.add(c)
    db.session.commit()

    return True

def edit_command(cid, request_json):
    command = get_command(cid)
    if command:
        command.title = request_json["title"]
        command.description = request_json["description"]
        command.text = request_json["text"]
        command.lang = request_json["lang"]
        db.session.commit()
        return True
    return False

def delete_command(cid):
    command = get_command(cid)
    db.session.delete(command)
    return True

def get_prism_lang():
    with open(os.path.join(os.getcwd(), "app", "./prism-lang.json")) as read_file:
        prism_lang = json.load(read_file)
        return prism_lang