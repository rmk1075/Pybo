from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo, Email, Length


# Flask-WTF 모듈의 FlaskForm 클래스를 상속받아 subject, content 속성을 포함한다.
class QuestionForm(FlaskForm):
    # StringField('form label', validators)
    # form label: 템플릿에서 이 값으로 라벨을 출력할 수 있다.
    # validators: 필드값을 검증할 때 사용한다. - DataRequired(), Email(), Length() ...

    # 글자 수에 제한이 있는 입력은 StringField 객체를 사용한다.
    subject = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])

    # 글자 수에 제한이 없는 입력은 TextAreaField 객체를 사용한다.
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


# 답변 등록 form
class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


# 회원 등록 form
class UserCreateForm(FlaskForm):
    # Length: 입력 string 길이 제한
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    # EqualTo -> 비밀번호와 비밀번호확인이 일치하는지 검증
    # PasswordField -> <input type="password">
    password1 = PasswordField('비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    # EmailField -> <input type="email">
    email = EmailField('이메일', validators=[DataRequired(), Email()])
