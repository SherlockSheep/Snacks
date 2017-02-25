from flask import jsonify, request, g, abort, url_for, current_app, send_from_directory
from . import api
import os
from werkzeug.utils import secure_filename

@api.route('/article/<int:id>')
def get_article(id):
	filename = "article_" + str(id) + ".mdown"
	if os.path.isfile(os.path.join(current_app.config['ARTICLE_DIC'],filename)):
		return send_from_directory(current_app.config['ARTICLE_DIC'],filename)
	abort(404)

@api.route('/snack_pic/<int:upc>')
def get_snack_pic(upc):
	filename = "cover_" + str(upc) + ".jpg"
	if os.path.isfile(os.path.join(current_app.config['SNACK_PIC_DIC'],filename)):
		return send_from_directory(current_app.config['SNACK_PIC_DIC'],filename)
	abort(404)

@api.route('/user_ava/<int:id>')
def get_user_ava(id):
	filename = "user_" + str(id) + ".jpg"
	if os.path.isfile(os.path.join(current_app.config['AVATAR_PIC'],filename)):
		return send_from_directory(current_app.config['AVATAR_PIC'],filename)
	else:
		return send_from_directory(current_app.config['AVATAR_PIC'],'default.jpg')
	abort(404)

@api.route('/upload', methods=['POST'])
def upload_file():
	f = request.files['file']
	fname = request.args.get('name', 1, type=str)
	if os.path.exists(current_app.config['TEST_UPLOAD']):
		if os.path.exists(os.path.join(current_app.config['TEST_UPLOAD'], fname)):
			return jsonify({
			'error': 'file name exists'
		}), 400
		f.save(os.path.join(current_app.config['TEST_UPLOAD'], fname))
		return jsonify({
		'success': 'Successfully uploading'
	}), 201
	else:
		return jsonify({
		'error': 'No such path'
	}), 400

@api.route('/upload_user_ava/<int:id>', methods=['POST'])
def upload_user_ava(id):
	f = request.files['file']
	fname = "user_" + str(id) + ".jpg"
	if os.path.exists(current_app.config['AVATAR_PIC']):
		f.save(os.path.join(current_app.config['AVATAR_PIC'], fname))
		return jsonify({
		'success': 'Successfully uploading'
	}), 201
	else:
		return jsonify({
		'error': 'No such path'
	}), 400

@api.route('/upload_snack_pic/<int:upc>', methods=['POST'])
def upload_snack_pic(upc):
	f = request.files['file']
	fname = "cover_" + str(upc) + ".jpg"
	if os.path.exists(current_app.config['SNACK_PIC_DIC']):
		f.save(os.path.join(current_app.config['SNACK_PIC_DIC'], fname))
		return jsonify({
		'success': 'Successfully uploading'
	}), 201
	else:
		return jsonify({
		'error': 'No such path'
	}), 400