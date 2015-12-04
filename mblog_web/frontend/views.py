from flask import render_template, Blueprint, redirect, request, current_app, session, url_for, jsonify
from mblog_web.frontend import decorators
from mblog_web import db_utils
from mblog_web import json_utils
from mblog_web import models

mod = Blueprint('main', __name__)


@mod.route('/login', methods=['GET', 'POST'])
def login():
    logger = current_app.logger
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username is None or len(username.strip()) == 0:
            logger.debug('Wrong username\password {0}'.format(username))
            return render_template('login.html', error='Enter username')

        if not db_utils.check_user_credentials(username, password):
            return render_template('login.html', error='Wrong username or password')

        session['username'] = username
        logger.debug('User logged in: {0}'.format(username))
        return redirect(url_for('.main'))
    else:
        if 'username' in session:
            return redirect(url_for('.main'))
        else:
            return render_template('login.html')


@mod.route('/reg', methods=['GET', 'POST'])
def registration():
    logger = current_app.logger
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username is None or len(username.strip()) == 0:
            logger.debug('Wrong username {0}'.format(username))
            return render_template('reg.html', error='Enter your username')

        if password is None or len(password.strip()) < 5:
            logger.debug('Wrong password {0}'.format(password))
            return render_template('reg.html', error='Password length must be greater than 5 symbols')

        if db_utils.user_exists(username):
            return render_template('reg.html', error='Selected username already in use')

        user = models.User(username, password)
        db_utils.add_user(user)
        logger.debug('New user registered: {0}'.format(username))
        session['username'] = username
        logger.debug('User logged in: {0}'.format(username))
        return redirect(url_for('.main'))
    else:
        if 'username' in session:
            return redirect(url_for('.main'))
        else:
            return render_template('reg.html')


@mod.route('/logout')
def logout():
    logger = current_app.logger
    if 'username' in session:
        logger.debug('User logged out: %s', session['username'])
        session.pop('username', None)
    return redirect('/')


@mod.route('/', methods=['GET', 'POST'])
@mod.route('/p/<post_id>', methods=['GET'])
@mod.route('/edit_post/<post_id>', methods=['GET'])
@mod.route('/new_post', methods=['GET'])
def main(post_id=None):
    name = None
    if 'username' in session:
        name = session['username']
    return render_template('main.html', name=name)


@mod.route('/post', methods=['GET'])
@decorators.login_required
def new_post():
    return render_template('main.html', name=session['username'])


@mod.route('/api/post', methods=['POST'])
@decorators.login_required
def add_post():
    post = models.Post(**request.json)
    db_utils.add_post(post)
    logger = current_app.logger
    username = session['username']
    logger.debug('User {0} added post {1}'.format(username, post.__dict__['_id']))
    return jsonify(*json_utils.ApiDataResponse(data='Successfully added'))


@mod.route('/api/post/<post_id>', methods=['PUT'])
@decorators.login_required
def update_post(post_id):
    post = models.Post(**request.json)
    db_utils.update_post(post_id, post)
    logger = current_app.logger
    username = session['username']
    logger.debug('User {0} updated his post {1}'.format(username, post_id))
    return jsonify(*json_utils.ApiDataResponse(data='Successfully updated'))


@mod.route('/api/post/<post_id>', methods=['DELETE'])
@decorators.login_required
def delete_post(post_id):
    db_utils.delete_post(post_id)
    logger = current_app.logger
    username = session['username']
    logger.debug('User {0} deleted his post {1}'.format(username, post_id))
    return jsonify(*json_utils.ApiDataResponse(data='Successfully deleted'))


@mod.route('/api/post/<post_id>', methods=['GET'])
def get_post(post_id):
    post = db_utils.get_post(post_id)
    return post


@mod.route('/api/comment', methods=['POST'])
@decorators.login_required
def add_comment():
    logger = current_app.logger
    username = session['username']
    comment = models.Comment(**request.json)
    db_utils.add_comment(comment)
    comment = comment.__dict__
    logger.debug('User {0} added comment {1}'.format(username, comment['_id']))
    comment['id'] = str(comment['_id'])
    del comment['_id']
    return jsonify(*json_utils.ApiDataResponse(data=comment))


@mod.route('/api/comment/<comment_id>', methods=['PUT'])
@decorators.login_required
def update_comment(comment_id):
    comment = models.Comment(**request.json)
    db_utils.update_comment(comment_id, comment)
    logger = current_app.logger
    username = session['username']
    logger.debug('User {0} updated his comment {1}'.format(username, comment_id))
    return jsonify(*json_utils.ApiDataResponse(data='Successfully updated'))


@mod.route('/api/comment/<comment_id>', methods=['DELETE'])
@decorators.login_required
def delete_comment(comment_id):
    logger = current_app.logger
    username = session['username']
    logger.debug('User {0} deleted his comment {1}'.format(username, comment_id))
    db_utils.delete_comment(comment_id)
    return jsonify(*json_utils.ApiDataResponse(data='Successfully deleted'))


@mod.route('/api/posts/<int:skip_counter>/<int:posts_limit>', methods=['GET', 'POST'])
def posts(skip_counter, posts_limit):
    posts, is_older_posts = db_utils.get_posts(skip_counter, posts_limit)
    return jsonify(*json_utils.ApiDataResponse(data={'posts': posts, 'is_older_posts':is_older_posts}))
