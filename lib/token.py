from itsdangerous import URLSafeTimedSerializer
import os

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(os.environ['SECURITY_PASSWORD'])
    return serializer.dumps(email, salt=os.environ['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(os.environ['SECURITY_PASSWORD'])
    try:
        email = serializer.loads(
            token,
            salt=os.environ['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email