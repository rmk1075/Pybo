from flask import Blueprint, url_for, render_template, flash, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm
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