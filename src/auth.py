#src/shared/Authentication
import jwt
import os
import datetime
from flask import json, Response, request, g
from functools import wraps
from .models.usermodel import UserModel as um


class Auth():
    """
    Generates JWT token with user_id, current time and expiry time for use later
    """
    @staticmethod
    def generate_token(user_id):
        try:
            payload = {
                #time using timezone attribute from UserModel
                'exp': datetime.datetime.now(um.tz) + datetime.timedelta(days=1),
                'iat': datetime.datetime.now(um.tz),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                os.getenv('JWT_SECRET_KEY'),
                'HS256'
            ).decode("utf-8")
        except Exception as e:
            return Response(
                mimetype="application/json",
                response=json.dumps({'error': 'error generating jwt token'}),
                status=400
            )

    @staticmethod
    def decode_token(token):
        re = {'data': {}, 'error': {}}
        try:
            payload = jwt.decode(token, os.getenv('JWT_SECRET_KEY'))
            re['data'] = {'user_id': payload['sub']}
            return re
        except jwt.ExpiredSignatureError as e1:
            re['error'] = {'message': 'token expired, please login again'}
            return re
        except jwt.InvalidTokenError:
            re['error'] = {'message': 'Invalid token, please try again'}
            return re

    # decorator
    @staticmethod
    def auth_required(func):
        # Wraps keeps docstrings/name of the function we use @auth_required decorator over it
        @wraps(func)
        def decorated_auth(*args, **kwargs):
            if 'api-token' not in request.headers:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': 'Please login to authenticate'}),
                    status=400
                )
            token = request.headers.get('api-token')
            data = Auth.decode_token(token)

            if data['error']:
                return Response(
                    mimetype="application/json",
                    response=json.dumps(data['error']),
                    status=400
                )

            user_id = data['data']['user_id']
            check_user = um.get_one_user(user_id)

            if not check_user:
                return Response(
                    mimetype="application/json",
                    response=json.dumps({'error': 'User does not exist'}),
                    status=400
                )
            g.user = {'id': user_id}
            return func(*args, **kwargs)

        return decorated_auth
