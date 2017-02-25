from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Post, Permission, Tag_Enum, Snacks, User
from . import api
import json

@api.route('/snacks/')
def get_all_snacks():
	page = request.args.get('page', 1, type=int)
	pagination = Snacks.query.order_by(Snacks.id.asc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	snacks = pagination.items
	prev = None
	if pagination.has_prev:
		prev = url_for('api.get_all_snacks', page=page-1, _external=True)
	next = None
	if pagination.has_next:
		next = url_for('api.get_all_snacks', page=page+1, _external=True)
	return json.dumps([snack.to_json() for snack in snacks])

@api.route('/snacks/testlist')
def get_all_snacks_list():
	page = request.args.get('page', 1, type=int)
	pagination = Snacks.query.order_by(Snacks.id.asc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	snacks = pagination.items
	prev = None
	if pagination.has_prev:
		prev = url_for('api.get_all_snacks_list', page=page-1, _external=True)
	next = None
	if pagination.has_next:
		next = url_for('api.get_all_snacks_list', page=page+1, _external=True)
	return jsonify({
		'snacks': [snack.to_json() for snack in snacks],
		'prev': prev,
		'next': next,
		'count': pagination.total
	})

@api.route('/snacks/<int:left>/<int:right>/interval/')
def get_snacks_interval(left,right):
	page = request.args.get('page', 1, type=int)
	pagination = Snacks.query.filter(((Snacks.id>=left)&(Snacks.id<=right))).order_by(Snacks.id.asc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	snacks = pagination.items
	prev = None
	if pagination.has_prev:
		prev = url_for('api.get_snacks_interval', left=left, right=right, page=page-1, _external=True)
	next = None
	if pagination.has_next:
		next = url_for('api.get_snacks_interval', left=left, right=right, page=page+1, _external=True)
	return jsonify({
		'snacks': [snack.to_json() for snack in snacks],
		'prev': prev,
		'next': next,
		'count': pagination.total
	})

@api.route('/snacks_by_keyword/',methods=['POST'])
def snacks_by_keyword():
	keyword = request.json.get('keyword')
	page = request.args.get('page', 1, type=int)
	pagination = Snacks.query.filter(Snacks.name.like(keyword)).order_by(Snacks.id.asc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	snacks = pagination.items
	prev = None
	if pagination.has_prev:
		prev = url_for('api.get_snacks_interval', page=page-1, _external=True)
	next = None
	if pagination.has_next:
		next = url_for('api.get_snacks_interval', page=page+1, _external=True)
	return json.dumps([snack.to_json() for snack in snacks])

@api.route('/snacks/<int:id>')
def get_snack(id):
	snack = Snacks.query.get_or_404(id)
	return jsonify(snack.to_json())

@api.route('/new_snack/', methods=['POST'])
def new_snack():
	name = request.json.get('name')
	if Snacks.query.filter_by(name=name).first():
		return jsonify({
        'error': 'snack already exist'
    }), 400
	snack = Snacks.from_json(request.json)
	db.session.add(snack)
	db.session.commit()
	return jsonify(snack.to_json()), 201

@api.route('/taged_snacks/<int:id>')
def get_taged_snacks(id):
	tag = Tag_Enum.query.get_or_404(id)
	page = request.args.get('page', 1, type=int)
	pagination = tag.tag_to_snacks.order_by(Snacks.id.asc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	snacks = pagination.items
	prev = None
	if pagination.has_prev:
		prev = url_for('api.get_taged_snacks', id=id, page=page-1, _external=True)
	next = None
	if pagination.has_next:
		next = url_for('api.get_taged_snacks', id=id, page=page+1, _external=True)
	return jsonify({
		'snacks': [snack.to_json() for snack in snacks],
		'prev': prev,
		'next': next,
		'count': pagination.total
	})

@api.route('/related_snacks/<int:id>')
def get_related_snacks(id):
	post = Post.query.get_or_404(id)
	page = request.args.get('page', 1, type=int)
	pagination = post.related_snack.order_by(Snacks.id.asc()).paginate(
		page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
		error_out=False)
	snacks = pagination.items
	prev = None
	if pagination.has_prev:
		prev = url_for('api.get_related_snacks', id=id, page=page-1, _external=True)
	next = None
	if pagination.has_next:
		next = url_for('api.get_related_snacks', id=id, page=page+1, _external=True)
	return jsonify({
		'snacks': [snack.to_json() for snack in snacks],
		'prev': prev,
		'next': next,
		'count': pagination.total
	})

@api.route('/user_marked_snacks/<int:id>')
def get_user_marked_snacks(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.s_marks.order_by(Snacks.id.asc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    snacks = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_marked_snacks', id=id, page=page-1,
                       _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_marked_snacks', id=id, page=page+1,
                       _external=True)
    return json.dumps([snack.to_json() for snack in snacks])