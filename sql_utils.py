__author__ = 'max'

from mysql.connector.cursor import MySQLCursor


class MySQLCursorDict(MySQLCursor):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None


class NotFound(Exception):
    def __init__(self, message):
        self.message = message


def optional(obj, default):
    if obj is None or obj == '':
        return default
    return obj

# queries


def set_forum(cursor, name, short_name, user_id):
    query = '''INSERT INTO `Forum`
               (`name`, `short_name`, `user_id`)
               VALUES ('%s', '%s', %d);''' % (name, short_name, user_id)
    cursor.execute(query)


def get_user_by_id(cursor, user_id):
    query = '''SELECT `id`, `username`, `about`, `name`, `email`, `isAnonymous`
               FROM `User`
               WHERE `id` = %d
               LIMIT 1;''' % user_id
    cursor.execute(query)

    user = cursor.fetchone()
    if user is None:
        raise NotFound("User with the '%d' id is not found" % user_id)

    return user


def get_user_by_email(cursor, email):
    email = optional(email, 'no_name@no_host.com')

    query = '''SELECT `id` FROM `User` WHERE `email` = '%s';''' % email
    cursor.execute(query)

    user = cursor.fetchone()
    if user is None:
        raise NotFound("User with the '%s' email is not found" % email)

    return user


def get_forum_by_shortname(cursor, short_name):
    short_name = optional(short_name, 'no_name')

    query = '''SELECT `id`, `name`, `short_name`, `user_id`
               FROM `Forum`
               WHERE `short_name` = '%s'
               LIMIT 1;''' % short_name
    cursor.execute(query)

    forum = cursor.fetchone()
    if forum is None:
        raise NotFound("Forum with the '%s' short_name is not found" % short_name)

    return forum


def get_forum_posts(cursor, forum_id, since, limit, sort, order):
    since = optional(since, '2000-01-01')
    order = optional(order, 'DESC')
    limit = optional(limit, '')

    if limit != '':
        limit = 'LIMIT ' + limit

    query = '''SELECT `id`, `date`, `message`, `parent`, `user`,
                      `isApproved`, `isDeleted`,`isEdited`, `isHighlighted`, `isSpam`
               FROM `Post`
               WHERE `forum` = '%d' AND `date` > '%s'
               ORDER BY `date` %s
               %s;''' % (forum_id, since, order, limit)

    cursor.execute(query)
    return cursor.fetchall()


def get_forum_threads(cursor, forum_id, since, limit, order):
    since = optional(since, '2000-01-01')
    order = optional(order, 'DESC')
    limit = optional(limit, '')

    if limit != '':
        limit = 'LIMIT ' + limit

    query = '''SELECT `id`, `date`, `message`, `user`
               FROM `Thread`
               WHERE `forum` = '%d' AND `date` > '%s'
               ORDER BY `date` %s
               %s;''' % (forum_id, since, order, limit)

    cursor.execute(query)
    return cursor.fetchall()

#--------------------------------------------------------------------------------------------------


def get_post_by_id(cursor, post_id):
    query = '''SELECT `date`, `dislikes`, `forum`, `id`,
                      `isApproved`, `isDeleted`, `isEdited`, `isHighlighted`, `isSpam`,
                      `likes`, `message`, `parent`, `points`, `thread`, `user`
               FROM `Post`
               WHERE `id` = %d
               LIMIT 1;''' % post_id
    cursor.execute(query)

    post = cursor.fetchone()
    if post is None:
        raise NotFound("Post with the '%d' id is not found" % post_id)

    return post


def set_post_deleted(cursor, post, logical):
    query = '''UPDATE `Post`
               SET `isDeleted` = %s
               WHERE `id` = %d;''' % (logical, post)

    cursor.execute(query)


def set_post_message(cursor, post, message):
    query = '''UPDATE `Post`
               SET `message` = %s
               WHERE `id` = %d;''' % (message, post)

    cursor.execute(query)


def set_post_vote(cursor, post, vote):
    if vote < 0:
        column = 'dislikes'
    else:
        column = 'likes'

    query = '''UPDATE `Post`
               SET `%s` = `%s` + 1
               WHERE `id` = %d;''' % (column, column, post)

    cursor.execute(query)

#--------------------------------------------------------------------------------------------------

#--------------------------------------------------------------------------------------------------


def get_thread_by_id(cursor, thread_id):
    query = '''SELECT `date`, `dislikes`, `forum`, `id`,
                      `isClosed`, `isDeleted`, `likes`, `message`,
                      `points`, `posts`, `slug`, `title`, `user`
               FROM `Thread`
               WHERE `id` = %d
               LIMIT 1;''' % thread_id
    cursor.execute(query)

    thread = cursor.fetchone()
    if thread is None:
        raise NotFound("Thread with the '%d' id is not found" % thread_id)

    return thread


def set_thread_closed(cursor, thread, logical):
    query = '''UPDATE `Thread`
               SET `isClosed` = %s
               WHERE `id` = %d;''' % (logical, thread)

    cursor.execute(query)


def set_thread_deleted(cursor, thread, logical):
    query = '''UPDATE `Thread`
               SET `isDeleted` = %s
               WHERE `id` = %d;''' % (logical, thread)

    cursor.execute(query)


def set_thread_message_slug(cursor, thread, message, slug):
    query = '''UPDATE `Thread`
               SET `message` = %s, `slug` = %s
               WHERE `id` = %d;''' % (message, slug, thread)

    cursor.execute(query)


def set_thread_vote(cursor, thread, vote):
    if vote < 0:
        column = 'dislikes'
    else:
        column = 'likes'

    query = '''UPDATE `Thread`
               SET `%s` = `%s` + 1
               WHERE `id` = %d;''' % (column, column, thread)

    cursor.execute(query)

