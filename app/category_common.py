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
    return [get_category(c.child_id) for c in c_to_c]

def get_subcategory_json(parent_category_id, get_category):
    return [c.to_json() for c in get_subcategory(parent_category_id, get_category)]

def get_parent_category(child_id, get_category):
    c_to_c = Category_To_Category.query.filter_by(child_id=child_id).first()
    return get_category(c_to_c.parent_id)