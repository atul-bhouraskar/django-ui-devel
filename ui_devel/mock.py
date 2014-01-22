import json

class UIMock(object):
    def __init__(self, name__, *args, **kwargs):
        self.name__ = name__
        # make all kwargs attributes of this object
        for name,value in kwargs.items():
            self.__setattr__(name, value)

    def __getattr__(self, name):
        # undefined attribute being accessed
        return 'UNDEF: %s.%s' % (self.name__, name)

    def __repr__(self):
        repr_dict = self.__dict__.copy()
        del repr_dict['name__']
        return repr(repr_dict)

class UIMockEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UIMock):
            repr_dict = obj.__dict__.copy()
            del repr_dict['name__']
            return repr_dict
        else:
            return json.JSONEncoder.default(self, obj)