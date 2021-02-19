#/src/views/blogpostview
from flask import request, json, Response, Blueprint, jsonify, g
from marshmallow import ValidationError
from ..models.blogpostmodel import BlogpostModel, BlogpostSchema
from ..models.usermodel import UserModel
from ..auth import Auth

# initialize blueprint object
posts_api = Blueprint('posts', __name__)
posts_schema = BlogpostSchema

@posts_api.route('/', methods=['POST')
@Auth.auth_required
def create():
    req = request.get_json()
    # try to deserialize data for use
    try:
        data = posts_schema.load(req)
    except ValidationError as err:
        return custom_response(err, 400)

    # set owner id to same id as the users id in the request context
    req['owner_id'] = g.user.get('id')

    # Create table object to be saved directly to db
    post = BlogpostModel(data)
    post.save()

    # Serializes data to be returned as json
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
    data = posts_schema.dump(posts)
    return custom_response(data, 200)

@post_api.route('/<int:owner_id>', methods=['GET'])
def get_all_owners(owner_id):
    user = UserModel.get_one_user(owner_id)
    if not users:
        return custom_response({'error': 'user does not exist!'}, 400)

    posts = BlogpostModel.get_user_blogposts(owner_id)
    if not posts:
        return custom_response({'error': 'User does not have any posts'})

    data = posts_schema.dump(posts, many=True)
    return custom_response(data, 200)

@post_api.route('/<int:blogpost_id>', methods=['PUT'])
@Auth.auth_required
def update(blogpost_id):
    req = request.get_json()
    posts = BlogpostModel.get_one_blogpost(blogpost_id)
    if not posts:
        return custom_response({'error':'post not found'}, 404)
    data = posts_schema.dump(posts)

    # user should have same id as blog post owner id after logging in
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    # try to deserialize data to blogpost object to update
    try:
        data = blogpost_schema.load(req_data, partial=True)
    except ValidationError as err:
        return custom_response(error, 200)

    posts.update(data)
    data = blogpost_schema.dump(posts) # serialize again
    return custom_response({'message': 'post updated!'}, 200)

@blogpost_api.route('/<int:blogpost_id>', methods=['DELETE'])
@Auth.auth_required
def delete(blogpost_id):
    posts = BlogpostModel.get_one_blogpost(blogpost_id)
    if not posts:
        return custom_response({'error':'post not found'}, 404)

    data = posts_schema.dump(posts)
    # user should have same id as blog post owner id after logging in
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    posts.delete()
    return custom_response({'message': 'post deleted!'}, 200)

def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
