import os
import unittest
from unittest.mock import patch

from cachelib import NullCache

from howdoi import howdoi
from test_howdoi import _get_result_mock


class MultiSourceTestCase(unittest.TestCase):
    def setUp(self):
        self.patcher_get_result = patch.object(howdoi, '_get_result')
        self.mock_get_result = self.patcher_get_result.start()
        self.mock_get_result.side_effect = _get_result_mock
        howdoi.cache = NullCache()

    def tearDown(self):
        self.patcher_get_result.stop()
        if 'HOWDOI_URL' in os.environ:
            del os.environ['HOWDOI_URL']

    def test_multi_answers(self):
        output = howdoi.howdoi('restart apache')
        self.assertIn('[Stack Overflow]', output)
        self.assertIn('[Server Fault]', output)

    def test_url_override(self):
        os.environ['HOWDOI_URL'] = 'stackoverflow.com'
        output = howdoi.howdoi('restart apache')
        self.assertIn('[Stack Overflow]', output)
        self.assertNotIn('[Server Fault]', output)


if __name__ == '__main__':
    unittest.main()
