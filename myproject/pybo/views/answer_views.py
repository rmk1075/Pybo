from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
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


# answer 수정 함수
# login_required decorator
@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)

    # 사용자 글쓴이 일치 확인
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))

    # POST 방식
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            # form에 입력된 데이터를 answer에 적용한다.
            form.populate_obj(answer)
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=answer.question.id))
    else:
        # AnswerForm(obj=answer): 조회한 데이터를 obj 인자로 전달하여 폼을 생성한다.
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', answer=answer, form=form)


# answer 삭제 함수
@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id

    # 사용자 글쓴이 확인
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))
