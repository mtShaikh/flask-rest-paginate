from app import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('author_id'), nullable=False)

    def __repr__(self):
        return '<Post %r>' % self.title
