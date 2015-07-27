try:
    # Try importing from unittest2 first. This is primarily for Py2.6 support.
    import unittest2 as unittest
except ImportError:
    import unittest


import json
from mock import patch, Mock, ANY

from liquidplanner import LiquidPlanner
from liquidplanner.exceptions import *


class MockCredentials(object):
    def __init__(self):
        self.auth = None


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
            "message": "{}",
            "error": "{}",
            "type": "Error"
        }}""".format(message, title)
    )

class ManagerTest(unittest.TestCase):
    @patch('requests.get')
    def test_bad_request(self, r_get):
        "Check that 400 responses are handled correctly"
        r_get.return_value = create_error_response(400, "BadRequest", "Bad Request")

        # Will attempt to fetch the workspace list
        with self.assertRaises(LiquidPlannerBadRequest):
            lp = LiquidPlanner(MockCredentials())

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_unauthorized(self, r_get):
        "Check that 401 responses are handled correctly"
        r_get.return_value = create_error_response(401, "Unauthorized", "Not authorized")

        # Will attempt to fetch the workspace list
        with self.assertRaises(LiquidPlannerUnauthorized):
            lp = LiquidPlanner(MockCredentials())

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_unprocessable(self, r_get):
        "Check that 422 responses are handled correctly"
        r_get.return_value = create_error_response(422, 
            "UnprocessableEntity", "That entity can't be processed")

        # Will attempt to fetch the workspace list
        with self.assertRaises(LiquidPlannerUnprocessableEntity):
            lp = LiquidPlanner(MockCredentials())

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_not_found(self, r_get):
        "Check that 404 responses are handled correctly"
        r_get.return_value = create_error_response(404, 
            "NotFound", "Cannot be found")

        # Will attempt to fetch the workspace list
        with self.assertRaises(LiquidPlannerNotFound):
            lp = LiquidPlanner(MockCredentials())

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_internal_error(self, r_get):
        "Check that 500 responses are handled correctly"
        r_get.return_value = create_error_response(500, 
            "InternalError", "Internal Server Error")

        # Will attempt to fetch the workspace list
        with self.assertRaises(LiquidPlannerInternalError):
            lp = LiquidPlanner(MockCredentials())

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_not_implemented(self, r_get):
        "Check that 501 responses are handled correctly"
        r_get.return_value = create_error_response(501, 
            "NotImplemented", "Action is not implemented")

        # Will attempt to fetch the workspace list
        with self.assertRaises(LiquidPlannerNotImplemented):
            lp = LiquidPlanner(MockCredentials())

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_unavailable(self, r_get):
        "Check that 503 responses are handled correctly"
        r_get.return_value = create_error_response(503, 
            "ServiceUnavailable", "Service is not available")

        # Will attempt to fetch the workspace list
        with self.assertRaises(LiquidPlannerUnavailable):
            lp = LiquidPlanner(MockCredentials())

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_strange_response_code(self, r_get):
        "Check that unexpected response codes are handled correctly"
        r_get.return_value = create_error_response(299, 
            "NoBananas", "Yes, we have no bananas")

        # Will attempt to fetch the workspace list
        with self.assertRaises(LiquidPlannerException):
            lp = LiquidPlanner(MockCredentials())

        self.assertTrue(r_get.called)

    @patch('requests.get')
    def test_all(self, r_get):
        "Check that use_first_workspace works"

        output = [{"id": 123, "name": "My Workspace"}]
        r_get.return_value = create_success_response(200, expected_output) 

        lp = LiquidPlanner(MockCredentials())

        self.assertTrue(r_get.called)
        self.assertTrue(lp.workspace_id == output[0]["id"])

    @patch('requests.get')
    def test_all(self, r_get):
        "Check that all() runs ok"
        lp = LiquidPlanner(MockCredentials(), use_first_workspace=False)
        lp.workspace_id = 1

        expected_output = [{"id": 1}, {"id": 2}] 
        r_get.return_value = create_success_response(200, expected_output) 

        results = lp.clients.all()

        self.assertTrue(r_get.called)
        self.assertTrue(len(results) == len(expected_output))
        self.assertTrue(results[0]["id"] == expected_output[0]["id"])

    @patch('requests.get')
    def test_get(self, r_get):
        "Check that get() runs ok"
        lp = LiquidPlanner(MockCredentials(), use_first_workspace=False)
        lp.workspace_id = 1

        expected_output = {"id": 1, "name": "Trevor"}
        r_get.return_value = create_success_response(200, expected_output) 

        result = lp.clients.get(1)

        self.assertTrue(r_get.called)
        self.assertTrue(result["name"] == expected_output["name"])

    @patch('requests.post')
    def test_create(self, r_post):
        "Check that get() runs ok"
        lp = LiquidPlanner(MockCredentials(), use_first_workspace=False)
        lp.workspace_id = 1

        expected_output = {"id": 1, "name": "Trevor"}
        expected_post = {"client": {"name": "Trevor"}}
        r_post.return_value = create_success_response(201, expected_output) 

        result = lp.clients.create({"name": "Trevor"})

        self.assertTrue(r_post.called)
        r_post.assert_called_with(ANY, data=json.dumps(expected_post),
                auth=ANY, headers=ANY, timeout=ANY, params=ANY)

    @patch('requests.put')
    def test_update(self, r_put):
        "Check that update() runs ok"
        lp = LiquidPlanner(MockCredentials(), use_first_workspace=False)
        lp.workspace_id = 1

        expected_output = {"id": 1, "name": "Trevor"}
        expected_put = {"client": {"name": "Trevor"}}
        r_put.return_value = create_success_response(200, expected_output) 

        # id should be stripped from the object
        result = lp.clients.update({"id": 1, "name": "Trevor"})

        self.assertTrue(r_put.called)
        r_put.assert_called_with(ANY, data=json.dumps(expected_put),
                auth=ANY, headers=ANY, timeout=ANY, params=ANY)

        # id as a parameter
        r_put.reset_mock()
        r_put.return_value = create_success_response(200, expected_output) 
        result = lp.clients.update({"name": "Trevor"}, 1)

        self.assertTrue(r_put.called)
        r_put.assert_called_with(ANY, data=json.dumps(expected_put),
                auth=ANY, headers=ANY, timeout=ANY, params=ANY)

    def test_singular(self):
        "Make sure object singular names are determined correctly"

        lp = LiquidPlanner(MockCredentials(), use_first_workspace=False)

        self.assertEqual(lp.projects.singular, "project")

        self.assertEqual(lp.account.singular, "account")

        self.assertEqual(lp.custom_fields.singular, "custom_field")

        self.assertEqual(lp.activities.singular, "activity")

