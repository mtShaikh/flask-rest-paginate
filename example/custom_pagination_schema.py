from faker import Faker
from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_rest_paginate import Pagination

"""
Initialize the app
"""
app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///paginate-test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Possible configurations for Paginate
# app.config['PAGINATE_PAGE_SIZE'] = 20
# app.config['PAGINATE_PAGE_PARAM'] = "pagenumber"
# app.config['PAGINATE_SIZE_PARAM'] = "pagesize"
# app.config['PAGINATE_RESOURCE_LINKS_ENABLED'] = False
pagination = Pagination(app, db)


"""
Models
"""
class AuthorModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    posts = db.relationship('PostModel', backref='author', lazy=True)


class PostModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.String(255))
    author_id = db.Column(db.Integer, db.ForeignKey('author_model.id'), nullable=False)


"""
Resource fields for marshalling
"""
post_fields = {
    'title': fields.String,
    'content': fields.String,
    'author_id': fields.Integer
}

author_fields = {
    'name': fields.String,
    'posts': fields.List(fields.Nested(post_fields))
}


"""
Controllers
"""
class Post(Resource):
    @marshal_with(post_fields)
    def get(self, post_id):
        return PostModel.query.filter_by(id=post_id).first()


class PostList(Resource):
    @marshal_with(post_fields)
    def get(self):
        return PostModel.query.all()


class Author(Resource):
    # No need to decorate with `marshal_with` as the function will marshal it automatically
    # @marshal_with(author_fields)
    def get(self, author_id):
        # Can pass the query object with filters
        return pagination.paginate(AuthorModel.query.filter_by(id=author_id), author_fields)


class AuthorList(Resource):
    def get(self):
        # Can also pass the model directly, in which case, no filters can be attached
        return pagination.paginate(AuthorModel, author_fields,  pagination_schema_hook=lambda current_page, page_obj: {
            "next": page_obj.has_next,
            "prev": page_obj.has_prev,
            "current": current_page,
            "pages": page_obj.pages,
            "per_page": page_obj.per_page,
            "total": page_obj.total,
        })


"""
Register the resources
"""
api.add_resource(Post, '/posts/<post_id>')
api.add_resource(PostList, '/posts')
api.add_resource(Author, '/authors/<author_id>')
api.add_resource(AuthorList, '/authors')


"""
Seed database
"""
def seed():
    fake = Faker()
    for i in range(100):
        db.session.add(AuthorModel(name=fake.name()))
        for j in range(10):
            db.session.add(PostModel(title=fake.sentence(), content=fake.text(), author_id=i))

    db.session.commit()


"""
Recreate the DB
"""
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()



"""
Run the app
"""
if __name__ == '__main__':
    recreate_db()
    seed()
    app.run(debug=True)


