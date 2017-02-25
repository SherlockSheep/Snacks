from flask import jsonify, request, g, current_app, url_for, abort
from . import api
from ..models import User, Post, Tag_Enum, Permission, Snacks
from .. import db
from .decorators import permission_required
from .errors import forbidden

@api.route('/valid_users/')
def valic_user():
    user = g.current_user
    print user
    return jsonify({
        'id': user.id
    })

@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_posts', id=id, page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_posts', id=id, page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/users/<int:id>/timeline/')
def get_user_followed_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_user_followed_posts', id=id, page=page-1,
                       _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_user_followed_posts', id=id, page=page+1,
                       _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/user_mark_snack/<int:user_id>/<int:snack_id>', methods=['POST'])
def user_mark_snack(user_id,snack_id):
    user = User.query.get_or_404(user_id)
    snack = Snacks.query.get_or_404(snack_id)
    for each_snack in user.s_marks:
        if each_snack.id == snack.id:
            return jsonify({
            'error': 'mark relation already exist'
        }), 400
    user.s_marks.append(snack)
    db.session.add(user)
    db.session.commit()
    return jsonify({
    'Success': 'Successfully marking'
}), 201

@api.route('/user_subscribe_tag/<int:user_id>/<int:tag_id>', methods=['POST'])
def user_subscribe_tag(user_id,tag_id):
    user = User.query.get_or_404(user_id)
    tag = Tag_Enum.query.get_or_404(tag_id)
    for each_tag in user.subscribe_tags:
        if each_tag.id == tag.id:
            return jsonify({
            'error': 'subscribe relation already exist'
        }), 400
    user.subscribe_tags.append(tag)
    db.session.add(user)
    db.session.commit()
    return jsonify({
    'Success': 'Successfully subscribing'
}), 201

@api.route('/snack_marking_users/<int:id>')
def get_snack_marking_users(id):
    snack = Snacks.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = snack.s_followers.order_by(User.id.asc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    users = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_snack_marking_users', id=id, page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_snack_marking_users', id=id, page=page+1, _external=True)
    return jsonify({
        'users': [user.to_json() for user in users],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })