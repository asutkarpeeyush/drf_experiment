from rest_framework.authentication import TokenAuthentication
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"