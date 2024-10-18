import datetime
import json
import os
import shutil
import uuid
import zipfile
from ..db_class.db import *
from .. import db 
from .. import category_common as CategoryModel
from flask import session, request, send_file
from werkzeug.utils import secure_filename
from ..utils.utils import create_specific_dir

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
TEMP_FOLDER = os.path.join(os.getcwd(), "temp")
FILE_FOLDER = os.path.join(UPLOAD_FOLDER, "files")

def add_category(request_json):
    color = ""
    if "color" in request_json:
        color = request_json["color"]
    
    c = Category_Doc(
        name=request_json["name"],
        color=color
    )

    db.session.add(c)
    db.session.commit()

    return c

def edit_category(cid, request_json):
    c = get_category(cid)

    c.name = request_json["name"]
    c.color = request_json["color"]
    db.session.commit()
    return True

def delete_category(cid):
    c = get_category(cid)

    ### Delete all children
    c_t_c = Category_To_Category.query.filter_by(parent_id=cid).all()
    for loc_c in c_t_c:
        cat_del = get_category(loc_c.child_id)
        db.session.delete(cat_del)
        # Category_Doc.query.filter_by(id=loc_c.child_id).delete()
        db.session.delete(loc_c)
        db.session.commit()
    
    ### Delete link to parent
    c_t_c = Category_To_Category.query.filter_by(child_id=cid).first()
    if c_t_c:
        db.session.delete(c_t_c)
        db.session.commit()

    db.session.delete(c)
    db.session.commit()
    return True


def get_categories():
    return Category_Doc.query.all()

def get_category(cid):
    return Category_Doc.query.get(cid)

def get_doc(did):
    return Documentation.query.get(did)

def get_file(fid):
    """Return a file"""
    return File.query.get(fid)

def create_doc(request_json):
    description = ""
    if "description" in request_json:
        description = request_json["description"]
    
    d = Documentation(
        text="",
        description = description,
        title = request_json["title"],
        category_id=session["active_category_doc"],
        creation_date=datetime.datetime.now(tz=datetime.timezone.utc),
        last_modif=datetime.datetime.now(tz=datetime.timezone.utc)
    )
    db.session.add(d)
    db.session.commit()

    return d

def edit_doc(did, request_json):
    doc = get_doc(did)
    if doc.title != request_json["title"]:
        doc.title = request_json["title"]

    if doc.description != request_json["description"]:
        doc.description = request_json["description"]

    doc.last_modif = datetime.datetime.now(tz=datetime.timezone.utc)

    db.session.commit()

    return True

def edit_doc_text(did, request_json):
    doc = get_doc(did)

    doc.text = request_json["text"]
    doc.last_modif = datetime.datetime.now(tz=datetime.timezone.utc)

    db.session.commit()

    return True

def delete_doc(did):
    doc = get_doc(did)
    for file in doc.files:
        try:
            os.remove(os.path.join(FILE_FOLDER, file.uuid))
        except:
            return False
        db.session.delete(file)
        db.session.commit()
    db.session.delete(doc)
    return True

def download_all(did):
    doc = get_doc(did)
    create_specific_dir(TEMP_FOLDER)
    zf = zipfile.ZipFile(os.path.join(TEMP_FOLDER, f'{doc.title.replace(" ", "_")}.zip'), mode="w")
    try:
        for file in doc.files:
            zf.write(os.path.join(FILE_FOLDER, file.uuid), file.name, compress_type=zipfile.ZIP_DEFLATED)
        zf.writestr(f'{doc.title.replace(" ", "_")}.md', doc.text,compress_type=zipfile.ZIP_DEFLATED)

    except FileNotFoundError:
        return False
    finally:
        zf.close()
    
    return True

def download_zip(doc_title):
    return send_file(os.path.join(TEMP_FOLDER, f'{doc_title.replace(" ", "_")}.zip'), as_attachment=True)

def delete_temp_folder():
    """Delete temp folder"""
    shutil.rmtree(TEMP_FOLDER)

#########
# Files #
#########

def add_file_core(doc_id, files_list):
    create_specific_dir(UPLOAD_FOLDER)
    create_specific_dir(FILE_FOLDER)

    for file in files_list:
        if files_list[file].filename:
            uuid_loc = str(uuid.uuid4())
            filename = secure_filename(files_list[file].filename)
            try:
                file_data = request.files[file].read()
                with open(os.path.join(FILE_FOLDER, uuid_loc), "wb") as write_file:
                    write_file.write(file_data)
            except Exception as e:
                print(e)
                return False

            f = File(
                name=filename,
                doc_id=doc_id,
                uuid = uuid_loc
            )
            db.session.add(f)
            db.session.commit()
    return True

def delete_file(file):
    """Delete a file"""
    try:
        os.remove(os.path.join(FILE_FOLDER, file.uuid))
    except:
        return False

    db.session.delete(file)
    db.session.commit()
    return True

def download_file(file):
    """Download a file"""
    return send_file(os.path.join(FILE_FOLDER, file.uuid), as_attachment=True, download_name=file.name)
