import sys
import sqlite3
import argparse

def main(args):
    inp = sqlite3.connect(args.input)
    out = sqlite3.connect(args.output)

    out.cursor().execute('DELETE FROM words')
    query = 'SELECT word, definition, added FROM words ORDER BY added'
    transaction = 'INSERT INTO words (word, definition, added) VALUES (?, ?, ?)'

    for row in inp.execute(query):
        out.cursor().execute(transaction, row)

    out.commit()
    out.close()
    inp.close()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Import vocab words')
    parser.add_argument('input', help='sqlite3 input db file')
    parser.add_argument('output', help='sqlite3 output db file')

    return parser.parse_args()

if __name__ == '__main__':
    main(parse_arguments())

