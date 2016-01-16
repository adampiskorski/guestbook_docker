from flask import Flask, render_template, g, request

# flask-sqlalchemy also installs and imports sqlalchemy as a requirement
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Chooses the file location of the sqlite DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
db = SQLAlchemy(app)


# The DB Schema, or medel (SQLAlchemy will create the schema based on this)
class GuestBook(db.Model):
    # primary_key=True means that SQLAlchemy will automatically generate
    # IDs for this column and so you never have to touch it.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    message = db.Column(db.String(500))

    # Creates DB the DB objects that can be saved.
    def __init__(self, name, message):
        self.name = name
        self.message = message

# Explicitly say it can handle both GET and POST now (necesary for POST to work)
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    # If posted to and basic validation on input
    if (request.method == 'POST' and
        request.form['name'] and
        request.form['message']):

        # Save to DB
        message = GuestBook(name=request.form['name'],
                            message=request.form['message'])
        db.session.add(message)
        db.session.commit()

    # Get all Guest Book Entries and Pass to template
    messages = GuestBook.query.all()

    return render_template('home.html', messages=messages)


if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run(host='0.0.0.0')