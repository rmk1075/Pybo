from flask import Flask


# application factory: app 객체를 생성하는 함수
# - create_app()은 플라스크 내부에서 정의된 함수명으로 다른 함수명을 사용하는 경우 오류 발생한다.
def create_app():
    # - flask 어플리케이션을 생성
    # - __name__: 모듈명을 나타내는 변수. 이 파일의 경우 pybo라는 값이 담겨져있다.
    app = Flask(__name__)

    # @app.route: 라우트 함수
    # @app.route('/')
    # def hello_pybo():
    #     return 'Hello, Pybo!'

    # 블루프린트 적용
    from .views import main_views
    app.register_blueprint(main_views.bp)

    return app


