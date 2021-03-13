from flask import Blueprint, render_template, url_for
from werkzeug.utils import redirect

from pybo.models import Question

# 블루프린트 객체 생성 (이름, 모듈명, url prefix)
# 객체의 이름 'main'은 함수명으로 url을 찾는 url_for에서 사용한다.
bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'


@bp.route('/')
def index():
    # Question 테이블 데이터를 create date 내림차순으로 조회 (.asc() 또는 생략시 오름차순으로 정렬한다.)
    # question_list = Question.query.order_by(Question.create_date.desc())

    # template 화면을 전달한 데이터로 그려준다.
    # return render_template('question/question_list.html', question_list=question_list)

    # question._list로 url redirect
    return redirect(url_for('question._list'))


# question_id에 int 값이 매핑된다.
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    # 접근한 url의 question_id를 통해서 질문 데이터를 조회한다.
    # 해당 번호에 일치하는 질문이 없는 경우 404 페이지를 출력한다.
    question = Question.query.get_or_404(question_id)

    # 조회한 질문 객체를 반환해서 질문 상세 템플릿으로 출력한다.
    return render_template('question/question_detail.html', question=question)
