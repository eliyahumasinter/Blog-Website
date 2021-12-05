# Israel Blog

from flask import Flask, render_template, request, redirect, url_for, g, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_basicauth import BasicAuth
from sqlalchemy import desc
from PIL import Image
from datetime import datetime
import os
import urllib.request
import sqlite3
import secrets
from werkzeug.utils import secure_filename
from jinja2 import Environment, FileSystemLoader
from Optimizer import optomize
from Notifier import send_notifications

UPLOAD_FOLDER = 'static/images'

app = Flask(__name__)

app.config['SECRET_KEY'] =  os.environ['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['BASIC_AUTH_USERNAME'] = os.environ['USERNAME']
app.config['BASIC_AUTH_PASSWORD'] = os.environ['PASSWORD']
bootstrap = Bootstrap(app)
basic_auth = BasicAuth(app)
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    image = db.Column(db.PickleType)
    likes = db.Column(db.Integer)
    likers = db.Column(db.PickleType)


def connect_db(database):
    sql = sqlite3.connect(database)
    sql.row_factory = sqlite3.Row
    return sql


def get_db(database):
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db(database)
    return g.sqlite_db


def getPostTitles():
    result = Post.query.with_entities(Post.title).all()
    return result


app.jinja_env.globals.update(optomize=optomize, getPostTitles=getPostTitles)


@app.route("/")
@app.route('/home')
def home():
    content = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template("home.html", posts=content)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/notifications")
def notifications():
    return render_template("notifications.html")


@app.route("/admin")
@basic_auth.required
def admin():
    results = Post.query.all()
    db = get_db('mailinglist.db')
    cur = db.execute('select id, email from emails')
    emails = cur.fetchall()
    return render_template("admin.html", content=results, emails=emails)


@app.route("/goToPost", methods=["POST"])
def goToPost():
    postname = request.form['postname']
    goto = "http://localhost:1234#post-" + postname
    validposts = getPostTitles()
    for title in validposts:
        if postname == title[0]:
            return redirect(goto)
    else:
        return redirect(url_for("home"))


# User Routes
@app.route('/getemail', methods=["POST"])
def getemail():
    try:
        email = request.form['email']
        db = get_db('mailinglist.db')
        db.execute('insert into emails (email) values (?)', [email])
        db.commit()
        flash("Successfully added your email to the notifications list", "success")
    except:
        flash("Something went wrong", "error")
    return redirect(url_for("home"))


@app.route('/likepost/<postID>', methods=["POST"])
def likepost(postID):
    email = request.form['email']
    db = get_db('mailinglist.db')
    cur = db.execute('select email from emails')
    emails = cur.fetchall()
    email_list = []
    for e in emails:
        email_list.append(e[0])
    print(email_list)

    if email not in email_list:
        flash("You must be signed up for notifications to like a post", "error")
        return redirect(url_for("notifications"))
    else:
        db = get_db('site.db')
        cur = db.execute('select likers from post')
        emails = cur.fetchall()
        email_list = []
        for e in emails:
            email_list.append(e[0])
        email_list.append(email)
        print(email_list)
        db.execute(
            'insert into post (likers) values (?)', [email_list])
        db.commit()
    return email

# Admin Routes


@ app.route("/submitnewpost", methods=["POST"])
def submitnewpost():
    title = request.form['title']
    content = request.form['post']
    images = request.files.getlist('picture')
    image_list = []
    try:
        for i in images:
            filename = secure_filename(i.filename)
            i.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_list.append(filename)
    except:
        print("Something went wrong")
    post = Post(title=title, content=content, image=image_list)

    db.session.add(post)
    db.session.commit()
    return redirect(url_for("home"))


@ app.route("/deletepost", methods=["POST"])
def deletepost():
    query_delete = request.form['id']
    db = get_db('site.db')
    db.execute('DELETE from post  where id = (?)', [query_delete])
    db.commit()
    return redirect(url_for("admin"))


@ app.route("/deleteemail", methods=["POST"])
def deleteemail():
    query_delete = request.form['id']
    db = get_db('mailinglist.db')
    db.execute('DELETE from emails  where id = (?)', [query_delete])
    db.commit()
    return redirect(url_for("admin"))


@ app.route('/sendnotifications', methods=["POST"])
def sendnotifications():
    title = request.form['title']
    db = get_db('mailinglist.db')
    cur = db.execute('select email from emails')
    emails = cur.fetchall()
    for email in emails:
        try:
            send_notifications(email[0], title)
        except:
            flash("Something went wrong with " + str(email[0]), "error")
    flash("Successfully sent out the notifications", "success")
    return redirect(url_for("admin"))


if __name__ == '__main__':
    app.run(port=1234, debug=True)
