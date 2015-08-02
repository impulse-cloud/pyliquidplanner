try:
    # Try importing from unittest2 first. This is primarily for Py2.6 support.
    import unittest2 as unittest
except ImportError:
    import unittest


import datetime
import json
from mock import patch, Mock, ANY

from liquidplanner import LiquidPlanner
from liquidplanner.exceptions import *
from liquidplanner.manager import Manager
from liquidplanner.utils import UTC


def create_client_manager():
    config = Mock(
        workspace_id=1,
        credentials=Mock(auth=None))

    return Manager(config, 'clients', '/workspaces/{workspace_id}/clients')


def create_success_response(status_code, body):
    def return_body():
       return body

    return Mock(
        status_code=status_code,
        headers={'content-type': 'application/json'},
        text=json.dumps(body),
        json=return_body
    )


def create_error_response(status_code, title, message):
    return Mock(
        status_code=status_code,
        headers={'content-type': 'application/json'},
        text="""{{
            "message": "{0}",
            "error": "{1}",
            "type": "Error"
        }}""".format(message, title)
    )


class ManagerTest(unittest.TestCase):
    @patch('requests.get')
    def test_bad_request(self, r_get):
        "Check that 400 responses are handled correctly"
        r_get.return_value = create_error_response(400, "BadRequest", "Bad Request")
        manager = create_client_manager()

        # Trigger a 'get' request
        with self.assertRaises(LiquidPlannerBadRequest):
            manager.all()

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_unauthorized(self, r_get):
        "Check that 401 responses are handled correctly"
        r_get.return_value = create_error_response(401, "Unauthorized", "Not authorized")
        manager = create_client_manager()

        # Trigger a 'get' request
        with self.assertRaises(LiquidPlannerUnauthorized):
            manager.all()

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_unprocessable(self, r_get):
        "Check that 422 responses are handled correctly"
        r_get.return_value = create_error_response(422, 
            "UnprocessableEntity", "That entity can't be processed")
        manager = create_client_manager()

        # Trigger a 'get' request
        with self.assertRaises(LiquidPlannerUnprocessableEntity):
            manager.all()

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_not_found(self, r_get):
        "Check that 404 responses are handled correctly"
        r_get.return_value = create_error_response(404, 
            "NotFound", "Cannot be found")
        manager = create_client_manager()

        # Trigger a 'get' request
        with self.assertRaises(LiquidPlannerNotFound):
            manager.all()

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_internal_error(self, r_get):
        "Check that 500 responses are handled correctly"
        r_get.return_value = create_error_response(500, 
            "InternalError", "Internal Server Error")
        manager = create_client_manager()

        # Trigger a 'get' request
        with self.assertRaises(LiquidPlannerInternalError):
            manager.all()

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_not_implemented(self, r_get):
        "Check that 501 responses are handled correctly"
        r_get.return_value = create_error_response(501, 
            "NotImplemented", "Action is not implemented")
        manager = create_client_manager()

        # Trigger a 'get' request
        with self.assertRaises(LiquidPlannerNotImplemented):
            manager.all()

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_unavailable(self, r_get):
        "Check that 503 responses are handled correctly"
        r_get.return_value = create_error_response(503, 
            "ServiceUnavailable", "Service is not available")
        manager = create_client_manager()

        # Trigger a 'get' request
        with self.assertRaises(LiquidPlannerUnavailable):
            manager.all()

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_strange_response_code(self, r_get):
        "Check that unexpected response codes are handled correctly"
        r_get.return_value = create_error_response(299, 
            "NoBananas", "Yes, we have no bananas")
        manager = create_client_manager()

        # Trigger a 'get' request
        with self.assertRaises(LiquidPlannerException):
            manager.all()

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_all(self, r_get):
        "Check that all() runs ok"
        expected_output = [{"id": 1}, {"id": 2}] 
        r_get.return_value = create_success_response(200, expected_output) 
        manager = create_client_manager()

        # Trigger a 'get' request
        results = manager.all()

        self.assertTrue(r_get.called)
        self.assertTrue(len(results) == len(expected_output))
        self.assertTrue(results[0]["id"] == expected_output[0]["id"])

    @patch('requests.get')
    def test_get(self, r_get):
        "Check that get() runs ok"
        expected_output = {"id": 1, "name": "Trevor"}
        r_get.return_value = create_success_response(200, expected_output) 
        manager = create_client_manager()

        result = manager.get(1)

        self.assertTrue(r_get.called)
        self.assertTrue(result["name"] == expected_output["name"])

    @patch('requests.post')
    def test_create(self, r_post):
        "Check that create() runs ok"
        expected_output = {"id": 1, "name": "Trevor"}
        expected_post = {"client": {"name": "Trevor"}}
        r_post.return_value = create_success_response(201, expected_output) 
        manager = create_client_manager()

        result = manager.create({"name": "Trevor"})

        self.assertTrue(r_post.called)
        r_post.assert_called_with(ANY, data=json.dumps(expected_post),
                auth=ANY, headers=ANY, timeout=ANY, params=ANY)

    @patch('requests.put')
    def test_update(self, r_put):
        "Check that update() runs ok"
        expected_output = {"id": 1, "name": "Trevor"}
        expected_put = {"client": {"name": "Trevor"}}
        r_put.return_value = create_success_response(200, expected_output) 
        manager = create_client_manager()

        # id as a parameter
        r_put.return_value = create_success_response(200, expected_output) 
        result = manager.update(1, {"name": "Trevor"})

        self.assertTrue(r_put.called)
        r_put.assert_called_with(ANY, data=json.dumps(expected_put),
                auth=ANY, headers=ANY, timeout=ANY, params=ANY)

    @patch('requests.put')
    def test_date_encoding(self, r_put):
        """Check that dates are JSON encoded correctly"""
        obj = {"date": datetime.datetime(2015, 5, 2, 10, 0, 0, 0, tzinfo=UTC())}
        expected_data = '{"client": {"date": "2015-05-02T10:00:00+00:00"}}'
        manager = create_client_manager()

        r_put.return_value = create_success_response(200, {})
        manager.update(1, obj)
        
        r_put.assert_called_with(ANY, data=expected_data,
                auth=ANY, headers=ANY, timeout=ANY, params=ANY)

    @patch('requests.delete')
    def test_delete(self, r_delete):
        "Check that delete() runs ok"
        expected_output = {}
        r_delete.return_value = create_success_response(200, expected_output) 
        manager = create_client_manager()

        # id should be stripped from the object
        result = manager.delete(1)

        self.assertTrue(r_delete.called)
        r_delete.assert_called_with(ANY, data=None,
                auth=ANY, headers=ANY, timeout=ANY, params=None)

    def test_singular(self):
        "Make sure object singular names are determined correctly"

        credentials = Mock(auth=None)

        self.assertEqual(Manager({}, 'projects', '/').singular, "project")

        self.assertEqual(Manager({}, 'accounts', '/').singular, "account")

        self.assertEqual(Manager({}, 'custom_fields', '/').singular, "custom_field")

        self.assertEqual(Manager({}, 'activities', '/').singular, "activity")

