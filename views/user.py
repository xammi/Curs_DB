__author__ = 'max'

from flask import Blueprint, request
from mysql.connector.errors import IntegrityError as IsDuplicate
from queries.user import *
from utils import *

app = Blueprint('user', __name__)


@app.route("/create/", methods=["POST"])
@exceptions
def user_create(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['email']
    cond_args = ['username', 'about', 'name']
    opt_args = ['isAnonymous']

    json = request.get_json(force=True)

    email = extract_req(json, req_args)
    username, about, name = extract_opt(json, cond_args)
    is_anonymous = extract_opt(json, opt_args)

    if is_anonymous == 'True':
        extract_req(json, cond_args)

    try:
        set_user(cursor, username, about, name, email, is_anonymous)
        connect.commit()
    except IsDuplicate:
        return jsonify({'code': USER_EXISTED, 'response': "User already exists"})

    user_id = cursor.lastrowid
    user = get_user_pattern(user_id, username, about, name, email, is_anonymous)
    return response_ok(user)


@app.route("/details/", methods=["GET"])
@exceptions
def user_details(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['user']
    user = extract_req(request.args, req_args)

    user = get_user_by_email(cursor, user)
    return response_ok(user)


@app.route("/follow/", methods=["POST"])
@exceptions
def user_follow(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['follower', 'followee']
    follower, followee = extract_req(request.get_json(force=True), req_args)

    set_user_follow(cursor, follower, followee)
    connect.commit()

    user = get_user_by_email(cursor, follower)
    return response_ok(user)


@app.route("/listFollowers/", methods=["GET"])
@exceptions
def user_list_followers(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['user']
    opt_args = ['limit', 'order', 'since_id']
    user = extract_req(request.args, req_args)
    limit, order, since_id = extract_opt(request.args, opt_args)

    followers = get_user_followers(cursor, user, limit, order, since_id)
    for follower in followers:
        complete_user(cursor, follower)

    return response_ok(followers)


@app.route("/listFollowing/", methods=["GET"])
@exceptions
def user_list_following(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['user']
    opt_args = ['limit', 'order', 'since_id']
    user = extract_req(request.args, req_args)
    limit, order, since_id = extract_opt(request.args, opt_args)

    followees = get_user_followers(cursor, user, limit, order, since_id)
    for follower in followees:
        complete_user(cursor, follower)

    return response_ok(followees)


@app.route("/listPosts/", methods=["GET"])
@exceptions
def user_list_posts(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['user']
    opt_args = ['since', 'limit', 'sort', 'order']
    user = extract_req(request.args, req_args)
    since, limit, sort, order = extract_opt(request.args, opt_args)

    posts = get_user_posts(cursor, user, since, limit, sort, order)

    return response_ok(posts)


@app.route("/unfollow/", methods=["POST"])
@exceptions
def user_unfollow(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['follower', 'followee']
    follower, followee = extract_req(request.get_json(force=True), req_args)

    set_user_unfollow(cursor, follower, followee)
    connect.commit()

    user = get_user_by_email(cursor, follower)
    return response_ok(user)


@app.route("/updateProfile/", methods=["POST"])
@exceptions
def user_update_profile(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['about', 'user', 'name']
    about, user, name = extract_req(request.get_json(force=True), req_args)

    set_user_details(cursor, user, name, about)
    connect.commit()

    user = get_user_by_email(cursor, user)
    return response_ok(user)