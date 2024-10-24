from .db_class.db import *
from . import db 


##########
# Getter #
##########

def get_categories(is_doc):
    if is_doc:
        return Category_Doc.query.all()
    else:
        return Category.query.all()

def get_category(cid, is_doc):
    if is_doc:
        return Category_Doc.query.get(cid)
    else:
        return Category.query.get(cid)

def get_root_categories(is_doc):
    c_list = []
    c_all = get_categories(is_doc)
    for cat in c_all:
        if is_doc:
            if not Category_To_Category_Doc.query.filter_by(child_id=cat.id).first():
                c_list.append(cat)
        else:
            if not Category_To_Category.query.filter_by(child_id=cat.id).first():
                c_list.append(cat)
    return c_list

def get_categories_json(is_doc):
    return [cat.to_json() for cat in get_categories(is_doc)]

def get_root_categories_json(is_doc):
    return [cat.to_json() for cat in get_root_categories(is_doc)]

def get_subcategory(parent_category_id, is_doc):
    if is_doc:
        c_to_c = Category_To_Category_Doc.query.filter_by(parent_id=parent_category_id).all()
    else:
        c_to_c = Category_To_Category.query.filter_by(parent_id=parent_category_id).all()
    if c_to_c:
        return [get_category(c.child_id, is_doc) for c in c_to_c]
    return []

def get_subcategory_json(parent_category_id, is_doc):
    subcats = get_subcategory(parent_category_id, is_doc)
    print(subcats)
    if subcats:
        return [c.to_json() for c in subcats]
    return []



##########
# Action #
##########

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

def edit_category(cid, request_json, is_doc):
    c = get_category(cid, is_doc)

    c.name = request_json["name"]
    c.color = request_json["color"]
    db.session.commit()
    return True

def delete_category(cid, is_doc):
    c = get_category(cid, is_doc)

    ### Delete all children
    if is_doc:
        c_t_c = Category_To_Category_Doc.query.filter_by(parent_id=cid).all()
    else:
        c_t_c = Category_To_Category.query.filter_by(parent_id=cid).all()
    for loc_c in c_t_c:
        cat_del = get_category(loc_c.child_id, is_doc)
        db.session.delete(cat_del)
        # Category_Doc.query.filter_by(id=loc_c.child_id).delete()
        db.session.delete(loc_c)
        db.session.commit()
    
    ### Delete link to parent
    if is_doc:
        c_t_c = Category_To_Category.query.filter_by(child_id=cid).first()
    else:
        c_t_c = Category_To_Category.query.filter_by(child_id=cid).first()
    if c_t_c:
        db.session.delete(c_t_c)
        db.session.commit()

    db.session.delete(c)
    db.session.commit()
    return True


def add_sub_category(category_id, request_json, is_doc):
    parent_category = get_category(category_id, is_doc)
    if parent_category:
        c = add_category(request_json, is_doc)
        if is_doc:
            c_to_c = Category_To_Category_Doc(
                parent_id=category_id,
                child_id=c.id
            )
        else:
            c_to_c = Category_To_Category(
            parent_id=category_id,
            child_id=c.id
        )

        db.session.add(c_to_c)
        db.session.commit()
    return True