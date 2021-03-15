import os

BASE_DIR = os.path.dirname(__file__)

# 데이터 베이스 접속 주소 -> pybo.db 데이터 베이스 파일로 저장
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))

# SQLAlchemy 이벤트 처리 옵션
SQLALCHEMY_TRACK_MODIFICATIONS = False

# SECRET_KEY 설정
SECRET_KEY = "dev"
