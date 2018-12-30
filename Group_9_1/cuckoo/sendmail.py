from .models import EmailVerifyRecord
from random import Random
from django.core.mail import send_mail
from Group_9.settings import EMAIL_FROM



# 生成随机字符串
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGg1234567890'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 保存到数据库
def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(6)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = "Welcome to use Cuckoo!"
    email_body = code
    print('has')
    send_mail(email_title, email_body, EMAIL_FROM, [email])
    return code