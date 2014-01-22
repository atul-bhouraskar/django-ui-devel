import django
from django.conf import settings
from django.utils import unittest

import ui_devel.discover

class DiscoveryTestCase(django.test.TestCase):
    def setUp(self):
        if 'test_project.test_ui_devel' not in settings.INSTALLED_APPS:
            self.skipTest('Skipping discovery test')

    def test_get_template_fixtures(self):
        fixtures = ui_devel.discover.get_template_fixtures()
        print fixtures