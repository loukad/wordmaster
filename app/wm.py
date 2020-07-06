import os
import sys
import sqlite3
import flask

from datetime import datetime

from flask import Flask, g, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

class Word(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, unique=True, nullable=False)
    definition = db.Column(db.String, nullable=False)
    added = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, word, definition):
        self.word = word
        self.definition = definition

db.create_all()
db.session.commit()

@app.before_request
def setup_context():
    g.word = Word

def get_definition(word):
    return Word.query.filter(Word.word == word).first()

def insert_definition(word, definition):
    db.session.add(Word(word, definition))
    db.session.commit()

@app.route('/')
@app.route('/add')
def add_word():

    msg_kind = 'info'
    message = ''

    # Check for form parameters
    word = request.values.get('word')
    definition = request.values.get('definition')

    if word:
        # Is the word already in the dictionary?
        previous = Word.query.filter(Word.word == word).first()
        if previous is not None:
            del_url = url_for('delete_word', word=word)
            msg_kind = 'error'
            message = f'Word already exists: {previous.word} &mdash; ' \
                      f'{previous.definition}. ' \
                      f'[<a href="{del_url}">Delete it</a>]'
        else:
            insert_definition(word, definition)
            message = f'Added <em>{word}</em> : {definition} to dictionary'

    return render_template('add.html', msg_kind=msg_kind,
                                       message=message)

@app.route("/view")
def view():
    words = Word.query.order_by(Word.added.desc()).limit(200).all()
    return render_template('view.html', words=words)

@app.route("/view/all")
def view_all():
    words = Word.query.order_by(Word.added.desc()).all()
    return render_template('view.html', words=words)

@app.route("/rand")
def random():
    words = Word.query.order_by(func.random()).limit(1).all()
    return render_template('rand.html', words=words)

@app.route("/delete/<word>")
def delete_word(word):
    msg_kind = 'info'
    message = f'Deleted word <em>{word}</em>'

    found = Word.query.filter(Word.word == word).one()
    if found is None:
        msg_kind = 'error'
        message = f'Could not find word {word} to delete'
    else:
        db.session.delete(found)
        db.session.commit()

    return render_template('add.html', msg_kind=msg_kind, message=message)

