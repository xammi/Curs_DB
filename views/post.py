__author__ = 'max'

from flask import Blueprint, request
from queries.post import *
from queries.forum import get_forum_by_slug, get_forum_posts
from queries.user import get_user_by_email
from queries.thread import get_thread_by_id, get_thread_posts
from utils import *


app = Blueprint('post', __name__)


@app.route("/create/", methods=["POST"])
@exceptions
def post_create(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['date', 'thread', 'message', 'user', 'forum']
    opt_args = ['parent', 'isApproved', 'isHighlighted', 'isEdited', 'isSpam', 'isDeleted']

    json = request.get_json(force=True)

    date, thread, message, user, forum = extract_req(json, req_args)
    parent, is_approved, is_highlighted, is_edited, is_spam, is_deleted = extract_opt(json, opt_args)

    set_post(cursor, date, thread, message, user, forum, is_deleted)
    post_id = cursor.lastrowid
    set_post_opt(cursor, post_id, parent, is_approved, is_highlighted, is_edited, is_spam)
    connect.commit()

    post = get_post_by_id(cursor, post_id)
    return response_ok(post)


@app.route("/details/", methods=["GET"])
@exceptions
def post_details(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    req_args = ['post']
    post = extract_req(request.args, req_args)
    related = extract_list(request.args, 'related', ['user', 'forum', 'thread'])

    post = get_post_by_id(cursor, post)

    if 'user' in related:
        post['user'] = get_user_by_email(cursor, post['user'])

    if 'forum' in related:
        post['forum'] = get_forum_by_slug(cursor, post['forum'])

    if 'thread' in related:
        post['thread'] = get_thread_by_id(cursor, post['thread'])

    return response_ok(post)


@app.route("/list/", methods=["GET"])
@exceptions
def post_list(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)

    opt_args = ['forum', 'thread', 'since', 'limit', 'sort', 'order']
    short_name, thread, since, limit, sort, order = extract_opt(request.args, opt_args)

    if short_name is None and thread is None:
        raise RequiredNone('forum OR thread')

    posts = []
    if not short_name is None:
        posts = get_forum_posts(cursor, short_name, since, limit, sort, order)
    elif not thread is None:
        posts = get_thread_posts(cursor, thread, since, limit, sort, order)

    return response_ok(posts)


@app.route("/remove/", methods=["POST"])
@exceptions
def post_remove(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    req_args = ['post']
    post = extract_req(request.get_json(force=True), req_args)

    set_post_deleted(cursor, post, 'True')
    connect.commit()
    return response_ok({'post': post})


@app.route("/restore/", methods=["POST"])
@exceptions
def post_restore(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    req_args = ['post']
    post = extract_req(request.get_json(force=True), req_args)

    set_post_deleted(cursor, post, 'False')
    connect.commit()
    return response_ok({'post': post})


@app.route("/update/", methods=["POST"])
@exceptions
def post_update(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    req_args = ['post', 'message']
    post, message = extract_req(request.get_json(force=True), req_args)

    set_post_message(cursor, post, message)
    connect.commit()

    post = get_post_by_id(cursor, post)
    return response_ok(post)


@app.route("/vote/", methods=["POST"])
@exceptions
def post_vote(connect):
    cursor = connect.cursor(cursor_class=MySQLCursorDict)
    req_args = ['post', 'vote']
    post, vote = extract_req(request.get_json(force=True), req_args)

    set_post_vote(cursor, post, vote)
    connect.commit()

    post = get_post_by_id(cursor, post)
    return response_ok(post)