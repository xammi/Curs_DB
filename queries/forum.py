__author__ = 'max'

from utils import optional, NotFound, hierarchy_sort
from utils import prepare_post, prepare_thread, prepare_user


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
    order = optional(order, 'DESC')
    limit = optional(limit, '')
    sort = hierarchy_sort(sort)

    if limit != '':
        limit = 'LIMIT ' + limit

    query = '''SELECT *
               FROM `Post`
               WHERE `forum` = '%s' AND `date` > '%s'
               ORDER BY `date` %s %s
               %s;
            ''' % (forum, since, order, sort, limit)

    cursor.execute(query)
    posts = cursor.fetchall()

    for post in posts:
        prepare_post(post)

    return posts


def get_forum_threads(cursor, forum, since, limit, order):
    since = optional(since, '2000-01-01 00:00:00')
    order = optional(order, 'DESC')
    limit = optional(limit, '')

    if limit != '':
        limit = 'LIMIT ' + limit

    query = '''SELECT *
               FROM `Thread`
               WHERE `forum` = '%s' AND `date` > '%s'
               ORDER BY `date` %s
               %s;
            ''' % (forum, since, order, limit)

    cursor.execute(query)
    threads = cursor.fetchall()

    for thread in threads:
        prepare_thread(thread)

    return threads


def get_forum_users(cursor, forum, limit, order, since_id):
    order = optional(order, 'DESC')
    since_id = optional(since_id, '0')
    limit = optional(limit, '')

    if limit != '':
        limit = 'LIMIT ' + limit

    query = '''SELECT *
               FROM `User`
               WHERE `User`.`id` >= %s AND EXISTS (
                   SELECT * FROM `Post` WHERE `forum` = '%s' AND `user` = `User`.`email`
               )
               ORDER BY `User`.`name` %s
               %s;
            ''' % (since_id, forum, order, limit)

    cursor.execute(query)
    users = cursor.fetchall()
    for user in users:
        prepare_user(user)

    return users