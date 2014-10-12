__author__ = 'max'

from mysql.connector.cursor import MySQLCursor


def optional(obj, default):
    if obj is None or obj == '':
        return default
    return obj


class MySQLCursorDict(MySQLCursor):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
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


# queries


def set_forum(cursor, name, slug, user):
    query = '''INSERT INTO `Forum`
               (`name`, `slug`, `founder`)
               VALUES ('%s', '%s', '%s');''' % (name, slug, user)
    cursor.execute(query)


def get_forum_by_slug(cursor, slug):
    slug = optional(slug, 'no_name')

    query = '''SELECT `id`, `name`, `slug`, `founder`
               FROM `Forum`
               WHERE `slug` = '%s'
               LIMIT 1;''' % slug
    cursor.execute(query)

    forum = cursor.fetchone()
    if forum is None:
        raise NotFound("Forum with the '%s' short_name is not found" % slug)

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
                      `likes`, `message`, `parent`, `thread`, `author`
               FROM `Post`
               WHERE `id` = %d
               LIMIT 1;''' % post_id
    cursor.execute(query)

    post = cursor.fetchone()
    if post is None:
        raise NotFound("Post with the '%d' id is not found" % post_id)

    return post


def set_post(cursor, date, thread, message, user, forum):
    query = '''INSERT INTO `Post` (`date`, `thread`, `message`, `author`, `forum`)
               VALUES ('%s', %d, '%s', '%s', '%s');''' % (date, thread, message, user, forum)
    cursor.execute(query)


def set_post_opt(cursor, post_id, parent, is_approved, is_highlighted, is_edited, is_spam, is_deleted):
    parent = optional(parent, 'NULL')
    is_approved = optional(is_approved, 'false')
    is_highlighted = optional(is_highlighted, 'false')
    is_edited = optional(is_edited, 'false')
    is_spam = optional(is_spam, 'false')
    is_deleted = optional(is_deleted, 'false')

    query = '''UPDATE `Post`
               SET `parent` = %s, `isApproved` = %s, `isHighlighted` = %s,
                   `isEdited` = %s, `isSpam` = %s, `isDeleted` = %s
               WHERE `id` = %d;''' % (parent, is_approved, is_highlighted, is_edited,
                                      is_spam, is_deleted, post_id)
    cursor.execute(query)


def set_post_deleted(cursor, post, logical):
    query = '''UPDATE `Post`
               SET `isDeleted` = %s
               WHERE `id` = %d;''' % (logical, post)

    cursor.execute(query)


def set_post_message(cursor, post, message):
    query = '''UPDATE `Post`
               SET `message` = '%s'
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


def set_user(cursor, username, about, name, email, is_anonymous):
    is_anonymous = optional(is_anonymous, 'false')

    query = '''INSERT INTO `User` (`username`, `about`, `email`, `name`, `isAnonymous`)
               VALUES ('%s', '%s', '%s', '%s', %s);''' \
            % (username, about, email, name, is_anonymous)

    cursor.execute(query)


def get_user_by_email(cursor, email):
    query = '''SELECT `id`, `username`, `about`, `name`, `email`
               FROM `User`
               WHERE `email` = '%s';''' % email
    cursor.execute(query)

    user = cursor.fetchone()
    if user is None:
        raise NotFound("User with the '%s' email is not found" % email)

    return user

#--------------------------------------------------------------------------------------------------


def get_thread_by_id(cursor, thread_id):
    query = '''SELECT `date`, `dislikes`, `forum`, `id`,
                      `isClosed`, `isDeleted`, `likes`, `message`,
                      `slug`, `title`, `author`
               FROM `Thread`
               WHERE `id` = %d
               LIMIT 1;''' % thread_id
    cursor.execute(query)

    thread = cursor.fetchone()
    if thread is None:
        raise NotFound("Thread with the '%d' id is not found" % thread_id)

    return thread


def set_thread(cursor, forum, title, is_closed, user, date, message, slug, is_deleted):
    is_deleted = optional(is_deleted, 'false')

    query = '''INSERT INTO `Thread` (`forum`, `title`, `isClosed`, `author`,
                                     `date`, `message`, `slug`, `isDeleted`)
               VALUES ('%s', '%s', %s, '%s', '%s', '%s', '%s', %s);''' \
            % (forum, title, is_closed, user, date, message, slug, is_deleted)

    cursor.execute(query)


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
               SET `message` = '%s', `slug` = '%s'
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

