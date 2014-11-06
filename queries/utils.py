__author__ = 'max'


def optional(obj, default):
    if obj is None or obj == '':
        return default
    return obj


class NotFound(Exception):
    def __init__(self, message):
        self.msg = message


class WrongType(Exception):
    def __init__(self, param, right_type):
        self.msg = 'Parameter (%s) must be of %s type' % (param, right_type)


class WrongValue(Exception):
    def __init__(self, param, value):
        self.msg = 'Parameter (%s) has wrong value: %s' % (param, value)


def check_order(string, default):
    string = optional(string, default)
    string = string.upper()

    if string not in ['ASC', 'DESC']:
        raise WrongValue('order', string)
    return string


def check_sort(string, default):
    string = optional(string, default)
    string = string.lower()

    if string not in ['flat', 'tree', 'parent_tree']:
        raise WrongValue('sort', string)
    return string


def check_limit(limit):
    limit = optional(limit, '')
    if limit == '':
        return ''

    num = to_number(limit, 'limit')
    return 'LIMIT %d' % num


def to_number(string, param):
    string = optional(string, '0')
    try:
        return int(string)
    except ValueError:
        raise WrongType(param, 'integer')


def to_bool(string, param):
    string = optional(string, 'false')
    try:
        return bool(string)
    except ValueError:
        raise WrongType(param, 'bool')


def prepare_thread(thread):
    thread['date'] = thread['date'].strftime("%Y-%m-%d %H:%M:%S")


def prepare_post(post):
    post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")


def prepare_user(user):
    return user


def hierarchy_sort(sort):
    sort = check_sort(sort, 'flat')
    stmt = ''

    if sort is None or sort == 'flat':
        stmt = ''
    elif sort == 'tree':
        stmt = ', `parent` ASC'
    elif sort == 'parent_tree':
        stmt = ', `parent` ASC'

    return stmt
