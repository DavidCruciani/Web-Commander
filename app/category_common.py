import json
import os
from .db_class.db import *
from . import db 


def get_root_categories(get_categories):
    c_list = []
    c_all = get_categories()
    for cat in c_all:
        if not Category_To_Category.query.filter_by(child_id=cat.id).first():
            c_list.append(cat)
    return c_list

def get_categories_json(get_categories):
    return [cat.to_json() for cat in get_categories()]

def get_root_categories_json(get_categories):
    return [cat.to_json() for cat in get_root_categories(get_categories)]

def get_subcategory(parent_category_id, get_category):
    c_to_c = Category_To_Category.query.filter_by(parent_id=parent_category_id).all()
    if c_to_c:
        return [get_category(c.child_id) for c in c_to_c]
    return []

def get_subcategory_json(parent_category_id, get_category):
    subcats = get_subcategory(parent_category_id, get_category)
    if subcats:
        return [c.to_json() for c in subcats]
    return []

def get_parent_category(child_id, get_category):
    c_to_c = Category_To_Category.query.filter_by(child_id=child_id).first()
    return get_category(c_to_c.parent_id)


def add_category(request_json, is_doc):
    color = ""
    if "color" in request_json:
        color = request_json["color"]
    
    if is_doc:
        c = Category_Doc(
            name=request_json["name"],
            color=color
        )
    else: 
        c = Category(
            name=request_json["name"],
            color=color
        )

    db.session.add(c)
    db.session.commit()

    return c

def add_sub_category(category_id, request_json, is_doc, get_category):
    parent_category = get_category(category_id)
    if parent_category:
        c = add_category(request_json, is_doc)

        c_to_c = Category_To_Category(
            parent_id=category_id,
            child_id=c.id
        )

        db.session.add(c_to_c)
        db.session.commit()

        return True
    return False

