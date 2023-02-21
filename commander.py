from commander_core import *

from flask import Flask, render_template, url_for, request, jsonify

import sqlite3

cur = sqlite3.connect('webcommander.db',check_same_thread=False)


FLASK_URL = '127.0.0.1'
FLASK_PORT = 7050

app = Flask(__name__)
# app.debug = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True



@app.route("/")
def index():
    """Home page"""

    categ_list = get_categ_core()
    return render_template("index.html", categ_list=categ_list, len_cat=len(categ_list), cat_name="")

@app.route("/categ_list", methods=['GET'])
def categ():
    """"""

    data_dict = dict(request.args)
    categ_list = get_categ_core()
    cat_name = get_cat_by_id(data_dict["cat"])
    return render_template("index.html", categ_list=categ_list, len_cat=len(categ_list), cat_name=cat_name)

@app.route("/category")
def category():
    """Add Category page"""

    categ_list = get_categ_core()

    return render_template("categ.html", categ_list=categ_list, len_cat=len(categ_list))



@app.route("/create_note", methods=['POST'])
def create_note():
    """Form valid page"""

    note = request.json["note"]
    name_command = request.json["name_command"]
    
    if create_note_core(name_command, note):
        return jsonify({"message": "Note Created"}), 201
    else:
        return jsonify({"message": "Note not created. Something get wrong"}), 400

@app.route("/add_command", methods=['POST'])
def add_command():
    """Form valid page"""

    response_json = request.json
    msg, code = add_command_core(response_json['command'], response_json['category'])

    return jsonify({"message": msg}), code

@app.route("/add_category", methods=['POST'])
def add_category():
    """Add Category page"""

    response_json = request.json
    add_category_core(response_json['category'])

    return jsonify({"message": "Category add"}), 201


@app.route("/delete_command", methods=['POST'])
def delete_command():
    """Delete command page"""

    command = request.json["command"]
    if delete_command_core(command):
        return jsonify({"message": "Command delete"}), 201
    else:
        return jsonify({"message": "Command not delete. Something get wrong"}), 400

@app.route("/delete_category", methods=['POST'])
def delete_category():
    """Delete category form"""

    category = request.json["category"]
    if delete_category_core(category):
        return jsonify({"message": "Category delete"}), 201
    else:
        return jsonify({"message": "Category not delete. Something get wrong"}), 400


@app.route("/get_command", methods=['GET'])
def get_command():
    """Get command page"""

    data_dict = dict(request.args)

    command_list = get_command_core(data_dict)

    return jsonify({"command_list": command_list}), 201

@app.route("/get_category")
def get_category():
    """Get category page"""

    category_list = get_category_core()

    return jsonify({"category_list": category_list}), 201


@app.route("/get_category_list")
def get_category_list():
    """Get category page"""

    category_list = get_categ_core()

    return jsonify({"category_list": category_list}), 201


@app.route("/get_note", methods=['GET'])
def get_note():
    """Get category page"""

    data_dict = dict(request.args)

    note = get_notes_core(data_dict["id"])

    return jsonify({"note": note}), 201


@app.route("/save_note", methods=['POST'])
def save_note():
    """Get category page"""

    note = request.json["note"]
    id = request.json["id_note"]
    
    if save_note_core(id, note):
        return jsonify({"message": "Note Updated"}), 201
    else:
        return jsonify({"message": "Note not updated. Something get wrong"}), 400


@app.route("/run_command", methods=['POST'])
def run_command():
    """Run command page"""

    command = request.json["command"]
    term_num = request.json["terminal"]
    flag = request.json["flag"]

    cur.execute("SELECT id FROM Command WHERE name=?", (command,))

    if not cur:
        return jsonify({"message": "Command Not in db"}), 400
    
    try:
        int(term_num)
    except:
        return jsonify({"message": "Terminal number not valid"}), 400

    run_command_core(command, term_num, flag)

    return jsonify({"message": "Command run"}), 201

if __name__ == "__main__":
    app.run(host=FLASK_URL, port=FLASK_PORT)