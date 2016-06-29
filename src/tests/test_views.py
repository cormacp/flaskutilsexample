from flaskutils import app
from flaskutils.test import TransactionalTestCase

import json


class TestAppCase(TransactionalTestCase):
    def test_api_root(self):
        """
        Makes a HTTP GET REQUEST AND API information
        """
        result = self.client.get('/')
        assert 200 == result.status_code
        data = json.loads(result.get_data().decode('utf-8'))
        assert 'version' in data
        assert '1.0' == data['version']
