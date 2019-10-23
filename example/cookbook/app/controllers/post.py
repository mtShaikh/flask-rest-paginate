from flask import Blueprint

from app.models.post import Post

post = Blueprint('post', __name__)


@post.route('/')
def get_all():
    posts = Post.query.all()
