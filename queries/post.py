__author__ = 'max'

from utils import *


def get_post_by_id(cursor, post_id):
    post_id = to_number(post_id, 'post_id')
    query = '''SELECT *
               FROM `Post`
               WHERE `id` = %s
               LIMIT 1;
            '''
    params = (post_id,)
    cursor.execute(query, params)

    post = cursor.fetchone()
    if post is None:
        raise NotFound("Post with the '%d' id is not found" % post_id)

    prepare_post(post)
    return post


def set_post(cursor, date, thread, message, user, forum, is_deleted):
    is_deleted = to_bool(is_deleted, 'is_deleted')
    thread = to_number(thread, 'thread')

    query = '''INSERT INTO `Post` (`date`, `thread`, `message`, `user`, `forum`, `isDeleted`)
               VALUES (%s, %s, %s, %s, %s, %s);
            '''

    params = (date, thread, message, user, forum, is_deleted)
    cursor.execute(query, params)


def set_post_opt(cursor, post_id, parent, is_approved, is_highlighted, is_edited, is_spam):
    is_approved = to_bool(is_approved, 'is_approved')
    is_highlighted = to_bool(is_highlighted, 'is_highlighted')
    is_edited = to_bool(is_edited, 'is_edited')
    is_spam = to_bool(is_spam, 'is_spam')
    post_id = to_number(post_id, 'post_id')

    query = '''UPDATE `Post`
               SET `parent` = %s, `isApproved` = %s, `isHighlighted` = %s,
                   `isEdited` = %s, `isSpam` = %s
               WHERE `id` = %s;
            '''
    params = (parent, is_approved, is_highlighted, is_edited, is_spam, post_id)
    cursor.execute(query, params)


def set_post_deleted(cursor, post, logical):
    post = to_number(post, 'post')
    query = '''UPDATE `Post`
               SET `isDeleted` = {0}
               WHERE `id` = %s;
            '''.format(logical)
    params = (post,)
    cursor.execute(query, params)

    if logical == 'True':
        logical = '- 1'
    else:
        logical = '+ 1'

    post = get_post_by_id(cursor, post)
    query = '''UPDATE `Thread`
               SET `posts` = `posts` {0}
               WHERE `id` = %s;
            '''.format(logical)
    params = (post['thread'],)
    cursor.execute(query, params)


def set_post_message(cursor, post, message):
    post = to_number(post, 'post')
    query = '''UPDATE `Post`
               SET `message` = %s
               WHERE `id` = %s;
            '''

    params = (message, post)
    cursor.execute(query, params)


def set_post_vote(cursor, post, vote):
    post = to_number(post, 'post')

    if vote < 0:
        column = 'dislikes'
        points = '- 1'
    else:
        column = 'likes'
        points = '+ 1'

    query = '''UPDATE `Post`
               SET `{0}` = `{0}` + 1, `points` = `points` {1}
               WHERE `id` = %s;
            '''.format(column, points)
    params = (post,)
    cursor.execute(query, params)