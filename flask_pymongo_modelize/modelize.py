__author__ = 'kj'

from flask.ext.pymongo import PyMongo


class Modelize:
    def __init__(self, pymongo:PyMongo=None):
        if pymongo is not None:
            self.init_pymongo(pymongo)

    def init_pymongo(self, pymongo):
        if not hasattr(pymongo, 'extensions'):
            pymongo.extensions = dict()
            pymongo.extensions['modelize'] = dict()

