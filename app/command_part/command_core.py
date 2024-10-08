import json
import os
from ..db_class.db import *
from .. import db 


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


def add_category(request_json):
    color = ""
    if "color" in request_json:
        color = request_json["color"]
    
    c = Category(
        name=request_json["name"],
        color=color
    )

    db.session.add(c)
    db.session.commit()

    return c

def get_categories():
    return Category.query.all()

def get_root_categories():
    c_list = []
    c_all = get_categories()
    for cat in c_all:
        if not Category_To_Category.query.filter_by(child_id=cat.id).first():
            c_list.append(cat)
    return c_list

def get_categories_json():
    return [cat.to_json() for cat in get_categories()]

def get_root_categories_json():
    return [cat.to_json() for cat in get_root_categories()]

def get_category(cid):
    return Category.query.get(cid)


def add_sub_category(category_id, request_json):
    parent_category = get_category(category_id)
    if parent_category:
        c = add_category(request_json)

        c_to_c = Category_To_Category(
            parent_id=category_id,
            child_id=c.id
        )

        db.session.add(c_to_c)
        db.session.commit()

        return True
    return False

def get_subcategory(parent_category_id):
    c_to_c = Category_To_Category.query.filter_by(parent_id=parent_category_id).all()
    return [get_category(c.child_id) for c in c_to_c]

def get_subcategory_json(parent_category_id):
    return [c.to_json() for c in get_subcategory(parent_category_id)]

def get_parent_category(child_id):
    c_to_c = Category_To_Category.query.filter_by(child_id=child_id).first()
    return get_category(c_to_c.parent_id)


def get_prism_lang():
    with open(os.path.join(os.getcwd(), "app", "./prism-lang.json")) as read_file:
        prism_lang = json.load(read_file)
        return prism_lang