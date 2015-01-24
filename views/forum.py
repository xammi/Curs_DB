__author__ = 'max'

from flask import Blueprint, request
from mysql.connector.errors import IntegrityError as IsDuplicate
from mysql.connector.cursor import MySQLCursorDict
from queries.forum import *
from queries.user import get_user_by_email, complete_user
from queries.thread import get_thread_by_id
from views.utils import *

app = Blueprint('forum', __name__)


@app.route("/create/", methods=['POST'])
@exceptions
def forum_create(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['name', 'short_name', 'user']
    name, short_name, user = extract_req(request.get_json(force=True), req_args)

    try:
        set_forum(cursor, name, short_name, user)
        connect.commit()
    except IsDuplicate:
        pass

    forum_id = cursor.lastrowid
    forum = get_forum_pattern(forum_id, name, short_name, user)
    cursor.close()
    return response_ok(forum)


@app.route("/details/", methods=['GET'])
@exceptions
def forum_details(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['forum']
    short_name = extract_req(request.args, req_args)
    related = extract_list(request.args, 'related', ['user'])

    forum = get_forum_by_slug(cursor, short_name)
    if 'user' in related:
        user = get_user_by_email(cursor, forum['user'])
        forum.update({'user': user})

    cursor.close()
    return response_ok(forum)


@app.route("/listPosts/", methods=['GET'])
@exceptions
def forum_posts(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['forum']
    opt_args = ['since', 'limit', 'sort', 'order']
    short_name = extract_req(request.args, req_args)
    since, limit, sort, order = extract_opt(request.args, opt_args)

    related = extract_list(request.args, 'related', ['user', 'forum', 'thread'])

    forum = get_forum_by_slug(cursor, short_name)
    posts = get_forum_posts(cursor, short_name, since, limit, sort, order)

    for post in posts:
        if 'user' in related:
            post['user'] = get_user_by_email(cursor, post['user'])

        if 'forum' in related:
            post.update({'forum': forum})

        if 'thread' in related:
            post['thread'] = get_thread_by_id(cursor, post['thread'])

    cursor.close()
    return response_ok(posts)


@app.route("/listThreads/", methods=["GET"])
@exceptions
def forum_threads(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['forum']
    opt_args = ['since', 'limit', 'order']
    short_name = extract_req(request.args, req_args)
    since, limit, order = extract_opt(request.args, opt_args)

    related = extract_list(request.args, 'related', ['user', 'forum'])

    forum = get_forum_by_slug(cursor, short_name)
    threads = get_forum_threads(cursor, short_name, since, limit, order)

    for thread in threads:
        if 'user' in related:
            thread['user'] = get_user_by_email(cursor, thread['user'])

        if 'forum' in related:
            thread['forum'] = forum

    cursor.close()
    return response_ok(threads)


@app.route("/listUsers/", methods=["GET"])
@exceptions
def forum_users(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['forum']
    opt_args = ['limit', 'order', 'since_id']
    short_name = extract_req(request.args, req_args)
    limit, order, since_id = extract_opt(request.args, opt_args)

    users = get_forum_users(cursor, short_name, limit, order, since_id)
    for user in users:
        complete_user(cursor, user)

    cursor.close()
    return response_ok(users)