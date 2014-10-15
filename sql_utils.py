__author__ = 'max'

from mysql.connector.cursor import MySQLCursor


def optional(obj, default):
    if obj is None or obj == '':
        return default
    return obj


def hierarchy_sort(sort):
    if sort is None or sort == 'flat':
        sort = ''
    elif sort == 'tree':
        sort = ', `parent` ASC'
    elif sort == 'parent_tree':
        sort = ', `parent` ASC'

    return sort

#--------------------------------------------------------------------------------------------------


class MySQLCursorDict(MySQLCursor):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            if len(self.column_names) == 1:
                return row[0]
            return dict(zip(self.column_names, row))
        return None


class DBException(Exception):
    def __init__(self, message):
        self.msg = message


class NotFound(DBException):
    def __init__(self, message):
        self.msg = message


class RequiredNone(DBException):
    def __init__(self, arg):
        self.msg = 'Required parameter (%s) not found' % arg


class WrongType(DBException):
    def __init__(self, param, right_type):
        self.msg = 'Parameter (%s) must be of %s type' % (param, right_type)


def number(string, param):
    try:
        return int(string)
    except ValueError:
        raise WrongType(param, 'integer')


def logic(obj, param):
    try:
        return bool(obj)
    except ValueError:
        raise WrongType(param, 'bool')


thread_bools = ['isClosed', 'isDeleted']
post_bools = ['isApproved', 'isHighlighted', 'isDeleted', 'isSpam', 'isEdited']
bu = 'isAnonymous'


def prepare_thread(thread):
    thread['date'] = thread['date'].strftime("%Y-%m-%d %H:%M:%S")
    for bt in thread_bools:
        thread[bt] = logic(thread[bt], bt)


def prepare_post(post):
    post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")
    for bp in post_bools:
        post[bp] = logic(post[bp], bp)


def prepare_user(user):
    user[bu] = logic(user[bu], bu)

# queries -----------------------------------------------------------------------------------------


def clear_all(cursor):
    query = '''SET FOREIGN_KEY_CHECKS=0'''
    cursor.execute(query)

    tables = ['User', 'Forum', 'Thread', 'Post', 'Follow', 'Subscribe']
    for table in tables:
        query = '''TRUNCATE TABLE `%s`;''' % table
        cursor.execute(query)

    query = '''SET FOREIGN_KEY_CHECKS=1'''
    cursor.execute(query)


def set_forum(cursor, name, short_name, user):
    query = '''INSERT INTO `Forum`
               (`name`, `short_name`, `user`)
               VALUES ('%s', '%s', '%s');
            ''' % (name, short_name, user)
    cursor.execute(query)


def get_forum_by_slug(cursor, short_name):
    short_name = optional(short_name, 'no_name')

    query = '''SELECT *
               FROM `Forum`
               WHERE `short_name` = '%s'
               LIMIT 1;
            ''' % short_name
    cursor.execute(query)

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
    since_id = optional(since_id, 0)
    limit = optional(limit, '')

    if limit != '':
        limit = 'LIMIT ' + limit

    query = '''SELECT *
               FROM `User`
               WHERE `User`.`id` > %s AND EXISTS (
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

#--------------------------------------------------------------------------------------------------


def get_post_by_id(cursor, post_id):
    query = '''SELECT *
               FROM `Post`
               WHERE `id` = %s
               LIMIT 1;
            ''' % post_id
    cursor.execute(query)

    post = cursor.fetchone()
    if post is None:
        raise NotFound("Post with the '%s' id is not found" % post_id)

    prepare_post(post)
    return post


def set_post(cursor, date, thread, message, user, forum, is_deleted):
    is_deleted = optional(is_deleted, 'false')

    query = '''INSERT INTO `Post` (`date`, `thread`, `message`, `user`, `forum`, `isDeleted`)
               VALUES ('%s', %s, '%s', '%s', '%s', %s);
            ''' % (date, thread, message, user, forum, is_deleted)
    cursor.execute(query)


def set_post_opt(cursor, post_id, parent, is_approved, is_highlighted, is_edited, is_spam):
    parent = optional(parent, 'NULL')
    is_approved = optional(is_approved, 'false')
    is_highlighted = optional(is_highlighted, 'false')
    is_edited = optional(is_edited, 'false')
    is_spam = optional(is_spam, 'false')

    query = '''UPDATE `Post`
               SET `parent` = %s, `isApproved` = %s, `isHighlighted` = %s,
                   `isEdited` = %s, `isSpam` = %s
               WHERE `id` = %s;
            ''' % (parent, is_approved, is_highlighted, is_edited, is_spam, post_id)

    cursor.execute(query)


def set_post_deleted(cursor, post, logical):
    query = '''UPDATE `Post`
               SET `isDeleted` = %s
               WHERE `id` = %s;
            ''' % (logical, post)

    cursor.execute(query)


def set_post_message(cursor, post, message):
    query = '''UPDATE `Post`
               SET `message` = '%s'
               WHERE `id` = %s;
            ''' % (message, post)

    cursor.execute(query)


def set_post_vote(cursor, post, vote):
    if vote < 0:
        column = 'dislikes'
        points = '- 1'
    else:
        column = 'likes'
        points = '+ 1'

    query = '''UPDATE `Post`
               SET `%s` = `%s` + 1, `points` = `points` %s
               WHERE `id` = %s;
            ''' % (column, column, points, post)

    cursor.execute(query)

#--------------------------------------------------------------------------------------------------


def set_user(cursor, username, about, name, email, is_anonymous):
    is_anonymous = optional(is_anonymous, 'false')

    query = '''INSERT INTO `User` (`username`, `about`, `email`, `name`, `isAnonymous`)
               VALUES ('%s', '%s', '%s', '%s', %s);
            ''' % (username, about, email, name, is_anonymous)

    cursor.execute(query)


def get_followers_list(cursor, email):
    query = '''SELECT `follower`
               FROM `Follow`
               WHERE `followee` = '%s';
            ''' % email
    cursor.execute(query)
    return cursor.fetchall()


def get_following_list(cursor, email):
    query = '''SELECT `followee`
               FROM `Follow`
               WHERE `follower` = '%s';
            ''' % email
    cursor.execute(query)
    return cursor.fetchall()


def get_user_subs(cursor, email):
    query = '''SELECT `thread`
               FROM `Subscribe`
               WHERE `user` = '%s';
            ''' % email
    cursor.execute(query)
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
               WHERE `email` = '%s';
            ''' % email
    cursor.execute(query)

    user = cursor.fetchone()
    if user is None:
        raise NotFound("User with the '%s' email is not found" % email)

    complete_user(cursor, user)

    if user[bu]:
        user['about'] = None
        user['name'] = None
        user['username'] = None

    prepare_user(user)
    return user


def set_user_details(cursor, user, name, about):
    query = '''UPDATE `User`
               SET `name` = '%s', `about` = '%s'
               WHERE `email` = '%s';
            ''' % (name, about, user)

    cursor.execute(query)


def set_user_follow(cursor, follower, followee):
    query = '''INSERT INTO `Follow` (`follower`, `followee`)
               VALUES ('%s', '%s');
            ''' % (follower, followee)

    cursor.execute(query)


def set_user_unfollow(cursor, follower, followee):
    query = '''DELETE FROM `Follow`
               WHERE `follower` = '%s' AND `followee` = '%s';
            ''' % (follower, followee)

    cursor.execute(query)


def get_user_followers(cursor, user, limit, order, since_id):
    limit = optional(limit, '')
    order = optional(order, 'DESC')
    since_id = optional(since_id, 0)

    if limit != '':
        limit = 'LIMIT ' + limit

    query = '''SELECT *
               FROM `Follow` AS F
               JOIN `User` AS U ON F.`followee` = U.`email`
               WHERE `follower` = '%s' AND U.`id` > %s
               ORDER BY `name` %s
               %s;
            ''' % (user, since_id, order, limit)

    cursor.execute(query)
    users = cursor.fetchall()
    for user in users:
        prepare_user(user)

    return users


def get_user_following(cursor, user, limit, order, since_id):
    limit = optional(limit, '')
    order = optional(order, 'DESC')
    since_id = optional(since_id, 0)

    if limit != '':
        limit = 'LIMIT ' + limit

    query = '''SELECT *
               FROM `Follow` AS F
               JOIN `User` AS U ON F.`follower` = U.`email`
               WHERE `followee` = '%s' AND U.`id` > %s
               ORDER BY `name` %s
               %s;
            ''' % (user, since_id, order, limit)

    cursor.execute(query)
    users = cursor.fetchall()
    for user in users:
        prepare_user(user)

    return users


def get_user_posts(cursor, user, since, limit, sort, order):
    since = optional(since, '2000-01-01 00:00:00')
    order = optional(order, 'DESC')
    limit = optional(limit, '')

    if limit != '':
        limit = 'LIMIT ' + limit

    sort = hierarchy_sort(sort)
    query = '''SELECT *
               FROM `Post`
               WHERE `user` = '%s' AND `date` > '%s'
               ORDER BY `date` %s %s
               %s;
            ''' % (user, since, order, sort, limit)

    cursor.execute(query)
    posts = cursor.fetchall()

    for post in posts:
        prepare_post(post)

    return posts


def get_user_threads(cursor, user, since, limit, order):
    since = optional(since, '2000-01-01 00:00:00')
    order = optional(order, 'DESC')
    limit = optional(limit, '')

    if limit != '':
        limit = 'LIMIT ' + limit

    query = '''SELECT *
               FROM `Thread`
               WHERE `user` = '%s' AND `date` > '%s'
               ORDER BY `date` %s
               %s;
            ''' % (user, since, order, limit)

    cursor.execute(query)
    threads = cursor.fetchall()

    for thread in threads:
        prepare_thread(thread)

    return threads


#--------------------------------------------------------------------------------------------------


def get_thread_by_id(cursor, thread_id):
    query = '''SELECT *
               FROM `Thread`
               WHERE `id` = %s
               LIMIT 1;
            ''' % thread_id
    cursor.execute(query)

    thread = cursor.fetchone()
    if thread is None:
        raise NotFound("Thread with the '%s' id is not found" % thread_id)

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
    is_deleted = optional(is_deleted, 'false')

    query = '''INSERT INTO `Thread` (`forum`, `title`, `isClosed`, `user`,
                                     `date`, `message`, `slug`, `isDeleted`)
               VALUES ('%s', '%s', %s, '%s', '%s', '%s', '%s', %s);
            ''' % (forum, title, is_closed, user, date, message, slug, is_deleted)

    cursor.execute(query)


def set_thread_closed(cursor, thread, logical):
    query = '''UPDATE `Thread`
               SET `isClosed` = %s
               WHERE `id` = %s;
            ''' % (logical, thread)

    cursor.execute(query)


def set_thread_deleted(cursor, thread, logical):
    query = '''UPDATE `Thread`
               SET `isDeleted` = %s
               WHERE `id` = %s;
            ''' % (logical, thread)
    cursor.execute(query)

    query = '''UPDATE `Post`
               SET `isDeleted` = %s
               WHERE `thread` = %s;
            ''' % (logical, thread)
    cursor.execute(query)


def set_thread_message_slug(cursor, thread, message, slug):
    query = '''UPDATE `Thread`
               SET `message` = '%s', `slug` = '%s'
               WHERE `id` = %s;
            ''' % (message, slug, thread)

    cursor.execute(query)


def set_thread_vote(cursor, thread, vote):
    if vote < 0:
        column = 'dislikes'
        points = '- 1'
    else:
        column = 'likes'
        points = '+ 1'

    query = '''UPDATE `Thread`
               SET `%s` = `%s` + 1, `points` = `points` %s
               WHERE `id` = %s;
            ''' % (column, column, points, thread)

    cursor.execute(query)


def set_thread_subscribe(cursor, user, thread):
    query = '''INSERT INTO `Subscribe` (`thread`, `user`)
               VALUES (%s, '%s');
            ''' % (thread, user)
    cursor.execute(query)


def set_thread_unsubscribe(cursor, user, thread):
    query = '''DELETE FROM `Subscribe`
               WHERE `thread` = %s AND `user` = '%s';
            ''' % (thread, user)
    cursor.execute(query)


def get_subscribe_by_id(cursor, subs_id):
    query = '''SELECT *
               FROM `Subscribe`
               WHERE `id` = %s;
            ''' % subs_id
    cursor.execute(query)

    subs = cursor.fetchone()
    if subs is None:
        raise NotFound("Subscribe with the '%s' id is not found" % subs_id)

    return subs