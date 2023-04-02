import smtplib
from email.message import EmailMessage
from email.utils import formataddr
import random
import math

def generateCode():
    digits = [i for i in range(0, 10)]

    code = ""
    
    for i in range(6):
        index = math.floor(random.random() * 10)
        code += str(digits[index])
    
    return code


def sendMail(address):

    code = generateCode()

    # 이메일 주소와 암호 입력
    MY_ADDRESS = 'dign1120@naver.com'
    MY_PASSWORD = 'dpfthem40043029!'

    # 수신자 이메일 주소 입력
    TO_ADDRESS = address

    # 이메일 구성
    message = EmailMessage()

    message['From'] = formataddr(('PIM AGENT', MY_ADDRESS))
    message['To'] = TO_ADDRESS
    message['Subject'] = '[PIM AGENT] 비밀번호 재설정을 하기위한 메시지 입니다.'

    # 이메일 내용 입력
    body = '비밀번호를 재설정 하기 위해\n해당 6자리 코드({})를 입력해 주세요'.format(code)
    message.set_content(body)

    # SMTP 서버 설정 및 이메일 보내기
    with smtplib.SMTP('smtp.naver.com', 587) as smtp:
        smtp.starttls()
        smtp.login(MY_ADDRESS, MY_PASSWORD)
        smtp.send_message(message)

    return code
