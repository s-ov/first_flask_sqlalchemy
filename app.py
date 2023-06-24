from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# 'SQLALCHEMY_DATABASE_URI' - constant that define db location
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

# it is for python console
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# connect db to app
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # it bind these two tables with the foreign key
    profiles = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f"users {self.id}"


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    old = db.Column(db.Integer)
    city = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<profiles {self.id}>"


@app.route("/")
def index():
    info = []
    try:
        info = Users.query.all()
    except:
        print("Error while reading from db.")
    return render_template('index.html', title="Main page", list_=info)


@app.route("/register", methods=("POST", "GET"))
def register():
    if request.method == "POST":
        """here data must be checked out"""
        try:
            hash_ = generate_password_hash(request.form['psw'])
            user = Users(email=request.form['email'], psw=hash_)
            db.session.add(user)                    # adds new data to session(keeps data in RAM)
            db.session.flush()                      # adds new data in db(moves data from RAM in db)

            profile = Profiles(name=request.form['name'], old=request.form['old'],
                               city=request.form['city'], user_id=user.id)
            db.session.add(profile)
            db.session.commit()
        except:
            db.session.rollback()
            print("Error while adding in db.")
    return render_template('register.html', title="Registration")


if __name__ == '__main__':
    app.run(debug=True)
