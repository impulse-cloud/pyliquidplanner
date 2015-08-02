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
        self.config = {}


class ModelTest(unittest.TestCase):
    def test_date_conversion(self):
        "Check that string dates are converted into python dates"
        data = {
                "some_date": "not a date",
                "other_date": u"2015-01-01T09:10:20+00:00",
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

    def test_delete_assignment(self):
        """Check that delete_assignment() runs without error"""
        data = {}
        
        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.delete_assignment(2)

        manager._make_request.assert_called_with('delete', '/uri/1/assignments/2')

    def test_move_before(self):
        """Check that move_before() runs without error"""
        data = {}
        
        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.move_before(2)

        manager._make_request.assert_called_with('post', '/uri/1/move_before',
                params={'other_id': 2})

    def test_move_after(self):
        """Check that move_after() runs without error"""
        data = {}
        
        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.move_after(2)

        manager._make_request.assert_called_with('post', '/uri/1/move_after',
                params={'other_id': 2})

    def test_package_before(self):
        """Check that package_before() runs without error"""
        data = {}
        
        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.package_before(2)

        manager._make_request.assert_called_with('post', '/uri/1/package_before',
                params={'other_id': 2})

    def test_package_after(self):
        """Check that package_after() runs without error"""
        data = {}
        
        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.package_after(2)

        manager._make_request.assert_called_with('post', '/uri/1/package_after',
                params={'other_id': 2})

    def test_thumbnail(self):
        """Check that thumbnail() runs without error"""
        data = {}
        
        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.thumbnail()

        manager._make_request.assert_called_with('get', '/uri/1/thumbnail')

    def test_download(self):
        """Check that downlod() runs without error"""
        data = {}
        
        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.download()

        manager._make_request.assert_called_with('get', '/uri/1/download')

    def test_track_time(self):
        "Check that track_time() runs without error"
        data = {}
        obj = {"work": 4, "low": "1.5d", "high": "3d"}

        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.track_time(obj)

        manager._make_request.assert_called_with('post', '/uri/1/track_time', data=obj)

    def test_timer_commit(self):
        "Check that timer_commit() runs without error"
        data = {}
        obj = {"activity_id": 4, "low": "1.5d", "high": "3d"}

        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.timer_commit(obj)

        manager._make_request.assert_called_with('post', '/uri/1/timer/commit', data=obj)

    def test_timer_start(self):
        """Check that timer_start() runs without error"""
        data = {}
        
        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.timer_start()

        manager._make_request.assert_called_with('post', '/uri/1/timer/start')

    def test_timer_stop(self):
        """Check that timer_stop() runs without error"""
        data = {}
        
        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.timer_stop()

        manager._make_request.assert_called_with('post', '/uri/1/timer/stop')

    def test_timer_clear(self):
        """Check that timer_clear() runs without error"""
        data = {}
        
        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.timer_clear()

        manager._make_request.assert_called_with('post', '/uri/1/timer/clear')

    def test_comment_stream(self):
        """Check that comment_stream() runs without error"""
        data = {}
        params = {"limit": 5}
        
        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.comment_stream(params)

        manager._make_request.assert_called_with('get', '/uri/1/comment_stream',
                params=params)

    def test_upcoming_tasks(self):
        """Check that upcoming_tasks() runs without error"""
        data = {}
        params = {"limit": 5}
        
        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.upcoming_tasks(params)

        manager._make_request.assert_called_with('get', '/uri/1/upcoming_tasks',
                params=params)

    def test_changes(self):
        """Check that changes() runs without error"""
        data = {}
        params = {"limit": 5}
        
        manager = MockManager()
        model = Model(manager, data, "/uri/1")
        model.changes(params)

        manager._make_request.assert_called_with('get', '/uri/1/changes',
                params=params)

    def test_related_managers(self):
        """Check that related managers are created on demand"""
        data = {}
        manager = MockManager()
        model = Model(manager, data, "/uri/1")

        # If an exception is thrown, it will make the test fail
        model.activities
        model.comments
        model.dependencies
        model.dependents
        model.documents
        model.estimates
        model.links
        model.note
        model.snapshots
        model.tags
        model.timer
