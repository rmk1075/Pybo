from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

import config

# SQLite 데이터 베이스 제약 조건 이름 설정
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# db 설정 객체 생성
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()


# application factory: app 객체를 생성하는 함수
# - create_app()은 플라스크 내부에서 정의된 함수명으로 다른 함수명을 사용하는 경우 오류 발생한다.
def create_app():
    # - flask 어플리케이션을 생성
    # - __name__: 모듈명을 나타내는 변수. 이 파일의 경우 pybo라는 값이 담겨져있다.
    app = Flask(__name__)

    # config 설정 적용
    app.config.from_object(config)

    # ORM 설정
    db.init_app(app)
    # migrate.init_app(app, db)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    from . import models

    # @app.route: 라우트 함수
    # @app.route('/')
    # def hello_pybo():
    #     return 'Hello, Pybo!'

    # 블루프린트 적용 (main_veiws, question_views, answer_views, auth_views)
    from .views import main_views, question_views, answer_views, auth_views, comment_views, vote_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(comment_views.bp)
    app.register_blueprint(vote_views.bp)

    # 필터 적용
    from .filter import format_datetime

    # 'datetime' 필터 등록
    app.jinja_env.filters['datetime'] = format_datetime

    return app
