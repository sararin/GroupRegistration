from flask import Flask, flash, redirect, render_template, request, url_for
import json

from datetime import datetime, timedelta

import sys
limit = sys.argv[1]   #maximum amount of students per group
groups = sys.argv[3:] #groups that will exist
times = datetime.strptime(sys.argv[2], "%Hi:%M:%S") #gets in how many hours registration should start
delta = datetime.now() + timedelta(hours=times.hour, minutes=times.minute, seconds=times.second) 

app = Flask(__name__) #init of application, adds config, so both groups and limit will appear correctly
app.config['limit'] = int(limit) 
app.config['group'] = [{'group': x} for x in groups]

@app.route('/')
def index(): #opens the access to website after certain period of time
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
    if name not in data[group]: #part that checks if student already registered in that group
        data[group].append(name)
        with open("file", "w") as f:
            f.write(json.dumps(data))
        return "You registered sucessfully"
    return "You are already on the list"

@app.route("/results", methods=['POST'])
def results():
    with open("file", "r") as f:
        data = json.load(f)
    var = "" #ugly and hacky way of showing the results of
    for key in sorted(data):
        var += (key + ": " + ", ".join(data[key]) + "<br>")
    return var

if __name__ == "__main__":
    with open("file", "w") as f: #create empty file with skeletal JSON
        f.write(json.dumps({x: [] for x in groups}))
    app.run()
