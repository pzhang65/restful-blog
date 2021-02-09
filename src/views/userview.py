#/src/views/UserView

from flask import request, json, Response, Blueprint
from ..models.usermodel import UserModel, UserSchema

#initialize blueprint object to construct our flask app
user_api = Blueprint('users', __name__)
user_schema = UserSchema()

#params become common view arguements across all views in blueprint
@user_api.route('/', methods=['POST'])
def create():
  """
  Create User Function
  """
  req = request.get_json()
  #Similar to requests.load() where it loads the requests into python data objects
  data, error = user_schema.load(req)

  if error:
    return custom_response(error, 400)

  # check if user already exist in the db
  user_in_db = UserModel.get_user_by_email(data.get('email'))
  if user_in_db:
    message = {'error': 'User already exists, enter another email'}
    return custom_response(message, 400)

  user = UserModel(data)
  user.save()

  ser_data = user_schema.dump(user).data

  token = Auth.generate_token(ser_data.get('id'))

  return custom_response({'success': True}, 'user':f'User created: {user}', 200)


def custom_response(res, status_code):
  """
  Custom Response Function
  """
  return Response(
    mimetype="application/json",
    response=json.dumps(res),
    status=status_code
  )
