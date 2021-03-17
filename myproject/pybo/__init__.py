from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

# db 설정 객체 생성
db = SQLAlchemy()
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
    migrate.init_app(app, db)

    from . import models

    # @app.route: 라우트 함수
    # @app.route('/')
    # def hello_pybo():
    #     return 'Hello, Pybo!'

    # 블루프린트 적용 (main_veiws, question_views, answer_views)
    from .views import main_views, question_views, answer_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)

    # 필터 적용
    from .filter import format_datetime

    # 'datetime' 필터 등록
    app.jinja_env.filters['datetime'] = format_datetime

    return app
