from flask import Flask, render_template, request
import datetime

from InputValidator import InputValidator


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    now = 11
    if now >= 12:
        return render_template('about.html', current_hour=str(now))
    else:
        return render_template('about.html',current_hour="")


@app.route("/specials")
def specials():
    return render_template("specials.html")
    
@app.route("/inventory")
def inventory():
    return render_template("inventory.html")

@app.route("/search", methods=['POST', 'GET'])
def search():

    makes=[
        'Any Make', 'Alfa Romeo', 'AMC', 'Aston Martin', 'Audi', 'Bentley', 'BMW', 'Bugatti', 'Buick', 'Cadillac', 'Chevrolet', 'Chrysler', 'Daewoo',
        'Datsun', 'DeLorean', 'Dodge', 'Eagle', 'Ferrari', 'FIAT', 'Fisker', 'Ford', 'Freightliner', 'Genesis', 'Geo', 'GMC', 'Honda', 'HUMMER',
        'Hyundai', 'INFINITI', 'Isuzu', 'Jaguar', 'Jeep', 'Kia', 'Lamborghini', 'Land Rover', 'Lexus', 'Lincoln', 'Lotus', 'Maserati', 'Maybach', 'Mazda', 'McLaren',
        'Mercedes-Benz', 'Mercury', 'MINI', 'Mitsubishi', 'Nissan', 'Oldsmobile', 'Plymouth', 'Pontiac', 'Porsche', 'RAM', 'Rolls-Royce', 'Saab', 'Saturn', 'Scion',
        'smart', 'SRT', 'Subaru', 'Suzuki', 'Tesla', 'Toyota', 'Volkswagen', 'Volvo', 'Yugo']

    if request.method == 'POST':
        max_price = request.form["price"]
        if InputValidator.is_number(max_price):
            return render_template("/result.html", max_price=max_price)
        # print(searchParam)
        print(max_price)
    if request.method == 'GET':
        searchParam = request.args.get("q")
        print(searchParam);

    return render_template("/search.html", makes=makes)

app.run()
