__author__ = 'kj'

__author__ = 'kj'

__all__ = ['IFModel']

from inspect import Parameter, Signature


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


class IFModelMeta(type):
    def __new__(cls, name, bases, clsdict):
        def update_field(node):
            if node:
                if hasattr(node.node, '__fields__'):
                    clsdict['__fields__'][:0] = node.node.__fields__
                    if '__initials__' not in clsdict:
                        clsdict['__initials__'] = {}

                    clsdict['__initials__'].update(node.node.__initials__)
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

        clsobj.__init__ = __init__
        if '__clct_name__' not in clsobj.__dict__:
            setattr(clsobj, '__clct_name__', clsobj.__qualname__)
        return clsobj


class IFModel(dict, metaclass=IFModelMeta):
    __initials__ = {}
    __fields__ = []

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

    class _Query:
        def __get__(self, instance, owner):
            return getattr(mongo.db, owner.__clct_name__)

    query = _Query()
