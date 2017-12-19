from flask import Flask, render_template, request

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return "World"

@app.route("/inventory")
def inventory():
    return render_template("inventory.html")

@app.route("/search", methods=['POST', 'GET'])
def search():
    searchParam = "nothing"
    if request.method == 'POST':
        searchParam = request.form["carType"]
        print(searchParam)

    if request.method == 'GET':
        searchParam = request.args.get("q")
        print(searchParam);

    return render_template("/search.html")

app.run()
