from flask import Flask, redirect, render_template, request, session, flash, make_response
from service.InputValidator import InputValidator
from service.hasher import make_hash_from, are_strings_same

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://am_auto:am_auto@localhost:8889/am_auto'
app.config['SQLALCHEMY_ECHO'] = True
app.secret_key = 'TestManipulationThisIsMySecretKeyPleaseDoNotTellItToAnyone'

from models import db, User, Comment, Make


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and are_strings_same(password, user.password):
            session['user_id'] = user.id  #changed from email
            return redirect('/')
        else:
            flash('Invalid email and password combination. Please Try again', 'error')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        if password != verify:
            flash("Passwords must be identical")
            return render_template('register.html')
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, make_hash_from(password))
            db.session.add(new_user)
            db.session.flush()
            db.session.commit()
            session['user_id'] = new_user.id
            flash("You have successfully registered")
            return redirect('/')
        else:
            flash("User already exists")

    return render_template('register.html')


@app.before_request
def require_login():
    login_requirede_routes = ['comments']
    if request.endpoint in login_requirede_routes and 'user_id' not in session:
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
    resp = make_response(render_template("inventory.html"))
    resp.set_cookie("some_cookie",'32')
    resp.set_cookie("some_cookie1",'322')
    return resp


@app.route('/logout')
def logout():
    del session['user_id']
    return redirect('/')


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
    user = User.query.get(session.get('user_id'))
    if request.method == 'POST':
        comment_text = request.form['comment']
        new_comment = Comment(comment_text, user.id)
        db.session.add(new_comment)
        db.session.commit()
    comments = Comment.query.all()
    return render_template('comments.html', comments=comments, userid=user.id)


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

