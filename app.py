import os
import datetime
from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pymongo
from flask_jwt_extended import (JWTManager, create_access_token,
                                create_refresh_token, jwt_required,
                                jwt_refresh_token_required, get_jwt_identity)
# from bucket import client

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config['JWT_SECRET_KEY'] = os.environ.get("SECRET")
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
mongo = pymongo.MongoClient(os.environ.get("MONGO_URI"))
jwt = JWTManager(app)


@app.route('/')
@limiter.exempt
def index():
    '''
    Returns the home page of the app. Rate limiting is exempted here
    '''
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
@jwt_required
def apiUpload():
    if request.method == 'POST':
        if request.files:
            upload_file = request.files['file']
            file_name = upload_file.filename
            return jsonify({"filename": file_name}), 201


@app.route('/web/upload', methods=['POST'])
def webUpload():
    if request.method == 'POST':
        if request.files:
            upload_file = request.files['customFile']
            file_name = upload_file.filename
            return render_template('page.html', name=file_name), 201


@app.route('/user', methods=['GET', 'POST'])
def user():
    '''
    New User- Send request in json format with username and password values
    '''
    data = request.get_json()
    if request.method == 'POST':
        if data.get('username', None) and data.get('password', None):
            existing_user = mongo.api.users.find_one(
                {'username': data['username']})
            if existing_user is None:
                mongo.api.users.insert_one(data)
                return jsonify({'username': data['username'],
                                'message': 'User created successfully!'}), 200
            else:
                return jsonify({'username': data['username'],
                                'message': 'Already Exists!'}), 400

        else:
            return jsonify({'username': None,
                            'message': 'Bad request parameters!'}), 400


@app.route('/auth', methods=['POST'])
def auth_user():
    ''' Generating a token '''
    data = request.get_json()
    user = mongo.api.users.find_one({'username': data['username']})
    if user and (user['password'] == data['password']):
        del user['_id']
        del user['password']
        access_token = create_access_token(identity=user)
        refresh_token = create_refresh_token(identity=user)
        user['token'] = access_token
        user['refresh'] = refresh_token
        return jsonify({'loggedIn': True, 'username': user}), 200
    else:
        return jsonify({'loggedIn': False,
                        'message': 'Bad Request'}), 401


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    ''' refresh token endpoint '''
    current_user = get_jwt_identity()
    ret = {
        'token': create_access_token(identity=current_user)
    }
    return jsonify({'tokenRefresh': True, 'data': ret}), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404


@app.errorhandler(500)
def int_error(error):
    return jsonify({'error': 'Not Allowed'}), 403


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'status': "Forbidden",
        'message': 'Missing Authorization Header'}), 403


if __name__ == "__main__":
    app.run(debug="true", host='0.0.0.0', threaded="true")
