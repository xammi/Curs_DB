__author__ = 'max'

from utils import number, logic, optional, hierarchy_sort, NotFound
from utils import prepare_thread, prepare_post


def get_thread_by_id(cursor, thread_id):
    thread_id = number(thread_id, 'thread_id')
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
    since = optional(since, '2000-01-01 00:00:00')
    order = optional(order, 'DESC')
    limit = optional(limit, '')

    if limit != '':
        limit = 'LIMIT ' + limit

    sort = hierarchy_sort(sort)
    query = '''SELECT *
               FROM `Post`
               WHERE `thread` = %s AND `date` > '%s'
               ORDER BY `date` %s %s
               %s;
            ''' % (thread, since, order, sort, limit)

    cursor.execute(query)
    posts = cursor.fetchall()

    for post in posts:
        prepare_post(post)
    return posts


def set_thread(cursor, forum, title, is_closed, user, date, message, slug, is_deleted):
    is_deleted = logic(is_deleted, 'is_deleted')

    query = '''INSERT INTO `Thread` (`forum`, `title`, `isClosed`, `user`,
                                     `date`, `message`, `slug`, `isDeleted`)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            '''
    params = (forum, title, is_closed, user, date, message, slug, is_deleted)
    cursor.execute(query, params)


def set_thread_closed(cursor, thread, logical):
    thread = number(thread, 'thread')
    query = '''UPDATE `Thread`
               SET `isClosed` = {0}
               WHERE `id` = %s;
            '''.format(logical)
    params = (thread,)
    cursor.execute(query, params)


def set_thread_deleted(cursor, thread, logical):
    thread = number(thread, 'thread')
    query = '''UPDATE `Thread`
               SET `isDeleted` = {0}
               WHERE `id` = %s;
            '''.format(logical)
    params = (thread,)
    cursor.execute(query, params)

    query = '''UPDATE `Post`
               SET `isDeleted` = {0}
               WHERE `thread` = %s;
            '''.format(logical)
    cursor.execute(query, params)


def set_thread_message_slug(cursor, thread, message, slug):
    thread = number(thread, 'thread')
    query = '''UPDATE `Thread`
               SET `message` = %s, `slug` = %s
               WHERE `id` = %s;
            '''
    params = (message, slug, thread)
    cursor.execute(query, params)


def set_thread_vote(cursor, thread, vote):
    thread = number(thread, 'thread')
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
    thread = number(thread, 'thread')
    query = '''INSERT INTO `Subscribe` (`thread`, `user`)
               VALUES (%s, %s);
            '''
    params = (thread, user)
    cursor.execute(query, params)


def set_thread_unsubscribe(cursor, user, thread):
    thread = number(thread, 'thread')
    query = '''DELETE FROM `Subscribe`
               WHERE `thread` = %s AND `user` = %s;
            '''
    params = (thread, user)
    cursor.execute(query, params)


def get_subscribe_by_id(cursor, subs_id):
    subs_id = number(subs_id, 'subs_id')
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