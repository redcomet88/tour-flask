from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from app.utils import make_response

db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)
    ma.init_app(app)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 全局错误处理
    # @app.errorhandler(Exception)
    # def handle_exception(e):
    #     return make_response(code=1, message=str(e)), 500

    return app