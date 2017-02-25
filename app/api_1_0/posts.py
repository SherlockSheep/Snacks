from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Post, Permission, Tag_Enum, Snacks
from . import api
from .decorators import permission_required
from .errors import forbidden
import json

@api.route('/posts/')
def get_posts():
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_posts', page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api.route('/posts/<int:id>')
def get_post(id):
    post = Post.query.get_or_404(id)
    return jsonify(post.to_json())


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_post():
    post = Post.from_json(request.json)
    post.author = g.current_user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json()), 201, \
        {'Location': url_for('api.get_post', id=post.id, _external=True)}


@api.route('/posts/<int:id>', methods=['PUT'])
def edit_post(id):
    post = Post.query.get_or_404(id)
    if g.current_user != post.author and \
            not g.current_user.can(Permission.ADMINISTER):
        return forbidden('Insufficient permissions')
    post.body = request.json.get('body', post.body)
    db.session.add(post)
    return jsonify(post.to_json())

@api.route('/taged_posts/<int:id>')
def get_taged_posts(id):
    tag = Tag_Enum.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = tag.tag_to_post.order_by(Post.id.asc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_taged_posts', id=id, page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_taged_posts', id=id, page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })

@api.route('/relate_post_snack/<int:post_id>/<int:snack_id>', methods=['POST'])
def relate_post_snack(post_id,snack_id):
    post = Post.query.get_or_404(post_id)
    snack = Snacks.query.get_or_404(snack_id)
    for each_snack in post.related_snack:
        if each_snack.name == snack.name:
            return jsonify({
            'error': 'relation already exist'
        }), 400
    post.related_snack.append(snack)
    db.session.add(post)
    db.session.commit()
    return jsonify({
    'Success': 'Successfully relationing'
}), 201

@api.route('/related_posts/<int:id>')
def get_related_posts(id):
    snack = Snacks.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = snack.related_post.order_by(Post.id.asc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_related_posts', id=id, page=page-1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_related_posts', id=id, page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })
