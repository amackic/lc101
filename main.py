from flask import Flask, redirect, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import datetime
from InputValidator import InputValidator


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://am_auto:am_auto@localhost:8889/am_auto'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'TestManipulationThisIsMySecretKeyPleaseDoNotTellItToAnyone'


class Make(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    short_name = db.Column(db.String(80))

    def __init__(self, name, short_name):
        self.name = name
        self.short_name = short_name


class Comment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    owner_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    def __init__(self, text, owner_id):
        self.text = text
        self.owner_id = owner_id


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    comments = db.relationship('Comment', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            # TODO - "remember" that the user has logged in
            return redirect('/')
        else:
            return render_template('login.html', error='invalidLogin')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            flash("You have successfully registered")
            return redirect('/')
        else:
            flash("User already exists")

    return render_template('register.html')


@app.before_request
def require_login():
    print('I am here')
    login_requirede_routes = ['comments']
    if request.endpoint in login_requirede_routes and 'email' not in session:
        return redirect('/login')


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
    print("After that i am here")
    if request.method == 'POST':
        max_price = request.form["price"]
        if InputValidator.is_number(max_price):
            return render_template("/result.html", max_price=max_price)
        print(max_price)
    if request.method == 'GET':
        searchParam = request.args.get("q")
        print(searchParam);
    # all_makes = Make.query.all()
    # return render_template("/search.html", makes=all_makes)
    # print("these are my care makes ", retrieve_all_makes())
    return render_template("/search.html", makes=retrieve_all_makes())
    # return render_template("/search.html", makes = makes)


@app.route("/comments", methods=['GET', 'POST'])
def comments():
    if request.method == 'POST':
        print("this is post")
        comment_text = request.form['comment']
        user = User.query.first()
        new_comment = Comment(comment_text, user.id)
        db.session.add(new_comment)
        db.session.commit()

    if request.method == 'GET':
        print("this is post")
    comments = Comment.query.all()
    print(comments)
    return render_template('comments.html', comments=comments)


def retrieve_all_makes():
    makes = []
    all_makes = Make.query.all()
    for make in all_makes:
        makes.append(make.short_name)
    return makes


@app.route('/delete_comment', methods=['POST'])
def delete_comment():
    comment = Comment.query.get(int(request.form['comment-id']))
    db.session.delete(comment)
    db.session.commit()

    return redirect('/comments')

if __name__ == '__main__':
    app.run()

