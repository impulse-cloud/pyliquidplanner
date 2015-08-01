try:
    # Try importing from unittest2 first. This is primarily for Py2.6 support.
    import unittest2 as unittest
except ImportError:
    import unittest


import json
from mock import patch, Mock, ANY
import datetime

from liquidplanner.models import Model


class MockManager(object):
    def __init__(self):
        self._make_request = Mock()
        self.singular = Mock()


class ModelTest(unittest.TestCase):
    def test_date_conversion(self):
        "Check that string dates are converted into python dates"
        data = {
                "some_date": "not a date",
                "other_date": "2015-01-01T09:10:20+00:00",
                "nested": [{"extra_date": "2015-01-10T00:00:01+00:00"}]}

        manager = MockManager()
        model = Model(manager, data, "/")

        self.assertFalse(isinstance(model["some_date"], datetime.datetime))
        self.assertTrue(isinstance(model["other_date"], datetime.datetime))
        self.assertTrue(isinstance(model["nested"][0]["extra_date"], datetime.datetime))

    def test_update_assignment(self):
        "Check that update_assignment() runs without error"
        data = {}
        obj = {"name": "My Client"}

        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.update_assignment(obj)

        manager._make_request.assert_called_with('post', '/uri/1/update_assignment', data=obj)

    def test_reorder_assignments(self):
        "Check that reorder_assignments() runs without error"
        data = {}
        id_list = [6, 5, 4]

        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.reorder_assignments(id_list)

        manager._make_request.assert_called_with('post', '/uri/1/reorder_assignments',
                data={"assignment_ids": id_list })
