from datetime import datetime

from flask import Blueprint, url_for, request
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')


# answer 조회
# POST 방식으로 접근
@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    # question 객체 조회
    question = Question.query.get_or_404(question_id)

    # request: 브라우저에서 요청한 데이터를 확인할 수 있는 객체
    # form 형식으로 전달된 데이터 중 항목명이 'content' 인 데이터
    content = request.form['content']

    # 질문에 달릴 답변 객체 생성
    answer = Answer(content=content, create_date=datetime.now())
    question.answer_set.append(answer)
    db.session.commit()

    #
    return redirect(url_for('question.detail', question_id=question_id))