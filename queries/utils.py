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


def number(string, param):
    string = optional(string, '0')
    try:
        return int(string)
    except ValueError:
        raise WrongType(param, 'integer')


def logic(string, param):
    string = optional(string, 'false')
    try:
        return bool(string)
    except ValueError:
        raise WrongType(param, 'bool')


def none(obj):
    if obj == 'None' or obj == 0:
        return None
    return obj


def prepare_thread(thread):
    thread['date'] = thread['date'].strftime("%Y-%m-%d %H:%M:%S")


def prepare_post(post):
    post['date'] = post['date'].strftime("%Y-%m-%d %H:%M:%S")


def prepare_user(my_user):
    pass


def hierarchy_sort(sort):
    if sort is None or sort == 'flat':
        sort = ''
    elif sort == 'tree':
        sort = ', `parent` ASC'
    elif sort == 'parent_tree':
        sort = ', `parent` ASC'

    return sort
