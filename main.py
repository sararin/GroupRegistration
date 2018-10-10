from flask import Flask, flash, redirect, render_template, request, url_for
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', group = [{'group': "K1"}, {'group': "K2"}])

@app.route("/register", methods=['GET', 'POST'])
def registration():
    name = request.form.get('name_input')
    group = request.form.get('group_select')
    with open("file", "r") as f:
        data = json.load(f)
    if name not in data[group]:
        data[group].append(name)
        with open("file", "w") as f:
            f.write(json.dumps(data))
        return "You registered sucessfully"
    return "You are already on the list"

if __name__ == "__main__":
    with open("file", "w") as f:
        f.write(json.dumps({"K1":[], "K2":[]}))
    app.run()
