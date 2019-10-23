from flask import Blueprint

from app.models.author import Author

author = Blueprint('author', __name__)


@author.route('/')
def get_all():
    authors = Author.query.all()
