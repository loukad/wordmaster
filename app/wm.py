import os
import sys
import sqlite3
import flask
from flask import Flask,render_template,request

app = Flask(__name__)

def get_conn():
    if not hasattr(flask.g, 'dbconn'):
        flask.g.dbconn = sqlite3.connect('words.db')
    c = flask.g.dbconn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS words('
              'word TEXT PRIMARY KEY,'
              'definition TEXT,'
              'added DATETIME DEFAULT CURRENT_TIMESTAMP)')

    return flask.g.dbconn

def get_size():
    c = get_conn().cursor()
    c.execute('SELECT count(*) FROM words')
    return c.fetchone()[0]

def get_definition(word):
    c = get_conn().cursor()
    c.execute("SELECT definition, added FROM words WHERE word=?", (word,))
    return c.fetchone()

def insert_definition(word, definition):
    con = get_conn()
    c = con.cursor()
    c.execute("INSERT INTO words (word, definition) VALUES (?, ?)", (word, definition))
    con.commit()

@app.route("/")
@app.route("/add")
def add_word():

    msg_kind = 'info'
    message = ''

    # Check for form parameters
    word = request.values.get('word')
    definition = request.values.get('definition')

    # Is the word in the dictionary?
    if word:
        dict_def = get_definition(word)
        if dict_def is None:
            # Add it to the dictionary
            insert_definition(word, definition)
            message = 'Added <em>%s</em> : %s to dictionary' % (word, definition)
        else:
            definition, added = dict_def
            msg_kind = 'error'
            message = 'Word already exists: %s &mdash; %s [<a href="/delete/%s">Delete it</a>]' % \
                                (word, dict_def, word)

    return render_template('add.html', word_count=get_size(),
                                       msg_kind=msg_kind,
                                       message=message)

def view_template(template, conditions):
    c = get_conn().cursor()
    c.execute('SELECT word, definition FROM words ORDER BY %s' % conditions)
    words = c.fetchall()
    return render_template(template, word_count=get_size(), words=words)

@app.route("/view")
def view():
    return view_template('view.html', 'added DESC LIMIT 200')

@app.route("/view/all")
def view_all():
    return view_template('view.html', 'added DESC')

@app.route("/rand")
def random():
    return view_template('rand.html', 'RANDOM() LIMIT 1')

@app.route("/delete/<word>")
def delete_word(word):
    msg_kind = 'info'
    message = 'Deleted word <em>%s</em>' % word

    con = get_conn()
    con.cursor().execute('DELETE FROM words WHERE word=?', (word,))
    con.commit()

    return render_template('add.html', word_count=get_size(),
                                       msg_kind=msg_kind,
                                       message=message)


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(port = 5001)
