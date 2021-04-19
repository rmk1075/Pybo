from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from sqlalchemy import func
from werkzeug.utils import redirect

from .auth_views import login_required
from .. import db

from pybo.forms import QuestionForm, AnswerForm
from pybo.models import Question, Answer, User, question_voter, answer_voter, Comment

# 블루프린트 객체 이름 question으로 생성
# url_prefix를 '/question'으로 설정
bp = Blueprint('question', __name__, url_prefix='/question')


# question list 조회 함수
@bp.route('/list/')
def _list():
    # 페이징 기능 추가
    # GET 방식으로 페이지 값을 가져올때 사용한다.
    # 페이지 값의 type은 int이다.
    # default는 1, 첫번째 페이지이다.
    # page, kw(keyword), kw_con(keyword condition - all, title, author, contents) 검색을 위해서 사용
    # so는 게시물 정렬에 사용, default는 최신순
    page = request.args.get('page', type=int, default=1)
    kw_con = request.args.get('kw_con', type=str, default='all')
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # 게시물 정렬
    if so == 'recommend':
        # 추천순
        # 질문별 추천수 조회하는 서브쿼리
        # func.count('*'): 질문별 추천수
        sub_query = db.session.query(question_voter.c.question_id, func.count('*').label('num_voter')) \
            .group_by(question_voter.c.question_id).subquery()

        # Question 객체와 sub_query를 아우터조인
        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())
    elif so == 'popular':
        # 답변
        sub_query = db.session.query(Answer.question_id, func.count('*').label('num_answer')) \
            .group_by(Answer.question_id).subquery()

        question_list = Question.query \
            .outerjoin(sub_query, Question.id == sub_query.c.question_id) \
            .order_by(sub_query.c.num_answer.desc(), Question.create_date.desc())
    else:
        # recent
        question_list = Question.query.order_by(Question.create_date.desc())

    # kw 검색 사용시
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        if kw_con == 'all':
            question_list = question_list \
                .join(User) \
                .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
                .filter(Question.subject.ilike(search) |  # 질문제목
                        Question.content.ilike(search) |  # 질문내용
                        User.username.ilike(search) |  # 질문작성자
                        sub_query.c.content.ilike(search) |  # 답변내용
                        sub_query.c.username.ilike(search)  # 답변작성자
                        ) \
                .distinct()
        elif kw_con == 'title':
            question_list = question_list \
                .join(User) \
                .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
                .filter(Question.subject.ilike(search)) \
                .distinct()
        elif kw_con == 'author':
            question_list = question_list \
                .join(User) \
                .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
                .filter(User.username.ilike(search)) \
                .distinct()
        elif kw_con == 'contents':
            question_list = question_list \
                .join(User) \
                .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
                .filter(Question.content.ilike(search)) \
                .distinct()

    # paginate 함수로 페이징을 적용한다.
    # 첫번쨰 인자 page는 가져올 페이지의 번호이다,
    # per_page는 페이지마다 보여줄 데이터의 건수이다.
    # 페이징
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw_con=kw_con, kw=kw, so=so)


# question detail 조회 함수
# answer paging 기능 추가
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)

    # answer paging
    page = request.args.get('page', type=int, default=1)
    so = request.args.get('so', type=str, default='recent')
    if so == 'recommend':
        sub_query = db.session.query(answer_voter.c.answer_id, func.count('*').label('answer_voter')) \
            .group_by(answer_voter.c.answer_id).subquery()

        answer_list = Answer.query \
            .outerjoin(sub_query, Answer.id == sub_query.c.answer_id) \
            .order_by(sub_query.c.answer_voter.desc(), Answer.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(Comment.answer_id, func.count('*').label('num_comment')) \
            .group_by(Comment.answer_id).subquery()

        answer_list = Answer.query \
            .outerjoin(sub_query, Answer.id == sub_query.c.answer_id) \
            .order_by(sub_query.c.answer_answer.desc(), Answer.create_date.desc())
    else:
        answer_list = Answer.query.filter(Answer.question_id == question_id).order_by(Answer.create_date.desc())

    answer_list = answer_list.paginate(page, per_page=5)
    return render_template('question/question_detail.html', question=question, answer_list=answer_list, form=form, so=so)


# Quesiont 등록 함수
@bp.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    form = QuestionForm()

    # request.method: request 전송 방식
    # form.validate_on_submit(): 전송된 폼 데이터의 정합성 체크
    # POST 요청 시에 폼 데이터에 문제가 없으면 db 저장 후 main.index 화면으로 redirect한다.
    if request.method == 'POST' and form.validate_on_submit():
        # form data 접근 - form.subject.data
        # user 필드 반영 - g.user
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(), user=g.user)

        # question 객체 db 저장
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('question/question_form.html', form=form)


# Question 수정 함수
# login_required decorator 사용
@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)

    # 사용자가 글쓴이가 아닌 경우 flash 출력
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))

    # POST 방식인 경우 새롭게 입력된 값들로 Question을 수정해준다.
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            # form에 입력되어있는 데이터를 question 객체에 적용해 준다.
            form.populate_obj(question)

            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else:
        # QuestionForm(obj=question): 조회한 데이터를 obj 인자로 전달하여 폼을 생성한다.
        form = QuestionForm(obj=question)
    return render_template('question/question_form.html', form=form)


# Question 삭제 함수
# login_required decorator 사용
@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)

    # 사용자, 글쓴이 일치 확인
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))
