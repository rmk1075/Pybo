# value: datetime 객체
# value 값을 fmt로 포맷을 맞춰 str으로 반환한다.
def format_datetime(value, fmt='%Y년 %m월 %d일 %H:%M'):
    return value.strftime(fmt)