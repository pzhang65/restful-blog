#/src/views/userview
from flask import request, json, Response, Blueprint, jsonify, g
from marshmallow import ValidationError
from ..models.usermodel import UserModel, UserSchema
from ..auth import Auth

#initialize blueprint object to construct our flask app
user_api = Blueprint('users', __name__)
user_schema = UserSchema()

#params become common view arguements across all views in blueprint
@user_api.route('/', methods=['POST'])
def create():
    req = request.get_json()
    # try to deserialize data, if error print
    try:
        data = user_schema.load(req)
    except ValidationError as err:
        print("Create() try statement failed")
        return custom_response(err, 400)

    # check if user already exist in the db
    user_in_db = UserModel.get_user_by_email(data.get('email'))
    if user_in_db:
        message = {'error': 'User already exists, enter another email'}
        return custom_response(message, 400)

    user = UserModel(data)
    user.save()

    ser_data = user_schema.dump(user)

    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'jwt_token': token}, 201)


@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
    users = UserModel.get_all_users()
    ser_users = user_schema.dump(users, many=True).data
    return custom_response(ser_users, 200)

@user_api.route('/login', methods=['POST'])
def login():
    req = request.get_json()
    # try to deserialize data, if error print
    try:
        data = user_schema.load(req, partial=True) # Partial flag because name not needed
    except ValidationError as err:
        return custom_response(err, 400)

    if not data.get('email') or not data.get('password'):
        return custom_response({'error': 'you need email and password to sign in'}, 400)

    #Email is an alternate key that we use to query the DB from user inputs
    user = UserModel.get_user_by_email(data.get('email'))
    print(user)

    if not user:
        return custom_response({'error': 'email does not exist!'}, 400)

    if not user.check_hash(data.get('password')):
        return custom_response({'error': 'invalid password!'}, 400)

    ser_data = user_schema.dump(user)
    print(ser_data)
    print("serialize succesful")
    token = Auth.generate_token(ser_data.get('id'))
    print(token)
    return custom_response({'jwt_token': token}, 200)


@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
    user = UserModel.get_one_user(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, 404)

    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)

@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
    user = UserModel.get_one_user(g.user.get('id'))
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)

@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
    req = request.get_json()
    data, error = user_schema.load(req, partial=True)
    if error:
        return custom_response(error, 400)

@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
    user = UserModel.get_one_user(g.user.get('id'))
    user.delete()
    return custom_response({'message': 'deleted'}, 204)

def custom_response(res, status_code):

    # Flask default response object configured to return a JSON object
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
