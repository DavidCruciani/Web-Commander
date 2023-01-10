import redis
import subprocess
import datetime

from flask import Flask, render_template, url_for, request, jsonify

red = redis.Redis(host='localhost', port=6379, db=8)

FLASK_URL = '127.0.0.1'
FLASK_PORT = 7050

app = Flask(__name__)
# app.debug = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True





def run_command_core(command, term_num):
    # sudo chown root:root ttyecho && sudo chmod u+s ttyecho

    command_base = ['sudo', './ttyecho', '-n', f"/dev/pts/{term_num}"]
    command_base.append(command)

    subprocess.call(command_base)

def delete_command_core(command):
    return red.srem("command", command)

def get_command_core():
    command_list = list()
    for c in red.smembers("command"):
        command_list.append(c.decode())

    return command_list


@app.route("/")
def index():
    """Home page"""

    command_list = get_command_core()
    return render_template("index.html", command_list=command_list)


@app.route("/add_command", methods=['POST'])
def add_command():
    """Form valid page"""

    command_name = request.json['command']
    red.sadd("command", command_name.rstrip())

    return jsonify({"message": "Command add"}), 201


@app.route("/delete_command", methods=['POST'])
def delete_command():
    """Delete command page"""

    command = request.json["command"]
    if delete_command_core(command):
        return jsonify({"message": "Command delete"}), 201
    else:
        return jsonify({"message": "Command not delete. Something get wrong"}), 400


@app.route("/get_command", methods=['GET'])
def get_command():
    """Get command page"""

    command_list = get_command_core()

    return jsonify({"command_list": command_list}), 201


@app.route("/run_command", methods=['POST'])
def run_command():
    """Run command page"""

    command = request.json["command"]
    term_num = request.json["terminal"]

    if not red.sismember("command", command):
        return jsonify({"message": "Command Not in db"}), 400
    
    try:
        int(term_num)
    except:
        return jsonify({"message": "Terminal number not valid"}), 400

    run_command_core(command, term_num)

    return jsonify({"message": "Command run"}), 201


if __name__ == "__main__":
    app.run(host=FLASK_URL, port=FLASK_PORT)