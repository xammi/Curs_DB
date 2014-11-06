__author__ = 'max'

from utils import *


def set_user(cursor, username, about, name, email, is_anonymous):
    is_anonymous = to_bool(is_anonymous, 'is_anonymous')
    query = '''INSERT INTO `User` (`username`, `about`, `email`, `name`, `isAnonymous`)
               VALUES (%s, %s, %s, %s, %s);
            '''
    params = (username, about, email, name, is_anonymous)
    cursor.execute(query, params)


def get_followers_list(cursor, email):
    query = '''SELECT `follower`
               FROM `Follow`
               WHERE `followee` = %s;
            '''
    params = (email,)
    cursor.execute(query, params)
    return cursor.fetchall()


def get_following_list(cursor, email):
    query = '''SELECT `followee`
               FROM `Follow`
               WHERE `follower` = %s;
            '''
    params = (email,)
    cursor.execute(query, params)
    return cursor.fetchall()


def get_user_subs(cursor, email):
    query = '''SELECT `thread`
               FROM `Subscribe`
               WHERE `user` = %s;
            '''
    params = (email,)
    cursor.execute(query, params)
    return cursor.fetchall()


def complete_user(cursor, user):
    email = user['email']
    user['followers'] = get_followers_list(cursor, email)
    user['following'] = get_following_list(cursor, email)
    user['subscriptions'] = get_user_subs(cursor, email)
    return user


def get_user_by_email(cursor, email):
    query = '''SELECT *
               FROM `User`
               WHERE `email` = %s;
            '''
    params = (email,)
    cursor.execute(query, params)

    user = cursor.fetchone()
    if user is None:
        raise NotFound("User with the '%s' email is not found" % email)

    complete_user(cursor, user)
    prepare_user(user)
    return user


def set_user_details(cursor, user, name, about):
    query = '''UPDATE `User`
               SET `name` = %s, `about` = %s
               WHERE `email` = %s;
            '''
    params = (name, about, user)
    cursor.execute(query, params)


def set_user_follow(cursor, follower, followee):
    query = '''INSERT INTO `Follow` (`follower`, `followee`)
               VALUES (%s, %s);
            '''
    params = (follower, followee)
    cursor.execute(query, params)


def set_user_unfollow(cursor, follower, followee):
    query = '''DELETE FROM `Follow`
               WHERE `follower` = %s AND `followee` = %s;
            '''
    params = (follower, followee)
    cursor.execute(query, params)


def get_user_followers(cursor, user, limit, order, since_id):
    limit = prepare_limit(limit)
    order = check_order(order, 'DESC')
    since_id = to_number(since_id, 'since_id')

    query = '''SELECT *
               FROM `Follow` AS F
               JOIN `User` AS U ON F.`follower` = U.`email`
               WHERE `followee` = %s AND U.`id` >= %s
               ORDER BY `name` {0}
               {1};
            '''.format(order, limit)
    params = (user, since_id)
    cursor.execute(query, params)

    users = cursor.fetchall()
    for user in users:
        prepare_user(user)

    return users


def get_user_following(cursor, user, limit, order, since_id):
    limit = prepare_limit(limit)
    order = check_order(order, 'DESC')
    since_id = to_number(since_id, 'since_id')

    query = '''SELECT *
               FROM `Follow` AS F
               JOIN `User` AS U ON F.`followee` = U.`email`
               WHERE `follower` = %s AND U.`id` >= %s
               ORDER BY `name` {0}
               {1};
            '''.format(order, limit)
    params = (user, since_id)
    cursor.execute(query, params)

    users = cursor.fetchall()
    for user in users:
        prepare_user(user)

    return users


def get_user_posts(cursor, user, since, limit, sort, order):
    since = optional(since, '2000-01-01 00:00:00')
    order = check_order(order, 'DESC')

    sort_stmt = prepare_sort(sort, order)
    limit_stmt = prepare_limit(limit)

    query = '''SELECT *
               FROM `Post`
               WHERE `user` = %s AND `date` > %s
               {0} {1};
            '''.format(sort_stmt, limit_stmt)
    params = (user, since)
    cursor.execute(query, params)

    posts = cursor.fetchall()
    if sort == 'parent_tree':
        get_child_posts(posts)

    for post in posts:
        prepare_post(post)

    return posts


def get_user_threads(cursor, user, since, limit, order):
    since = optional(since, '2000-01-01 00:00:00')
    order = check_order(order, 'DESC')
    limit = prepare_limit(limit)

    query = '''SELECT *
               FROM `Thread`
               WHERE `user` = %s AND `date` > %s
               ORDER BY `date` {0}
               {1};
            '''.format(order, limit)
    params = (user, since)
    cursor.execute(query, params)

    threads = cursor.fetchall()
    for thread in threads:
        prepare_thread(thread)

    return threads
