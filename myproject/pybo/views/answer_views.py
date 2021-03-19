from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import AnswerForm
from pybo.models import Question, Answer
from pybo.views.auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')


# answer 조회
# POST 방식으로 접근
# login 상태 확인을 위한 decorator 사용
@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):
    # question 객체 조회
    question = Question.query.get_or_404(question_id)

    # answer form
    form = AnswerForm()
    if form.validate_on_submit():
        # request: 브라우저에서 요청한 데이터를 확인할 수 있는 객체
        # form 형식으로 전달된 데이터 중 항목명이 'content' 인 데이터
        content = request.form['content']

        # 질문에 달릴 답변 객체 생성
        # user 필드 반영 - g.user
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.commit()

        return redirect(url_for('question.detail', question_id=question_id))

    return render_template('question/question_detail.html', question=question, form=form)