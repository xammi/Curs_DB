__author__ = 'max'

from flask import current_app


def clear_all(cursor):
    current_app.logger.info('Start clear all')
    query = '''SET FOREIGN_KEY_CHECKS=0'''
    cursor.execute(query)

    tables = ['User', 'Forum', 'Thread', 'Post', 'Follow', 'Subscribe']
    for table in tables:
        query = '''TRUNCATE TABLE `%s`;''' % table
        current_app.logger.info(query)
        cursor.execute(query)

    query = '''SET FOREIGN_KEY_CHECKS=1'''
    current_app.logger.info('End clear all')
    cursor.execute(query)
