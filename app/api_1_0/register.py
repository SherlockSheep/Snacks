from flask import jsonify, request, current_app, url_for
from . import api
from ..models import User
from .. import db

@api.route('/register/',methods=['POST'])
def new_user():
	email=request.json.get('email')
	username=request.json.get('username')
	role_id=0
	password=request.json.get('password')
	if User.query.filter_by(email=email).first():
		return jsonify({
        'error': 'email already exist'
    }), 400
	if User.query.filter_by(username=username).first():
		return jsonify({
        'error': 'username already exist'
    }), 400
	nuser=User(email=email,username=username,password='dog')
	nuser.confirmed=True
	db.session.add(nuser)
	db.session.commit()
	myid = User.query.filter_by(email=email).first().id
	return jsonify({
		'id': myid,
        'email': email,
        'username': username,
        'password': password,
    }), 201