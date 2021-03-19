from pybo import db


# 질문 객체 클래스
# db.Model: 모든 모델의 기본 클래스
# 질문 객체 컬럼: 고유 번호(id), 제목(subject), 내용(content), 작성일시(create_date)
# db.Column(db.Integer, primary_key=True) -> (데이터 타입, primary key 여부, )
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

    # db.ForeignKey('user.id', ondelete='CASCADE')
    # User 모델의 id 값과 연결
    # ondelete='CASCADE' user 데이터 삭제 시에 Question 모델 데이터도 함께 삭제되도록함
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))

    # 수정일자 컬럼
    modify_date = db.Column(db.DateTime(), nullable=True)


# 답변 객체 클래스
# 답변 객체 클래스: 고유 번호(id), 질문 번호 (question_id), 질문 (question), 내용(content), 작성일시(create_date)
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # 기존 모델과 연동된 속성인 question_id는 foreign key로 설정된다.
    # ondelete는 삭제시의 설정에 대한 옵션인데, 'CASCADE'로 설정하게 되면 question 데이터 삭제 시에 이와 연동된 answer 데이터도 삭제된다.
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))

    # answer 객체에서 question 객체를 상속
    # db.relationship('참조할 모델명', backref=역참조 설정
    # 역참조: 질문에서 답변을 참조하는 것 - 하나의 질문에 여러개의 답변이 달릴 수 있는데, 질문에서 이 답변들을 참조하는 것
    question = db.relationship('Question', backref=db.backref('answer_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

    # user 객체의 id와 연결
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))

    # 수정일자 컬럼
    modify_date = db.Column(db.DateTime(), nullable=True)


# 회원 정보 모델
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
