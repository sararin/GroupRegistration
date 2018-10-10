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
    return name+group

if __name__ == "__main__":
    app.run()
