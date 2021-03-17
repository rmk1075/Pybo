from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

# auth blueprint 객체 생성
bp = Blueprint('auth', __name__, url_prefix='/auth')


# GET: 회원가입 화면
# POST: 회원 등록
@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    # POST 방식
    if request.method == 'POST' and form.validate_on_submit():
        # username 확인해서 이미 존재하는 회원인지 확인
        user = User.query.filter_by(username=form.username.data).first()
        # 이미 존재하는 회원이 없는 경우 등록을 진행
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            # 프로그램 논리 오류 발생
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)


# user login시 실행되는 함수
@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = '존재하지 않는 사용자입니다.'
        elif not check_password_hash(user.password, form.password.data):
            error = '비밀번호가 올바르지 않습니다.'

        if error is None:
            # session에 사용자 정보 저장
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))

        flash(error)

    return render_template('auth/login.html', form=form)


# 다른 route들보다 먼저 실행된다.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    # g: flask에서 제공해주는 객체로 request와 같이 요청 -> 응답시에 유효하다.
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

