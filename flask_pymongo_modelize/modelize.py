__author__ = 'kj'

from flask.ext.pymongo import PyMongo
from . import model
from enum import IntEnum, unique


@unique
class EntityStatus(IntEnum):
    Unchanged = 0,
    Modified = 1,
    Added = 2,
    Deleted = 3
    Detached = -1


class BaseEntity:
    pass


class BaseModel:
    pass


class BaseChangeTracker:
    pass


class Modelize:
    def __init__(self, pymongo:PyMongo=None):
        self.pymongo = None
        self._Model = None
        self._change_tracker = None
        if pymongo is not None:
            self.init_pymongo(pymongo)


    def init_pymongo(self, pymongo):
        self.pymongo = pymongo
        query = model.Query(self.pymongo)
        self._change_tracker = self.__get_change_tracker_type()()
        self._Model = self.__get_model_type(pymongo, self._change_tracker)

    @staticmethod
    def __get_change_tracker_type():
        class ChangeTracker(BaseChangeTracker):
            def __init__(self):
                self._tracked_objects = {}

            def __check_modeltype(self, type):
                if not isinstance(model, BaseModel):
                    raise TypeError("{!r} is not a valid model type.".format(type(model)))

            def __iadd__(self, entity):
                self.__check_modeltype(entity)
                self._tracked_objects.add(entity)

            def __isub__(self, entity):
                self.__check_modeltype(entity)
                self._tracked_objects.remove(entity)

            # These are for for different calling conventions
            attach = __iadd__
            detach = __isub__

            def get_entity_status(self, entity):
                if entity not in self._tracked_objects:
                    return EntityStatus.Detached

                #if self._tracked_objects[entity]

        return ChangeTracker


    @staticmethod
    def __get_model_type(pymongo:PyMongo, change_tracker:BaseChangeTracker):
        class Model(dict, BaseModel, metaclass=model.ModelMeta):
            __initials__ = {}
            __type_identifier__ = {}
            __fields__ = []
            __collection_name__ = None
            __pymongo = pymongo
            __change_tracker = change_tracker

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

            def __getattr__(self, item):
                return super().__getitem__(item)

            def __setattr__(self, key, value):
                super().__setitem__(key, value)

            def __delattr__(self, item):
                super().__delitem__(item)

            def __missing__(self, key):
                return self.__dict__[key]

            query = model.Query(pymongo)

        return Model

    @property
    def Model(self):
        return self._Model

    @property
    def change_tracker(self):
        return self._change_tracker