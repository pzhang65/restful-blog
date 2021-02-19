#/src/views/blogpostview
from flask import request, json, Response, Blueprint, jsonify, g
from marshmallow import ValidationError
from ..models.blogpostmodel import BlogpostModel, BlogpostSchema
from ..models.usermodel import UserModel
from ..auth import Auth

posts_api = Blueprint('posts', __name__)
posts_schema = BlogpostSchema

@posts_api.route('/', methods=['POST')
@Auth.auth_required
def create():
    req = request.get_json()

    try:
        data = posts_schema.load(req)
    except ValidationError as err:
        return custom_response(err, 400)

    req['owner_id'] = g.user.get('id')

    post = BlogpostModel(data)
    post.save()

    data = posts_schema.dump(post)
    return custom_response(data,201)

@posts_api.route('/', methods = ['GET'])
def get_all():
    posts = BlogpostModel.get_all_blogposts()
    data = posts_schema.dump(posts, many=True)
    return custom_response(data, 200)

@post_api.route('/<int:blogpost_id>', methods=['GET'])
def get_one(blogpost_id):
    posts = BlogpostModel.get_one_bologpost(blogpost_id)
    if not posts:
        return custom_response({'error':'post not found'}, 404)
    data = posts_schema.dump(post)
    return custom_response(data, 200)

@post_api.route('/<int:owner_id>', methods=['GET'])
def get_all_owners(owner_id):
    user = UserModel.get_one_user(owner_id)
    if not users:
        return custom_response({'error': 'user does not exist!'}, 400)

    posts = BlogpostModel.get_user_blogposts(owner_id)
    if not posts:
        return custom_response({'error': 'User does not have any posts'})

    data = posts_schema.dump(post, many=True)
    return custom_response(data, 200)



def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
