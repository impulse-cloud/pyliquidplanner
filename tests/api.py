try:
    # Try importing from unittest2 first. This is primarily for Py2.6 support.
    import unittest2 as unittest
except ImportError:
    import unittest


import json
from mock import patch, Mock, ANY

from liquidplanner import LiquidPlanner


class ApiTest(unittest.TestCase):
    @patch('liquidplanner.api.Manager.all')
    def test_first_workspace(self, mock_all):
        "Check that use_first_workspace works"

        expected_output = [{"id": 123, "name": "My Workspace"}]
        mock_all.return_value = expected_output

        credentials = Mock(auth=None)
        lp = LiquidPlanner(credentials)

        self.assertTrue(mock_all.called)
        self.assertTrue(lp.workspace_id == expected_output[0]["id"])

        mock_all.reset_mock()
        mock_all.return_value = expected_output
        lp = LiquidPlanner(credentials, use_first_workspace=False)

        self.assertFalse(mock_all.called)

