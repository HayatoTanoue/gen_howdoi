import re
import unittest
from unittest.mock import patch
from cachelib import NullCache

from howdoi import howdoi
from test_howdoi import _get_result_mock

class LinkoutTestCase(unittest.TestCase):
    def setUp(self):
        self.patcher_get_result = patch.object(howdoi, '_get_result')
        self.mock_get_result = self.patcher_get_result.start()
        self.mock_get_result.side_effect = _get_result_mock
        howdoi.cache = NullCache()
        self.query = 'print hello world in python'

    def tearDown(self):
        self.patcher_get_result.stop()

    def test_linkout_appends_url(self):
        result = howdoi.howdoi(self.query + ' -L')
        self.assertRegex(result, r'http.?://.*questions/\d')

if __name__ == '__main__':
    unittest.main()
