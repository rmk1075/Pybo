from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


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
