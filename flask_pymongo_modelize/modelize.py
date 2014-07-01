__author__ = 'kj'

from flask.ext.pymongo import PyMongo
from . import model

class Modelize:
    def __init__(self, pymongo:PyMongo=None):
        if pymongo is not None:
            self.init_pymongo(pymongo)


    def init_pymongo(self, pymongo):
        self.pymongo = pymongo

        class Model(dict, metaclass=model.ModelMeta):
            __initials__ = {}
            __fields__ = []
            __collection_name__ = None
            __pymongo = self.pymongo

            def __init__(self):
                super().__init__()

            def __getattr__(self, item):
                return super().__getitem__(item)

            def __setattr__(self, key, value):
                super().__setitem__(key, value)

            def __delattr__(self, item):
                super().__delitem__(item)

            def __missing__(self, key):
                return self.__dict__[key] if key in self.__dict__ else None

            query = model.Query(self.pymongo)

        self._Model = Model


    @property
    def Model(self):
        return self._Model