import requests
import os
from dotenv import load_dotenv
from django.http import HttpResponse
from functools import wraps
import json
from rest_framework.permissions import BasePermission
load_dotenv()



Domain = os.environ['auth_url']

class CustomIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        authorization_header = request.META.get('HTTP_AUTHORIZATION', '')
        if authorization_header.startswith('Bearer '):
            token = authorization_header.split(' ')[1]
        else:
            return False
        verify_token_url = f'{Domain}/Auth/verifytoken/'
        payload = {'token': token}
        try:
            response = requests.post(verify_token_url, data=payload)
        except Exception as e:
            return False
        else:            
            if response.status_code == 200:
                request.user = json.loads(response.text)
                return True
            else:
                return False