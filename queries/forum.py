__author__ = 'max'

from utils import *


def set_forum(cursor, name, short_name, user):
    query = '''INSERT INTO `Forum`
               (`name`, `short_name`, `user`)
               VALUES (%s, %s, %s);
            '''
    params = (name, short_name, user)
    cursor.execute(query, params)


def get_forum_by_slug(cursor, short_name):
    query = '''SELECT *
               FROM `Forum`
               WHERE `short_name` = %s
               LIMIT 1;
            '''
    params = (short_name,)
    cursor.execute(query, params)

    forum = cursor.fetchone()
    if forum is None:
        raise NotFound("Forum with the '%s' short_name is not found" % short_name)

    return forum


def get_forum_posts(cursor, forum, since, limit, sort, order):
    since = optional(since, '2000-01-01 00:00:00')
    order = check_order(order, 'DESC')

    sort_stmt = prepare_sort(sort, order)
    limit_stmt = prepare_limit(limit)

    query = '''SELECT *
               FROM `Post`
               WHERE `forum` = %s AND `date` > %s
               {0} {1};
            '''.format(sort_stmt, limit_stmt)

    params = (forum, since)
    cursor.execute(query, params)

    posts = cursor.fetchall()
    if sort == 'parent_tree':
        get_child_posts(posts)

    for post in posts:
        prepare_post(post)

    return posts


def get_forum_threads(cursor, forum, since, limit, order):
    since = optional(since, '2000-01-01 00:00:00')
    order = check_order(order, 'DESC')
    limit = prepare_limit(limit)

    query = '''SELECT *
               FROM `Thread`
               WHERE `forum` = %s AND `date` > %s
               ORDER BY `date` {0}
               {1};
            '''.format(order, limit)

    params = (forum, since)
    cursor.execute(query, params)
    threads = cursor.fetchall()

    for thread in threads:
        prepare_thread(thread)

    return threads


def get_forum_users(cursor, forum, limit, order, since_id):
    order = check_order(order, 'DESC')
    since_id = to_number(since_id, 'since_id')
    limit = prepare_limit(limit)

    query = '''SELECT *
               FROM `User`
               WHERE `User`.`id` >= %s AND EXISTS (
                   SELECT * FROM `Post` WHERE `forum` = %s AND `user` = `User`.`email`
               )
               ORDER BY `User`.`name` {0}
               {1};
            '''.format(order, limit)

    params = (since_id, forum)
    cursor.execute(query, params)

    users = cursor.fetchall()
    for user in users:
        prepare_user(user)

    return users