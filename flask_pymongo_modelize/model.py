__author__ = 'kj'

__all__ = ['Model']

from inspect import Parameter, Signature
from functools import partial
from flask import current_app
from flask.ext.pymongo import PyMongo


__type_identifier__ = '__type_identifier__'
__fields__ = '__fields__'
__collection_name__ = '__collection_name__'


def _make_signature(parameters={}):
    return Signature(
        Parameter(k, Parameter.POSITIONAL_OR_KEYWORD, default=v)
        for k, v in parameters.items()
    )


class Node:
    def __init__(self, node, children=()):
        self.node = node
        self.children = children


def retro(type_, child, nodemap):
    if type_ not in nodemap:
        node = Node(type_, (child,) if child else None)
        nodemap[type_] = node
    else:
        node = nodemap[type_]
        if child:
            node.children += (child,)

    if not type_.__base__:
        return nodemap[type_]

    for base in type_.__bases__:
        res = retro(base, node, nodemap)
    return res


def get_class_hierarchy_root(type_):
    return retro(type_, None, {})


def visualize(node):
    if node is None:
        return

    if node.children:
        print("{}有{}个子类，{}是{}".format(node.node,
                                      len(node.children),
                                      '分别' if len(node.children) > 1 else '',
                                      ', '.join([str(c.node) for c in node.children])))
        for child in node.children:
            visualize(child)
    else:
        print("{}没有子类".format(node.node))


class ModelMeta(type):
    def __new__(cls, name, bases, clsdict, **kwargs):
        if __fields__ not in clsdict:
            clsdict[__fields__] = []
        clsdict.update(kwargs)

        def update_field(node):
            if node:
                if hasattr(node.node, __fields__):
                    clsdict[__fields__][:0] = node.node.__fields__
                    if __type_identifier__ not in clsdict:
                        clsdict[__type_identifier__] = {}

                    clsdict[__type_identifier__].update(node.node.__initials__)
                if node.children:
                    for child in node.children:
                        update_field(child)

        for base in bases:
            clshierroot = get_class_hierarchy_root(base)
            update_field(clshierroot)

        clsobj = super().__new__(cls, name, bases, clsdict)
        fielddict = {k: clsobj.__initials__.get(k, None) for k in clsobj.__fields__}
        signature = _make_signature(fielddict)
        setattr(clsobj, '__signature__', signature)

        def __init__(self, *args, **kwargs):
            args = ()
            for k in set(kwargs.keys()) - set(fielddict.keys()):
                del kwargs[k]

            bound = self.__signature__.bind(*args, **kwargs)
            for param in self.__signature__.parameters.values():
                if param.name not in bound.arguments:
                    bound.arguments[param.name] = param.default
            for name, value in bound.arguments.items():
                setattr(self, name, value)

        @classmethod
        def from_dict(cls, dict_):
            return cls(**dict_)

        clsobj.__init__ = __init__
        clsobj.from_dict = from_dict
        if __collection_name__ not in clsobj.__dict__:
            setattr(clsobj, __collection_name__, clsobj.__qualname__)

        return clsobj


    def __init__(cls, name, bases, clsdict, **kwargs):
        super().__init__(name, bases, clsdict)


class Query:
    def __init__(self, pymongo):
        self.__pymongo = pymongo


    @property
    def __collection(self):
        return getattr(self.__pymongo.db, self.__collection_name)

    def __get__(self, instance, owner):
        self.__modeltype = owner
        self.__collection_name = owner.__collection_name__
        self.__type_identifier = \
            owner.__type_identifier__ \
                if hasattr(owner, '__type_identifier__') \
                else None
        return self

    def __cast_to_modeltype(self, doc_or_docs):
        if isinstance(doc_or_docs, dict):
            return self.__modeltype.from_dict(doc_or_docs)
        else:
            return [self.__modeltype.from_dict(doc) for doc in doc_or_docs]

    def find(self, *args, **kwargs):
        res = self.__collection.find(*args,
                                     kwargs=kwargs,
                                     **self.__type_identifier)

        return self.__cast_to_modeltype(res)


    def find_one(self, spec_or_id=None, *args, **kwargs):
        kwargs = kwargs.copy()
        kwargs.update(self.__type_identifier)
        res = self.__collection.find_one(spec_or_id=spec_or_id,
                                         *args,
                                         **kwargs)

        return self.__cast_to_modeltype(res)

    def insert(self, doc_or_docs, manipulate=True,
               safe=None, check_keys=True, continue_on_error=False, **kwargs):
        if isinstance(doc_or_docs, dict):
            doc_or_docs = [doc_or_docs]

        for item in doc_or_docs:
            item.update(self.__type_identifier)

        return self.__collection.insert(doc_or_docs,
                                        manipulate=manipulate,
                                        safe=safe,
                                        check_keys=check_keys,
                                        continue_on_error=continue_on_error,
                                        **kwargs)
