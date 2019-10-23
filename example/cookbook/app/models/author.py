from app import db


class Author(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    name = db.Column(db.String(64))
    posts = db.relationship('Post', backref='author')

