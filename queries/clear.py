__author__ = 'max'


def clear_all(cursor):
    query = '''SET FOREIGN_KEY_CHECKS=0'''
    cursor.execute(query)

    tables = ['User', 'Forum', 'Thread', 'Post', 'Follow', 'Subscribe']
    for table in tables:
        query = '''DELETE %s.* FROM %s;''' % (table, table)  # more perfomance
        # query = '''TRUNCATE TABLE `%s`;''' % table
        cursor.execute(query)

    query = '''SET FOREIGN_KEY_CHECKS=1'''
    cursor.execute(query)
