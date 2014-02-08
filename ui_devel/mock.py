import json
import random

from logging import getLogger

logger = getLogger(__name__)

class UIMock(object):
    def __init__(self, name__, *args, **kwargs):
        self.name__ = name__
        self.myattrs__ = set()
        self.value__ = kwargs.pop('value__', 'UIMock: %s' % self.name__)
        self.id = kwargs.pop('id', random.randint(100,10000))
        self.pk = kwargs.pop('pk', self.id)

        self.do_not_call_in_templates = kwargs.pop('do_not_call_in_templates',
                                               True)
        self.alters_data = kwargs.pop('alters_data', False)

        # make all kwargs attributes of this object
        for name,value in kwargs.items():
            self.__setattr__(name, value)
            self.myattrs__.add(name)

    def __getattr__(self, name):
        # undefined attribute being accessed
        val = UIMock('%s.%s' % (self.name__, name))
        logger.debug(val)
        return val

    def __repr__(self):
        val = self.value__
        return val

    def __unicode__(self):
        return unicode(self.value__)

    def __call__(self):
        val = 'UIMock: %s()' % self.name__
        logger.debug(val)
        return val

    def copy(self, Cls=None):
        if not Cls:
            Cls = UIMock
        return Cls(self.name__, self.__dict__)

# Some predefined instances

class User(UIMock):
    def __init__(self, **kwargs):
        self.is_staff = kwargs.pop('is_staff', False)
        self.full_name = kwargs.pop('full_name', 'Unnamed Person')
        kwargs['value__'] = self.full_name
        super(User, self).__init__('User', **kwargs)
    def get_full_name(self):
        return self.full_name

class UIMockEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UIMock):
            return self._handle_mockobj(obj)
        else:
            return json.JSONEncoder.default(self, obj)

    def _handle_mockobj(self, obj):
        repr_dict = {}
        for name in obj.myattrs__:
            child = getattr(obj, name)
            if isinstance(child, UIMock):
                repr_dict[name] = self._handle_mockobj(child)
            elif callable(child):
                # ignore function/lambda assigned to attribute
                continue
            else:
                encoded = json.JSONEncoder.encode(self, child)
                if isinstance(child, basestring):
                    # remove the '"' added by encode at the start and end
                    encoded = encoded[1:-1]
                    # escape any ' chars as the string will be enclosed in ''
                    encoded = encoded.replace("'", "&apos;")
                repr_dict[name] = encoded
        return repr_dict