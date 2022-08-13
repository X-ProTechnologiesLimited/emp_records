# project/email.py

from flask_mail import Message

from . import mail

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender='xprotech.contact@gmail.com'
    )
    mail.send(msg)