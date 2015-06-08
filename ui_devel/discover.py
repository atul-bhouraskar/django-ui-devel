from django.conf import settings
from importlib import import_module

class InvalidTemplateFixture(Exception):
    pass

# holds all the fixtures
template_fixtures = {}

def get_template_fixtures():
    """
    Return the list of all available template fixtures.

    Caches the result for faster access.

    Code modified from django/template/base.py/get_templatetags_modules()
    """
    global template_fixtures
    if not template_fixtures:
        _template_fixtures = {}
        # Populate list once per process. Mutate the local list first, and
        # then assign it to the global name to ensure there are no cases where
        # two threads try to populate it simultaneously.
        for app_module in list(settings.INSTALLED_APPS):
            try:
                templatefixture_module = '%s.templatefixtures' % app_module
                mod = import_module(templatefixture_module)
                try:
                    fixtures = mod.fixtures
                    # TODO: validate fixtures structure
                    _template_fixtures.update(fixtures)
                except AttributeError:
                    raise InvalidTemplateFixture('Template fixture module %s '
                                                 'does not have a variable'
                                                 'named "fixtures"' %
                                                 templatefixture_module)
                except ValueError:
                    raise InvalidTemplateFixture('%s.fixture should be a '
                                                 'dictionary' %
                                                 templatefixture_module)
            except ImportError as e:
                #print app_module, e
                continue
        template_fixtures = _template_fixtures
    return template_fixtures
