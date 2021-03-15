from datetime import datetime

from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from .. import db

from pybo.forms import QuestionForm, AnswerForm
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
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)


# Quesiont 등록 함수
@bp.route('/create/', methods=['GET', 'POST'])
def create():
    form = QuestionForm()

    # request.method: request 전송 방식
    # form.validate_on_submit(): 전송된 폼 데이터의 정합성 체크
    # POST 요청 시에 폼 데이터에 문제가 없으면 db 저장 후 main.index 화면으로 redirect한다.
    if request.method == 'POST' and form.validate_on_submit():
        # form data 접근 - form.subject.data
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())

        # question 객체 db 저장
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)
