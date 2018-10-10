from flask import Flask, flash, redirect, render_template, request, url_for
import json

from datetime import datetime, timedelta

import sys
limit = sys.argv[1]
groups = sys.argv[3:]
times = datetime.strptime(sys.argv[2], "%H%M%S")
delta = datetime.now() + timedelta(hours=times.hour, minutes=times.minute, seconds=times.second)

app = Flask(__name__)
app.config['limit'] = int(limit)
app.config['group'] = [{'group': x} for x in groups]

@app.route('/')
def index():
    now = datetime.now()
    if now < delta:
        return str(delta - now)
    return render_template('index.html', group = app.config['group'])

@app.route("/register", methods=['GET', 'POST'])
def registration():
    limit = app.config['limit']
    name = request.form.get('name_input')
    group = request.form.get('group_select')
    with open("file", "r") as f:
        data = json.load(f)
    if len(data[group]) >= limit:
        return "Limit reached"
    if name not in data[group]:
        data[group].append(name)
        with open("file", "w") as f:
            f.write(json.dumps(data))
        return "You registered sucessfully"
    return "You are already on the list"

@app.route("/results", methods=['POST'])
def results():
    with open("file", "r") as f:
        data = json.load(f)
    var = ""
    for key in sorted(data):
        var += (key + ": " + ", ".join(data[key]) + "<br>")
    return var

if __name__ == "__main__":
    with open("file", "w") as f:
        f.write(json.dumps({x: [] for x in groups}))
    app.run()
