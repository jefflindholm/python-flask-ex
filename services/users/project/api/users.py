from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc

from project.api.models import User
from project import db

users_blueprint = Blueprint('users', __name__, template_folder='./templates')


# routes
@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """
    Get All User
    ---
    definitions:
        User:
            type: object
            properties:
                id:
                    type: string
                username:
                    type: string
                email:
                    type: string
                active:
                    type: boolean
        AllUsersResponse:
            type: object
            properties:
                status:
                    type: string
                data:
                    type: array
                    items:
                        $ref: '#/definitions/User'
    responses:
        200:
            description: success
            schema:
                $ref: '#/definitions/AllUsersResponse'
    """
    response_object = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }
    return jsonify(response_object), 200


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """
    Get User
    ---
    definitions:
        UserResponse:
            type: object
            properties:
                status:
                    type: string
                data:
                    $ref: '#/definitions/User'
    parameters:
        -   name: user_id
            in: path
            type: integer
            required: true
    responses:
        200:
            description: success if the user was found
            schema:
                $ref: '#/definitions/UserResponse'
    """
    response_object = {
        'status': 'fail',
        'message': 'User does not exist'
    }
    try:
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify(response_object), 404

        response_object = {
            'status': 'success',
            'data': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'active': user.active
            }
        }
        return jsonify(response_object), 200

    except:
        return jsonify(response_object), 404


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    """
    Add user
    ---
    definitions:
        NewUser:
            type: object
            properties:
                username:
                    type: string
                email:
                    type: string
        Response:
            type: object
            properties:
                status:
                    type: string
                message:
                    type: string
                user_id:
                    type: integer
    parameters:
        -   name: user
            in: body
            required: true
            schema:
                $ref: '#/definitions/NewUser'
    responses:
        201:
            description: success if the user was added
            schema:
                $ref: '#/definitions/Response'
    """
    body = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not body:
        return jsonify(response_object), 400

    username = body.get('username')
    email = body.get('email')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(username=username, email=email)
            db.session.add(user)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{email} was added!'
            response_object['user_id'] = user.id
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That email already exists.'
    except exc.IntegrityError as e:
        db.session.rollback()

    return jsonify(response_object), 400


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    """
    Simple ping heart beat
    ---
    definitions:
        Ping:
            type: object
            properties:
                status:
                    type: string
                message:
                    type: string
    responses:
        200:
            description: success if the service is up
            schema:
                $ref: '#/definitions/Ping'
    """
    return jsonify({
        'status': 'success',
        'message': 'ping'
    })


@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        db.session.add(User(username=username, email=email))
        db.session.commit()

    users = User.query.all()
    return render_template('index.html', users=users)
