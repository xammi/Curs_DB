#! coding: utf-8 -*-

from flask import Flask
from flask import request, render_template, jsonify
from mysql.connector.errors import IntegrityError as IsDuplicate
from mysql.connector.errors import OperationalError as FailedConstraint
import mysql.connector
from sql_utils import *

app = Flask(__name__)
connect = mysql.connector.connect(user='root', password='22061994',
                                  host='127.0.0.1', database='forum_db')

API_PREFIX = "/db/api"
# codes of response
OK = 0
QUIRED_NOT_FOUND = 1
INVALID_QUERY = 2
UNCORRECT_QUERY = 3
UNKNOWN = 4
USER_EXISTED = 5


class exceptions():
    def __init__(self, function):
        self.function = function
        self.__name__ = function.__name__

    def __call__(self):
        try:
            return self.function()

        except RequiredNone as e:
            return jsonify({'code': INVALID_QUERY, 'response': e.msg})

        except (FailedConstraint, IsDuplicate) as e:
            return jsonify({'code': UNCORRECT_QUERY, 'response': e.msg})

        except DBException as e:
            return jsonify({'code': UNKNOWN, 'response': e.msg})


def extract_opt(store, args):
    if len(args) == 1:
        return store.get(args[0])
    return tuple(store.get(arg) for arg in args)


def extract_req(store, req_args):
    for arg in req_args:
        if store.get(arg) is None:
            raise RequiredNone(arg)

    return extract_opt(store, req_args)


@app.route("/", methods=['GET', 'POST'])
@exceptions
def tester():
    tml = "test.html"
    return render_template(tml)


@app.route(API_PREFIX + "/forum/create/", methods=['POST'])
@exceptions
def forum_create():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['name', 'short_name', 'user']
    name, short_name, user = extract_req(request.json, req_args)

    set_forum(cursor, name, short_name, user)
    connect.commit()
    forum = get_forum_by_slug(cursor, short_name)

    return jsonify({'code': OK, 'response': forum})


@app.route(API_PREFIX + "/forum/details/", methods=['GET'])
@exceptions
def forum_details():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['forum']
    opt_args = ['related']
    short_name = extract_req(request.args, req_args)
    related = extract_opt(request.args, opt_args)

    related = optional(related, [])

    forum = get_forum_by_slug(cursor, short_name)
    if 'user' in related:
        user = get_user_by_email(cursor, forum['founder'])
        forum.update({'user': user})

    return jsonify({'code': OK, 'response': forum})


# DEBUG
@app.route(API_PREFIX + "/forum/listPosts/", methods=['GET'])
@exceptions
def forum_posts():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['forum']
    opt_args = ['since', 'limit', 'sort', 'order', 'related']
    short_name = extract_req(request.args, req_args)
    since, limit, sort, order, related = extract_opt(request.args, opt_args)

    related = optional(related, [])

    forum = get_forum_by_slug(cursor, short_name)
    posts = get_forum_posts(cursor, forum['id'], since, limit, sort, order)

    for post in posts:
        user = get_user_by_id(cursor, post['user'])

        post['user'] = user['email']
        if 'user' in related:
            post['user'] = user

        if 'forum' in related:
            post.update({'forum': forum})

    return jsonify({'code': OK, 'response': posts})


# DEBUG
@app.route(API_PREFIX + "/forum/listThreads/", methods=["GET"])
@exceptions
def forum_threads():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['forum']
    opt_args = ['since', 'limit', 'order', 'related']
    short_name = extract_req(request.args, req_args)
    since, limit, order, related = extract_opt(request.args, opt_args)

    related = optional(related, [])

    forum = get_forum_by_slug(cursor, short_name)
    threads = get_forum_threads(cursor, forum['id'], since, limit, order)

    for thread in threads:
        user = get_user_by_id(cursor, thread['user'])

        thread['user'] = user['email']
        if 'user' in related:
            thread['user'] = user

        if 'forum' in related:
            thread['forum'] = forum

    return jsonify({'code': OK, 'response': threads})


# BUILD
@app.route(API_PREFIX + "/forum/listUsers/", methods=["GET"])
@exceptions
def forum_users():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['forum']
    opt_args = ['limit', 'order', 'since_id']
    short_name = extract_req(request.args, req_args)
    limit, order, since_id = extract_opt(request.args, opt_args)


#--------------------------------------------------------------------------------------------------


@app.route(API_PREFIX + "/post/create/", methods=["POST"])
@exceptions
def post_create():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['date', 'thread', 'message', 'user', 'forum']
    opt_args = ['parent', 'isApproved', 'isHighlighted', 'isEdited', 'isSpam', 'isDeleted']
    date, thread, message, user, forum = extract_req(request.json, req_args)
    parent, is_approved, is_highlighted, is_edited, is_spam, is_deleted = extract_opt(request.json, opt_args)

    set_post(cursor, date, thread, message, user, forum)
    post_id = cursor.lastrowid
    set_post_opt(cursor, post_id, parent, is_approved, is_highlighted, is_edited, is_spam, is_deleted)
    connect.commit()

    post = get_post_by_id(cursor, post_id)
    return jsonify({'code': OK, 'response': post})


# BUILD
@app.route(API_PREFIX + "/post/details/", methods=["GET"])
@exceptions
def post_details():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    req_args = ['post']
    opt_args = ['related']
    post = extract_req(request.args, req_args)
    related = extract_opt(request.args, opt_args)

    related = optional(related, [])


# BUILD
@app.route(API_PREFIX + "/post/list/", methods=["GET"])
@exceptions
def post_list():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    opt_args = ['forum', 'thread', 'since', 'limit', 'sort', 'order']
    short_name, thread, since, limit, sort, order = extract_opt(request.args, opt_args)

    if short_name is None and thread is None:
        raise RequiredNone('forum OR thread')


@app.route(API_PREFIX + "/post/remove/", methods=["POST"])
@exceptions
def post_remove():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    req_args = ['post']
    post = extract_req(request.json, req_args)

    set_post_deleted(cursor, post, 'True')
    connect.commit()
    return jsonify({'code': OK, 'response': {'post': post}})


@app.route(API_PREFIX + "/post/restore/", methods=["POST"])
@exceptions
def post_restore():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    req_args = ['post']
    post = extract_req(request.json, req_args)

    set_post_deleted(cursor, post, 'False')
    connect.commit()
    return jsonify({'code': OK, 'response': {'post': post}})


@app.route(API_PREFIX + "/post/update/", methods=["POST"])
@exceptions
def post_update():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    req_args = ['post', 'message']
    post, message = extract_req(request.json, req_args)

    set_post_message(cursor, post, message)
    connect.commit()

    post = get_post_by_id(cursor, post)
    return jsonify({'code': OK, 'response': post})


@app.route(API_PREFIX + "/post/vote/", methods=["POST"])
@exceptions
def post_vote():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    req_args = ['post', 'vote']
    post, vote = extract_req(request.json, req_args)

    set_post_vote(cursor, post, vote)
    connect.commit()

    post = get_post_by_id(cursor, post)
    return jsonify({'code': OK, 'response': post})

#--------------------------------------------------------------------------------------------------


@app.route(API_PREFIX + "/user/create/", methods=["POST"])
@exceptions
def user_create():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['username', 'about', 'name', 'email', 'isAnonymous']
    opt_args = ['isAnonymous']
    username, about, name, email = extract_req(request.json, req_args)
    is_anonymous = extract_opt(request.json, opt_args)

    set_user(cursor, username, about, name, email, is_anonymous)
    connect.commit()

    user = get_user_by_email(cursor, email)
    return jsonify({'code': OK, 'response': user})


# BUILD
@app.route(API_PREFIX + "/user/details/", methods=["GET"])
@exceptions
def user_details():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['user']
    user = extract_req(request.args, req_args)


# BUILD
@app.route(API_PREFIX + "/user/follow/", methods=["POST"])
@exceptions
def user_follow():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['follower', 'followee']
    follower, followee = extract_req(request.json, req_args)


# BUILD
@app.route(API_PREFIX + "/user/listFollowers/", methods=["GET"])
@exceptions
def user_list_followers():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['user']
    opt_args = ['limit', 'order', 'since_id']
    user = extract_req(request.args, req_args)
    limit, order, since_id = extract_opt(request.args, opt_args)


# BUILD
@app.route(API_PREFIX + "/user/listFollowing/", methods=["GET"])
@exceptions
def user_list_following():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['user']
    opt_args = ['limit', 'order', 'since_id']
    user = extract_req(request.args, req_args)
    limit, order, since_id = extract_opt(request.args, opt_args)


# BUILD
@app.route(API_PREFIX + "/user/listPosts/", methods=["GET"])
@exceptions
def user_list_posts():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['user']
    opt_args = ['since', 'limit', 'sort', 'order']
    user = extract_req(request.args, req_args)
    since, limit, sort, order = extract_opt(request.args, opt_args)


# BUILD
@app.route(API_PREFIX + "/user/unfollow/", methods=["POST"])
@exceptions
def user_unfollow():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['follower', 'followee']
    follower, followee = extract_req(request.json, req_args)


# BUILD
@app.route(API_PREFIX + "/user/updateProfile/", methods=["POST"])
@exceptions
def user_update_profile():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['about', 'user', 'name']
    about, user, name = extract_req(request.json, req_args)


#--------------------------------------------------------------------------------------------------


@app.route(API_PREFIX + "/thread/close/", methods=["POST"])
@exceptions
def thread_close():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['thread']
    thread = extract_req(request.json, req_args)

    set_thread_closed(cursor, thread, 'True')
    connect.commit()
    return jsonify({'code': OK, 'response': {'thread': thread}})


@app.route(API_PREFIX + "/thread/create/", methods=["POST"])
@exceptions
def thread_create():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['forum', 'title', 'isClosed', 'user', 'date', 'message', 'slug']
    forum, title, is_closed, user, date, message, slug = extract_req(request.json, req_args)
    opt_args = ['isDeleted']
    is_deleted = extract_opt(request.json, opt_args)

    set_thread(cursor, forum, title, is_closed, user, date, message, slug, is_deleted)
    thread_id = cursor.lastrowid
    connect.commit()

    thread = get_thread_by_id(cursor, thread_id)
    return jsonify({'code': OK, 'response': thread})


# BUILD
@app.route(API_PREFIX + "/thread/details/", methods=["GET"])
@exceptions
def thread_details():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['thread']
    opt_args = ['related']
    thread = extract_req(request.args, req_args)
    related = extract_opt(request.args, opt_args)

    related = optional(related, [])


# BUILD
@app.route(API_PREFIX + "/thread/list/", methods=["GET"])
@exceptions
def thread_list():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['user', 'forum']
    user, forum = extract_req(request.args, req_args)
    opt_args = ['since', 'limit', 'order']
    since, limit, order = extract_opt(request.args, opt_args)


# BUILD
@app.route(API_PREFIX + "/thread/listPosts/", methods=["GET"])
@exceptions
def thread_list_posts():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['thread']
    opt_args = ['since', 'limit', 'sort', 'order']
    thread = extract_req(request.args, req_args)
    since, limit, sort, order = extract_opt(request.args, opt_args)


@app.route(API_PREFIX + "/thread/open/", methods=["POST"])
@exceptions
def thread_open():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['thread']
    thread = extract_req(request.json, req_args)

    set_thread_closed(cursor, thread, 'False')
    connect.commit()
    return jsonify({'code': OK, 'response': {'thread': thread}})


@app.route(API_PREFIX + "/thread/remove/", methods=["POST"])
@exceptions
def thread_remove():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['thread']
    thread = extract_req(request.json, req_args)

    set_thread_deleted(cursor, thread, 'True')
    connect.commit()
    return jsonify({'code': OK, 'response': {'thread': thread}})


@app.route(API_PREFIX + "/thread/restore/", methods=["POST"])
@exceptions
def thread_restore():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['thread']
    thread = extract_req(request.json, req_args)

    set_thread_deleted(cursor, thread, 'False')
    connect.commit()
    return jsonify({'code': OK, 'response': {'thread': thread}})


# BUILD
@app.route(API_PREFIX + "/thread/subscribe/", methods=["POST"])
@exceptions
def thread_subscribe():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['user', 'thread']
    user, thread = extract_req(request.json, req_args)


# BUILD
@app.route(API_PREFIX + "/thread/unsubscribe/", methods=["POST"])
@exceptions
def thread_unsubscribe():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['user', 'thread']
    user, thread = extract_req(request.json, req_args)


@app.route(API_PREFIX + "/thread/update/", methods=["POST"])
@exceptions
def thread_update():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['message', 'slug', 'thread']
    message, slug, thread = extract_req(request.json, req_args)

    set_thread_message_slug(cursor, thread, message, slug)
    connect.commit()

    thread = get_thread_by_id(cursor, thread)
    return jsonify({'code': OK, 'response': thread})


@app.route(API_PREFIX + "/thread/vote/", methods=["POST"])
@exceptions
def thread_vote():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['vote', 'thread']
    vote, thread = extract_req(request.json, req_args)

    set_thread_vote(cursor, thread, vote)
    connect.commit()

    thread = get_thread_by_id(cursor, thread)
    return jsonify({'code': OK, 'response': thread})


#--------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.debug = True
    app.run()