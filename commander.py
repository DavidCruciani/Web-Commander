import redis
import subprocess

from flask import Flask, render_template, url_for, request, jsonify

red = redis.Redis(host='localhost', port=6379, db=8)

FLASK_URL = '127.0.0.1'
FLASK_PORT = 7050

app = Flask(__name__)
# app.debug = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True





def run_command_core(command):
    # sudo chown root:root ttyecho && sudo chmod u+s ttyecho

    command_base = ['sudo', './ttyecho', '-n', f"/dev/pts/3"]
    command_base.append(command)

    subprocess.call(command_base)

def delete_command_core(command):
    red.srem("command", command)

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


@app.route("/form_valid", methods=['POST'])
def form_valid():
    """Form valid page"""

    command_name = request.json['command']
    red.sadd("command", command_name)

    return jsonify({"message": "Command add"}), 201


@app.route("/delete_command", methods=['POST'])
def delete_command():
    """Delete command page"""

    command = request.json["command"]
    delete_command_core(command)

    return jsonify({"message": "Command delete"}), 201


@app.route("/get_command", methods=['GET'])
def get_command():
    """Get command page"""

    command_list = get_command_core()

    return jsonify({"command_list": command_list}), 201


@app.route("/run_command", methods=['POST'])
def run_command():
    """Run command page"""

    command = request.json["command"]
    run_command_core(command)

    return jsonify({"message": "Command run"}), 201


if __name__ == "__main__":
    app.run(host=FLASK_URL, port=FLASK_PORT)