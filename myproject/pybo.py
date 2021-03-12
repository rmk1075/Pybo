from flask import Flask

'''
- flask 어플리케이션을 생성
- __name__: 모듈명을 나타내는 변수. 이 파일의 경우 pybo라는 값이 담겨져있다. 
'''
app = Flask(__name__)

'''
@app.route: 특정 주소에 접근하면 다음 코드를 실행하도록 하는 플라스크의 데코레이터이다. 
'''
@app.route('/')
def hello_pybo():
    return 'Hello, Pybo!'
