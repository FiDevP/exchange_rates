import os


class Config(object):
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    DEBUG = True