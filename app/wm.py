from datetime import datetime

from flask import Flask, g, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import func

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

class Word(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, nullable=False)
    definition = db.Column(db.String, nullable=False)
    added = db.Column(db.DateTime, default=datetime.utcnow)

    dictionary_id = db.Column(db.Integer, db.ForeignKey('dictionary.id'))

class Dictionary(db.Model):
    __tablename__ = 'dictionary'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    words = db.relationship('Word', backref='dictionary')

def requires_dictionary(func):
    ''' Decorator for ensuring dictionary is loaded. '''
    def ensure_exists(name, **moreargs):
        did = db.session.query(Dictionary).filter_by(name=name).first()
        if did is None:
            return redirect(url_for('list'))
        return func(did, **moreargs)
    ensure_exists.__name__ = func.__name__
    return ensure_exists


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'max-age=0'
    return response

def word_selector(did, **selector):
    return db.session.query(Word).filter_by(dictionary_id=did, **selector)

def word_count(did):
    return word_selector(did).count()

def get_definition(did, word):
    return word_selector(did, word=word).first()

def insert_definition(did, word, definition):
    db.session.add(Word(dictionary_id=did, word=word, definition=definition))
    db.session.commit()

@app.after_request
def close_session(response):
    db.session.close()
    return response

@app.route('/')
def list():
    dicts = db.session.query(Dictionary).all()
    return render_template('list.html', dictionaries=dicts)

@app.route('/<name>/add')
@requires_dictionary
def add_word(d):
    msg_kind = 'info'
    message = ''

    # Check for form parameters
    word = request.values.get('word', '').strip()
    definition = request.values.get('definition', '').strip()

    if word:
        # Is the word already in the dictionary?
        previous = get_definition(d.id, word)
        if previous is not None:
            del_url = url_for('delete_word', word=word, name=d.name)
            msg_kind = 'error'
            message = f'Word already exists: {previous.word} &mdash; ' \
                      f'{previous.definition}. ' \
                      f'[<a href="{del_url}">Delete it</a>]'
        else:
            insert_definition(d.id, word, definition)
            message = f'Added <em>{word}</em> : {definition} to dictionary'

    params = dict(name=d.name, word_count=word_count(d.id), msg_kind=msg_kind,
                  message=message)
    return render_template('add.html', **params)

def template_selector(template, d, words):
    params = dict(word_count=word_count(d.id), words=words, name=d.name)
    return render_template(template, **params)

@app.route("/<name>/view")
@requires_dictionary
def view(d):
    words = word_selector(d.id).order_by(Word.added.desc()).limit(200).all()
    return template_selector('view.html', d, words)

@app.route("/<name>/view/all")
@requires_dictionary
def view_all(d):
    words = db.session.query(Word).order_by(Word.added.desc()).all()
    return template_selector('view.html', d, words)

@app.route("/<name>/rand")
@requires_dictionary
def random(d):
    words = word_selector(d.id).order_by(func.random()).limit(1).all()
    return template_selector('rand.html', d, words)

@app.route("/<name>/delete/<word>")
@requires_dictionary
def delete_word(d, word):
    msg_kind = 'info'
    message = f'Deleted word <em>{word}</em>'

    found = word_selector(d.id, word=word).one()
    if found is None:
        msg_kind = 'error'
        message = f'Could not find word {word} to delete'
    else:
        db.session.delete(found)
        db.session.commit()

    params = dict(name=d.name, msg_kind=msg_kind, message=message)
    return render_template('add.html', **params)

