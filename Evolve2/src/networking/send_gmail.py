import smtplib
from email.MIMEText import MIMEText

GMAIL_LOGIN = 'rblack@austincc.edu'
GMAIL_PASSWORD = 'xxxxxxxxx'

def send_email(subject, message, from_addr=GMAIL_LOGIN, to_addr=GMAIL_LOGIN):
    msg = MIMEText(message)
    msg['Subject'] = 'Test message'
    msg['From'] = from_addr
    msg['To'] = to_addr

    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(GMAIL_LOGIN,GMAIL_PASSWORD)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.close()

if __name__ == '__main__':
    send_email('testing email script', 'This is a test message')