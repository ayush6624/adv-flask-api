from flask import Flask, render_template, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)


@app.route('/')
@limiter.exempt
def index():
    '''
    Returns the home page of the app. Rate limiting is exempted here
    '''
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if request.files:
            upload_file = request.files['customFile']
            file_name = upload_file.filename
            print(request.headers['Content-Type'])
            if request.headers['Content-Type'] == 'application/json':
                return jsonify({"filename": file_name}, 201)
            else:
                return render_template('page.html', name=file_name), 201


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404


if __name__ == "__main__":
    app.run(debug="true", host='0.0.0.0', threaded="true")
