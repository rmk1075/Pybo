from flask import Blueprint

# 블루프린트 객체 생성 (이름, 모듈명, url prefix)
# 객체의 이름 'main'은 함수명으로 url을 찾는 url_for에서 사용한다.
bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    return 'Pybo index'
