from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Post, Permission, Tag_Enum, Snacks, User
from . import api
import json

@api.route('/post_tags/<int:id>')
def get_post_tags(id):
	post = Post.query.get_or_404(id)
	page = request.args.get('page', 1, type=int)
	pagination = post.post_tags.order_by(Tag_Enum.id.asc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	tags = pagination.items
	prev = None
	if pagination.has_prev:
		prev = url_for('api.get_post_tags', page=page-1, _external=True)
	next = None
	if pagination.has_next:
		next = url_for('api.get_post_tags', page=page+1, _external=True)
	return json.dumps([tag.to_json() for tag in tags])

@api.route('/snack_tags/<int:id>')
def get_snack_tags(id):
	snack = Snacks.query.get_or_404(id)
	page = request.args.get('page', 1, type=int)
	pagination = snack.snack_tags.order_by(Tag_Enum.id.asc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	tags = pagination.items
	prev = None
	if pagination.has_prev:
		prev = url_for('api.get_snack_tags', id=id, page=page-1, _external=True)
	next = None
	if pagination.has_next:
		next = url_for('api.get_snack_tags', id=id, page=page+1, _external=True)
	return json.dumps([tag.to_json() for tag in tags])

@api.route('/tags/')
def get_all_tags():
	page = request.args.get('page', 1, type=int)
	pagination = Tag_Enum.query.order_by(Tag_Enum.id.asc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	tags = pagination.items
	prev = None
	if pagination.has_prev:
		prev = url_for('api.get_all_tags', page=page-1, _external=True)
	next = None
	if pagination.has_next:
		next = url_for('api.get_all_tags', page=page+1, _external=True)
	return json.dumps([tag.to_json() for tag in tags])

@api.route('/new_tag/', methods=['POST'])
def new_tag():
	nliteral = request.json.get('literal')
	if nliteral== '' or nliteral == None:
		return jsonify({
		'error': 'empty tag'
	}), 400
	if Tag_Enum.query.filter_by(literal=nliteral).first():
		return jsonify({
		'error': 'tag already exist'
	}), 400
	ntag = Tag_Enum.from_json(request.json)
	db.session.add(ntag)
	db.session.commit()
	return jsonify(ntag.to_json()), 201

@api.route('/put_tag_snack/<int:tag_id>/<int:snack_id>', methods=['POST'])
def put_tag_snack(tag_id,snack_id):
	tag = Tag_Enum.query.get_or_404(tag_id)
	snack = Snacks.query.get_or_404(snack_id)
	for each_snack in tag.tag_to_snacks:
		if each_snack.name == snack.name:
			return jsonify({
        	'error': 'tag relation already exist'
    	}), 400
	tag.tag_to_snacks.append(snack)
	db.session.add(tag)
	db.session.commit()
	return jsonify({
	'Success': 'Successfully tagging'
}), 201

@api.route('/put_tag_post/<int:tag_id>/<int:post_id>', methods=['POST'])
def put_tag_post(tag_id,post_id):
	tag = Tag_Enum.query.get_or_404(tag_id)
	post = Post.query.get_or_404(post_id)
	for each_post in tag.tag_to_post:
		if each_post.id == post.id:
			return jsonify({
        	'error': 'tag relation already exist'
    	}), 400
	tag.tag_to_post.append(post)
	db.session.add(tag)
	db.session.commit()
	return jsonify({
	'Success': 'Successfully tagging'
}), 201

@api.route('/user_subscribed_tags/<int:id>')
def get_user_subscribed_tags(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.subscribe_tags.order_by(Tag_Enum.id.asc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    tags = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_subscribed_tags', id=id, page=page-1,
                       _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_subscribed_tags', id=id, page=page+1,
                       _external=True)
    return jsonify({
        'tags': [tag.to_json() for tag in tags],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })