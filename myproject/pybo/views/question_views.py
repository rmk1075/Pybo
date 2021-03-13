from flask import Blueprint, render_template

from pybo.models import Question

# 블루프린트 객체 이름 question으로 생성
# url_prefix를 '/question'으로 설정
bp = Blueprint('question', __name__, url_prefix='/question')


# question list 조회 함수
@bp.route('/list/')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=question_list)


# question detail 조회 함수
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question)