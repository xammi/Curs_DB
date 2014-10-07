__author__ = 'max'

from mysql.connector.cursor import MySQLCursor


class MySQLCursorDict(MySQLCursor):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None


class NotFound(Exception):
    def __init__(self, msg):
        self.msg = msg


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

