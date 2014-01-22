import django
from django.conf import settings
from django.utils import unittest

import ui_devel.mock

class UIMockTestCase(django.test.TestCase):
    def test_undefined_access(self):
        obj = ui_devel.mock.UIMock('Name')
        self.assertTrue('Name.test' in obj.test)

    def test_defined_access(self):
        obj = ui_devel.mock.UIMock('Name', test='defined_value',
                                      child=ui_devel.mock.UIMock('Child', a='a', grandchild=ui_devel.mock.UIMock('GrandChild')))
        self.assertEqual(obj.test, 'defined_value')
        print obj