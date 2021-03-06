__author__ = 'max'

from queries.utils import *


def get_thread_by_id(cursor, thread_id):
    thread_id = to_number(thread_id, 'thread_id')
    query = '''SELECT *
               FROM `Thread`
               WHERE `id` = %s
               LIMIT 1;
            '''
    params = (thread_id,)
    cursor.execute(query, params)

    thread = cursor.fetchone()
    if thread is None:
        raise NotFound("Thread with the '%d' id is not found" % thread_id)

    prepare_thread(thread)
    return thread


def get_thread_posts(cursor, thread, since, limit, sort, order):
    thread = to_number(thread, 'thread')
    since = optional(since, '2000-01-01 00:00:00')
    order = check_order(order, 'DESC')

    sort_stmt = prepare_sort(sort, order)
    limit_stmt = prepare_limit(limit)

    query = '''SELECT *
               FROM `Post`
               WHERE `thread` = %s AND `date` > %s
               {0} {1};
            '''.format(sort_stmt, limit_stmt)

    params = (thread, since)
    cursor.execute(query, params)

    posts = cursor.fetchall()
    if sort == 'parent_tree':
        posts = get_child_posts(cursor, posts)

    for post in posts:
        prepare_post(post)
    return posts


def set_thread(cursor, forum, title, is_closed, user, date, message, slug, is_deleted):
    is_deleted = to_bool(is_deleted, 'is_deleted')

    query = '''INSERT INTO `Thread` (`forum`, `title`, `isClosed`, `user`,
                                     `date`, `message`, `slug`, `isDeleted`)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            '''
    params = (forum, title, is_closed, user, date, message, slug, is_deleted)
    cursor.execute(query, params)

    thread = {'forum': forum, 'title': title, 'isClosed': is_closed,
              'user': user, 'date': date, 'message': message, 'slug': slug, 'isDeleted': is_deleted,
              'dislikes': 0, 'likes': 0, 'points': 0, 'posts': 0}
    return thread


def set_thread_closed(cursor, thread, logical):
    thread = to_number(thread, 'thread')
    query = '''UPDATE `Thread`
               SET `isClosed` = {0}
               WHERE `id` = %s;
            '''.format(logical)
    params = (thread,)
    cursor.execute(query, params)


def set_thread_deleted(cursor, thread, logical):
    thread = to_number(thread, 'thread')
    params = (thread,)

    posts = 0
    if logical == 'False':
        query = '''SELECT count(*) AS `posts` FROM `Post` WHERE `thread` = %s;'''
        cursor.execute(query, params)
        posts = cursor.fetchone()['posts']

    query = '''UPDATE `Thread`
               SET `isDeleted` = {0}, `posts` = {1}
               WHERE `id` = %s;
            '''.format(logical, str(posts))
    cursor.execute(query, params)

    query = '''UPDATE `Post`
               SET `isDeleted` = {0}
               WHERE `thread` = %s;
            '''.format(logical)
    cursor.execute(query, params)


def set_thread_message_slug(cursor, thread, message, slug):
    thread = to_number(thread, 'thread')
    query = '''UPDATE `Thread`
               SET `message` = %s, `slug` = %s
               WHERE `id` = %s;
            '''
    params = (message, slug, thread)
    cursor.execute(query, params)


def set_thread_vote(cursor, thread, vote):
    thread = to_number(thread, 'thread')
    if vote < 0:
        column = 'dislikes'
        points = '- 1'
    else:
        column = 'likes'
        points = '+ 1'

    query = '''UPDATE `Thread`
               SET `{0}` = `{0}` + 1, `points` = `points` {1}
               WHERE `id` = %s;
            '''.format(column, points)
    params = (thread,)
    cursor.execute(query, params)


def set_thread_subscribe(cursor, user, thread):
    thread = to_number(thread, 'thread')
    query = '''INSERT INTO `Subscribe` (`thread`, `user`)
               VALUES (%s, %s);
            '''
    params = (thread, user)
    cursor.execute(query, params)


def set_thread_unsubscribe(cursor, user, thread):
    thread = to_number(thread, 'thread')
    query = '''DELETE FROM `Subscribe`
               WHERE `thread` = %s AND `user` = %s;
            '''
    params = (thread, user)
    cursor.execute(query, params)


def get_subscribe_by_id(cursor, subs_id):
    subs_id = to_number(subs_id, 'subs_id')
    query = '''SELECT *
               FROM `Subscribe`
               WHERE `id` = %s;
            '''
    params = (subs_id,)
    cursor.execute(query, params)

    subs = cursor.fetchone()
    if subs is None:
        raise NotFound("Subscribe with the '%d' id is not found" % subs_id)

    return subs