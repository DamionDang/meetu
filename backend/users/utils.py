import jwt
from datetime import datetime, timedelta
from django.conf import settings
from users.models import CustomUser

def generate_jwt_token(user):
    payload = {
        'id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')