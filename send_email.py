from helpers.email_helper import get_default_email_helper
from datetime import datetime


def send_mail(self):
    e_helper = get_default_email_helper()
    session = e_helper.email_session
    sender = e_helper.sender
    receivers = e_helper.receivers
    msg = e_helper.email_msg
    # headers
    msg['From'] = '457638186@qq.com'
    msg['To'] = 'john526@foxmai.com'
    e_helper.set_header(sub="subject", title=f"Python email test on {str(datetime.now())[0:16]}", code='utf-8')
    content = self.output
    # content = json.dumps(self.output, ensure_ascii=False)  # json dumps把python对象转换成json字符串，json_load反之
    e_helper.att(content, 'html', 'utf-8')
    try:
        session.sendmail(sender, receivers, msg.as_string())
        print('email sent successfully!')
    except session.SMTPException:
        import traceback
        traceback.print_exc()
        print("failed to send email")

