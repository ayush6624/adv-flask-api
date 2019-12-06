# Flask API Project   
[![Build Status](https://travis-ci.com/ayush6624/adv-flask-api.svg?branch=master)](https://travis-ci.com/ayush6624/adv-flask-api)   

Website - https://app.goyal.club

# Objectives   

## Build a flask API 
- [x] A basic 2 page interface
- [ ] API & interface to upload images and when you click "submit" button, it shows a new page with name of the uploaded image.
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