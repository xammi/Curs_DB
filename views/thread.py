__author__ = 'max'

from flask import Blueprint, request
from queries.thread import *
from queries.forum import get_forum_by_slug, get_forum_threads
from queries.user import get_user_by_email, get_user_threads
from queries.thread import get_thread_by_id, get_thread_posts
from utils import *

app = Blueprint('thread', __name__)


@app.route("/close/", methods=["POST"])
@exceptions
def thread_close(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['thread']
    thread = extract_req(request.json, req_args)

    set_thread_closed(cursor, thread, 'True')
    connect.commit()
    return response_ok({'thread': thread})


@app.route("/create/", methods=["POST"])
@exceptions
def thread_create(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['forum', 'title', 'isClosed', 'user', 'date', 'message', 'slug']
    forum, title, is_closed, user, date, message, slug = extract_req(request.json, req_args)
    opt_args = ['isDeleted']
    is_deleted = extract_opt(request.json, opt_args)

    set_thread(cursor, forum, title, is_closed, user, date, message, slug, is_deleted)
    thread_id = cursor.lastrowid
    connect.commit()

    thread = get_thread_by_id(cursor, thread_id)
    return response_ok(thread)


@app.route("/details/", methods=["GET"])
@exceptions
def thread_details(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['thread']
    thread = extract_req(request.args, req_args)
    related = extract_list(request.args, 'related', ['user', 'forum'])

    thread = get_thread_by_id(cursor, thread)

    if 'user' in related:
        thread['user'] = get_user_by_email(cursor, thread['user'])

    if 'forum' in related:
        thread['forum'] = get_forum_by_slug(cursor, thread['forum'])

    return response_ok(thread)


@app.route("/list/", methods=["GET"])
@exceptions
def thread_list(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    opt_args = ['user', 'forum', 'since', 'limit', 'order']
    user, forum, since, limit, order = extract_opt(request.args, opt_args)

    if user is None and forum is None:
        raise RequiredNone('user OR forum')

    threads = []
    if not user is None:
        threads = get_user_threads(cursor, user, since, limit, order)
    elif not forum is None:
        threads = get_forum_threads(cursor, forum, since, limit, order)

    return response_ok(threads)


@app.route("/listPosts/", methods=["GET"])
@exceptions
def thread_list_posts(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['thread']
    opt_args = ['since', 'limit', 'sort', 'order']
    thread = extract_req(request.args, req_args)
    since, limit, sort, order = extract_opt(request.args, opt_args)

    posts = get_thread_posts(cursor, thread, since, limit, sort, order)

    return response_ok(posts)


@app.route("/open/", methods=["POST"])
@exceptions
def thread_open(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['thread']
    thread = extract_req(request.json, req_args)

    set_thread_closed(cursor, thread, 'False')
    connect.commit()
    return response_ok({'thread': thread})


@app.route("/remove/", methods=["POST"])
@exceptions
def thread_remove(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['thread']
    thread = extract_req(request.json, req_args)

    set_thread_deleted(cursor, thread, 'True')
    connect.commit()
    return response_ok({'thread': thread})


@app.route("/restore/", methods=["POST"])
@exceptions
def thread_restore(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['thread']
    thread = extract_req(request.json, req_args)

    set_thread_deleted(cursor, thread, 'False')
    connect.commit()
    return response_ok({'thread': thread})


@app.route("/subscribe/", methods=["POST"])
@exceptions
def thread_subscribe(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['user', 'thread']
    user, thread = extract_req(request.json, req_args)

    set_thread_subscribe(cursor, user, thread)
    connect.commit()

    subs = {'thread': thread, 'user': user}
    return response_ok(subs)


@app.route("/unsubscribe/", methods=["POST"])
@exceptions
def thread_unsubscribe(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['user', 'thread']
    user, thread = extract_req(request.json, req_args)

    set_thread_unsubscribe(cursor, user, thread)
    connect.commit()

    subs = {'thread': thread, 'user': user}
    return response_ok(subs)


@app.route("/update/", methods=["POST"])
@exceptions
def thread_update(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['message', 'slug', 'thread']
    message, slug, thread = extract_req(request.json, req_args)

    set_thread_message_slug(cursor, thread, message, slug)
    connect.commit()

    thread = get_thread_by_id(cursor, thread)
    return response_ok(thread)


@app.route("/vote/", methods=["POST"])
@exceptions
def thread_vote(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['vote', 'thread']
    vote, thread = extract_req(request.json, req_args)

    set_thread_vote(cursor, thread, vote)
    connect.commit()

    thread = get_thread_by_id(cursor, thread)
    return response_ok(thread)
