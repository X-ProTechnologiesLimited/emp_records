# project/email.py

from flask_mail import Message

from . import mail

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender='Employee Manager'
    )
    mail.send(msg)