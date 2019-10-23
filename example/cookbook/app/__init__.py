from flask import Flask, Blueprint
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    # api_bp = Blueprint('api', __name__)
    # api = Api(api_bp)

    app.config.from_object(Config())
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .controllers.author import author as author_bp
    app.register_blueprint(author_bp, url_prefix='/author')

    from .controllers.post import post as post_bp
    app.register_blueprint(post_bp, url_prefix='/post')

    return app
