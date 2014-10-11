#! coding: utf-8 -*-

from flask import Flask
from flask import request, render_template, jsonify
from mysql.connector.errors import IntegrityError as IsDuplicate
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

# Нужно ли хранить внешние ключи как id или как строки
# Как строки: индекс в виде HASH | M3

# Можно ли делать повторные запросы или нужно сделать за один
# Пытаться за один, но можно

# Как работать с иерархическими структурами в mysql
# Materialized path, конец 2 лекции


def extract(store, args):
    if hasattr(store, 'get'):
        if len(args) == 1:
            return store.get(args[0])
        return tuple(store.get(arg) for arg in args)

    if hasattr(store, '__getitem__'):
        if len(args) == 1:
            return store.get(args[0])
        return tuple(store[arg] for arg in args)


@app.route("/", methods=['GET', 'POST'])
def tester():
    tml = "test.html"
    return render_template(tml)


@app.route(API_PREFIX + "/forum/create/", methods=['POST'])
def forum_create():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    args = ['name', 'short_name', 'user']
    name, short_name, user = extract(request.json, args)

    try:
        set_forum(cursor, name, short_name, user)
        connect.commit()

        response = {'name': name, 'short_name': short_name, 'user': user}
        return jsonify({'code': OK, 'response': response})

    except IsDuplicate as e:
        return jsonify({'code': UNCORRECT_QUERY, 'response': e.message})
    except DBException as e:
        return jsonify({'code': UNKNOWN, 'response': e.message})


@app.route(API_PREFIX + "/forum/details/", methods=['GET'])
def forum_details():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    args = ['related', 'forum']
    related, short_name = extract(request.args, args)

    related = optional(related, [])

    try:
        forum = get_forum_by_slug(cursor, short_name)
        if 'user' in related:
            user = get_user_by_email(cursor, forum['founder'])
            forum.update({'user': user})

        return jsonify({'code': OK, 'response': forum})

    except NotFound as e:
        return jsonify({'code': QUIRED_NOT_FOUND, 'response': e.message})
    except DBException as e:
        return jsonify({'code': UNKNOWN, 'response': e.message})


# DEBUG
@app.route(API_PREFIX + "/forum/listPosts/", methods=['GET'])
def forum_posts():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    args = ['forum', 'since', 'limit', 'sort', 'order', 'related']
    short_name, since, limit, sort, order, related = extract(request.args, args)

    related = optional(related, [])

    try:
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

    except NotFound as e:
        return jsonify({'code': QUIRED_NOT_FOUND, 'response': e.message})


# DEBUG
@app.route(API_PREFIX + "/forum/listThreads/", methods=["GET"])
def forum_threads():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    args = ['forum', 'since', 'limit', 'order', 'related']
    short_name, since, limit, order, related = extract(request.args, args)

    related = optional(related, [])
    try:
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

    except NotFound as e:
        return jsonify({'code': QUIRED_NOT_FOUND, 'response': e.message})


# BUILD
@app.route(API_PREFIX + "/forum/listUsers/", methods=["GET"])
def forum_users():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['forum', 'limit', 'order', 'since_id']
    short_name, limit, order, since_id = extract(args)


#--------------------------------------------------------------------------------------------------


# BUILD
@app.route(API_PREFIX + "/post/create/", methods=["POST"])
def post_create():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['date', 'thread', 'message', 'user', 'forum']
    date, thread, message, user, forum = extract(request.json, req_args)
    opt_args = ['parent', 'isApproved', 'isHighlighted', 'isEdited', 'isSpam', 'isDeleted']
    parent, isApproved, isHighlighted, isEdited, isSpam, isDeleted = extract(request.args, opt_args)


# BUILD
@app.route(API_PREFIX + "/post/details/", methods=["GET"])
def post_details():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['post', 'related']
    post, related = extract(request.args, args)

    related = optional(related, [])


# BUILD
@app.route(API_PREFIX + "/post/list/", methods=["GET"])
def post_list():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['forum', 'thread', 'since', 'limit', 'sort', 'order']
    short_name, thread, since, limit, sort, order = extract(request.args, args)


@app.route(API_PREFIX + "/post/remove/", methods=["POST"])
def post_remove():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['post']
    post = extract(request.json, args)

    try:
        set_post_deleted(cursor, post, 'True')
        connect.commit()
        return jsonify({'code': OK, 'response': {'post': post}})

    except DBException as e:
        response = {'post': post, 'message': e.message}
        return jsonify({'code': UNKNOWN, 'response': response})


@app.route(API_PREFIX + "/post/restore/", methods=["POST"])
def post_restore():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['post']
    post = extract(request.json, args)

    try:
        set_post_deleted(cursor, post, 'False')
        connect.commit()
        return jsonify({'code': OK, 'response': {'post': post}})

    except DBException as e:
        response = {'post': post, 'message': e.message}
        return jsonify({'code': UNKNOWN, 'response': response})


# DEBUG
@app.route(API_PREFIX + "/post/update/", methods=["POST"])
def post_update():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['post', 'message']
    post, message = extract(request.json, args)

    try:
        set_post_message(cursor, post, message)
        connect.commit()

        post = get_post_by_id(cursor, post)
        return jsonify({'code': OK, 'response': post})

    except DBException as e:
        response = {'post': post, 'message': e.message}
        return jsonify({'code': UNKNOWN, 'response': response})


# DEBUG
@app.route(API_PREFIX + "/post/vote/", methods=["POST"])
def post_vote():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['post', 'vote']
    post, vote = extract(request.json, args)

    try:
        set_post_vote(cursor, post, vote)
        connect.commit()

        post = get_post_by_id(cursor, post)
        return jsonify({'code': OK, 'response': post})

    except DBException as e:
        response = {'post': post, 'message': e.message}
        return jsonify({'code': UNKNOWN, 'response': response})

#--------------------------------------------------------------------------------------------------

# BUILD
@app.route(API_PREFIX + "/user/create/", methods=["POST"])
def user_create():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['username', 'about', 'name', 'email', 'isAnonymous']
    username, about, name, email, isAnonymous = extract(request.json, args)


# BUILD
@app.route(API_PREFIX + "/user/details/", methods=["GET"])
def user_details():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['user']
    user = extract(request.args, args)


# BUILD
@app.route(API_PREFIX + "/user/follow/", methods=["POST"])
def user_follow():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['follower', 'followee']
    follower, followee = extract(request.json, args)


# BUILD
@app.route(API_PREFIX + "/user/listFollowers/", methods=["GET"])
def user_list_followers():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['user', 'limit', 'order', 'since_id']
    user, limit, order, since_id = extract(request.args, args)


# BUILD
@app.route(API_PREFIX + "/user/listFollowing/", methods=["GET"])
def user_list_following():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['user', 'limit', 'order', 'since_id']
    user, limit, order, since_id = extract(request.args, args)


# BUILD
@app.route(API_PREFIX + "/user/listPosts/", methods=["GET"])
def user_list_posts():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['user', 'since', 'limit', 'sort', 'order']
    user, since, limit, sort, order = extract(request.args, args)


# BUILD
@app.route(API_PREFIX + "/user/unfollow/", methods=["POST"])
def user_unfollow():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['follower', 'followee']
    follower, followee = extract(request.json, args)


# BUILD
@app.route(API_PREFIX + "/user/updateProfile/", methods=["POST"])
def user_update_profile():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['about', 'user', 'name']
    about, user, name = extract(request.json, args)


#--------------------------------------------------------------------------------------------------

# DEBUG
@app.route(API_PREFIX + "/thread/close/", methods=["POST"])
def thread_close():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['thread']
    thread = extract(request.json, args)

    try:
        set_thread_closed(cursor, thread, 'True')
        connect.commit()
        return jsonify({'code': OK, 'response': {'thread': thread}})

    except DBException as e:
        response = {'thread': thread, 'message': e.message}
        return jsonify({'code': UNKNOWN, 'response': response})


# BUILD
@app.route(API_PREFIX + "/thread/create/", methods=["POST"])
def thread_create():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['forum', 'title', 'isClosed', 'user', 'date', 'message', 'slug']
    forum, title, isClosed, user, date, message, slug = extract(request.json, req_args)
    opt_args = ['isDeleted']
    isDeleted = extract(request.json, opt_args)


# BUILD
@app.route(API_PREFIX + "/thread/details/", methods=["GET"])
def thread_details():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['thread', 'related']
    thread, related = extract(request.args, args)

    related = optional(related, [])


# BUILD
@app.route(API_PREFIX + "/thread/list/", methods=["GET"])
def thread_list():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['user', 'forum']
    user, forum = extract(request.args, req_args)
    opt_args = ['since', 'limit', 'order']
    since, limit, order = extract(request.args, opt_args)


# BUILD
@app.route(API_PREFIX + "/thread/listPosts/", methods=["GET"])
def thread_list_posts():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['thread', 'since', 'limit', 'sort', 'order']
    thread, since, limit, sort, order = extract(request.args, args)


# DEBUG
@app.route(API_PREFIX + "/thread/open/", methods=["POST"])
def thread_open():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['thread']
    thread = extract(request.json, args)

    try:
        set_thread_closed(cursor, thread, 'False')
        connect.commit()
        return jsonify({'code': OK, 'response': {'thread': thread}})

    except DBException as e:
        response = {'thread': thread, 'message': e.message}
        return jsonify({'code': UNKNOWN, 'response': response})


# DEBUG
@app.route(API_PREFIX + "/thread/remove/", methods=["POST"])
def thread_remove():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['thread']
    thread = extract(request.json, args)

    try:
        set_thread_deleted(cursor, thread, 'True')
        connect.commit()
        return jsonify({'code': OK, 'response': {'thread': thread}})

    except DBException as e:
        response = {'thread': thread, 'message': e.message}
        return jsonify({'code': UNKNOWN, 'response': response})


# DEBUG
@app.route(API_PREFIX + "/thread/restore/", methods=["POST"])
def thread_restore():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['thread']
    thread = extract(request.json, args)

    try:
        set_thread_deleted(cursor, thread, 'False')
        connect.commit()
        return jsonify({'code': OK, 'response': {'thread': thread}})

    except DBException as e:
        response = {'thread': thread, 'message': e.message}
        return jsonify({'code': UNKNOWN, 'response': response})


# BUILD
@app.route(API_PREFIX + "/thread/subscribe/", methods=["POST"])
def thread_subscribe():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['user', 'thread']
    user, thread = extract(request.json, args)


# BUILD
@app.route(API_PREFIX + "/thread/unsubscribe/", methods=["POST"])
def thread_unsubscribe():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['user', 'thread']
    user, thread = extract(request.json, args)


# DEBUG
@app.route(API_PREFIX + "/thread/update/", methods=["POST"])
def thread_update():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['message', 'slug', 'thread']
    message, slug, thread = extract(request.json, args)

    try:
        set_thread_message_slug(cursor, thread, message)
        connect.commit()

        thread = get_thread_by_id(cursor, thread)
        return jsonify({'code': OK, 'response': thread})

    except DBException as e:
        response = {'thread': thread, 'message': e.message}
        return jsonify({'code': UNKNOWN, 'response': response})


# DEBUG
@app.route(API_PREFIX + "/thread/vote/", methods=["POST"])
def thread_vote():
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    args = ['vote', 'thread']
    vote, thread = extract(request.json, args)

    try:
        set_thread_vote(cursor, thread, vote)
        connect.commit()

        thread = get_thread_by_id(cursor, thread)
        return jsonify({'code': OK, 'response': thread})

    except DBException as e:
        response = {'thread': thread, 'message': e.message}
        return jsonify({'code': UNKNOWN, 'response': response})


#--------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.debug = True
    app.run()