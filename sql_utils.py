__author__ = 'max'

from mysql.connector.cursor import MySQLCursor


class MySQLCursorDict(MySQLCursor):
    def _row_to_python(self, rowdata, desc=None):
        row = super(MySQLCursorDict, self)._row_to_python(rowdata, desc)
        if row:
            return dict(zip(self.column_names, row))
        return None


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
    return cursor.fetchone()


def get_user_by_email(cursor, email):
    query = '''SELECT `id` FROM `User` WHERE `email` = '%s';''' % email
    cursor.execute(query)
    return cursor.fetchone()


def get_forum_by_shortname(cursor, short_name):
    query = '''SELECT `id`, `name`, `short_name`, `user_id`
               FROM `Forum`
               WHERE `short_name` = '%s'
               LIMIT 1;''' % short_name
    cursor.execute(query)
    return cursor.fetchone()


def get_forum_posts(cursor, forum_id):
    query = '''SELECT `id`, `date`, `message`, `parent`,
                      `isApproved`, `isDeleted`,`isEdited`, `isHighlighted`, `isSpam`,
                      `User`.`email`
               FROM `Post`
               JOIN `Forum` ON `forum` = `Forum`.`id`
               JOIN `User` ON `user` = `User`.`id`
               WHERE `forum` = '%d';''' % forum_id
    cursor.execute(query)
    return cursor.fetchall()

