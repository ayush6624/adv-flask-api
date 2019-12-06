# Flask API Project   
[![Build Status](https://travis-ci.com/ayush6624/adv-flask-api.svg?branch=master)](https://travis-ci.com/ayush6624/adv-flask-api)   

Website - https://app.goyal.club

# Endpoints
- `GET /` - Homepage of the application
- `POST /upload` - The API endpoint for uploading a files via a client side application. This is protected by JWT Authentication and rate limited to 5 requests per minute. File must be passed with the key as `file`
- `POST /web/upload` - Endpoint for the Web Interface.
- `POST /user` - Signing up as a new user by providing username and password values (need to be in json format)
- `POST /auth` - Obtaining a JWT Token by providing username and password values (need to be in json format)
- `POST /refresh` - Endpoint for getting a fresh token by providing the refresh token

- This project uses flake8 guidelines.
- The API is hosted using Zeit Now (Serverless Platform) on an AWS Lambda (ap-south-1 Mumbai region) Function and all assets are served using Amazon Cloudfront. I've used MongoDB as a database solution which is deployed on a 3 node cluster on an AWS ap-south-1 instance.

# Objectives   

## Build a flask API 
- [x] A basic 2 page interface
- [x] API & interface to upload images and when you click "submit" button, it shows a new page with name of the uploaded image.
- [x] Build a key based authentication system using JWT token for accessing the api functionality.
- [x] Put in place a throttle for api call rate, let's say 5 / min.

## Docker Container Setup
The app can be built and run as a Docker container:
```bash
docker build -t flask-api .
docker run -d -p 5000:5000 --name api flask-api
```

## Local Installation Setup
```bash
pip3 install -r requirements.txt
python3 app.py
```
