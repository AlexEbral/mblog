from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import current_app
from werkzeug.security import generate_password_hash, \
     check_password_hash

mongo = None
app = None


def init_db(app_flask):
    global mongo
    mongo = PyMongo(app_flask)
    global app
    app = app_flask


def add_post(post):
    with app.app_context():
        mongo.db.posts.insert_one(post.__dict__)


def get_post(post_id):
    with app.app_context():
        post = mongo.db.posts.find_one_or_404({'_id': ObjectId(post_id)})
        post['comments'] = get_comments(post_id)
        del post['_id']
        return dumps(post)


def add_comment(comment):
    with app.app_context():
        mongo.db.comments.insert_one(comment.__dict__)


def update_post(post_id, post):
    with app.app_context():
        mongo.db.posts.update({'_id': ObjectId(post_id)}, post.__dict__)


def update_comment(comment_id, comment):
    with app.app_context():
        mongo.db.comments.update({'_id': ObjectId(comment_id)}, comment.__dict__)


def delete_post(post_id):
    with app.app_context():
        mongo.db.posts.remove({'_id': ObjectId(post_id)})


def delete_comment(comment_id):
    with app.app_context():
        mongo.db.comments.remove({'_id': ObjectId(comment_id)})


def get_posts(skip_counter, posts_limit):
    with app.app_context():
        count = mongo.db.posts.find().count()
        posts_cursor = mongo.db.posts.find().sort([('datetime', -1)]).skip(skip_counter).limit(posts_limit)

        posts = []
        for post in posts_cursor:
            id = str(post['_id'])
            del post['_id']
            post['id'] = id
            post['comments_count'] = mongo.db.comments.find({'post_id': id}).count()
            posts.append(post)

        return posts, (skip_counter + posts_limit <= count)


def get_comments(post_id):
    with app.app_context():
        comment_cursor = mongo.db.comments.find({'post_id': post_id})
        comments = []
        for comment in comment_cursor:
            id = str(comment['_id'])
            del comment['_id']
            comment['id'] = id
            comments.append(comment)
        return comments


def add_user(user):
    with app.app_context():
        mongo.db.users.insert_one(user.__dict__)

def user_exists(username):
    with app.app_context():
        user = mongo.db.users.find_one({'name': username})
        return user is not None


def check_user_hash(username, password):
    with app.app_context():
        pw_hash = mongo.db.users.find_one({'name': username})
        if pw_hash is not None:
            pw_hash = pw_hash['pwd']
            hash = check_password_hash(pw_hash, password)
            return hash


