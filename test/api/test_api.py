import context
from data.reviewer_model import *
import unittest
import requests
from src.node.settings import constants
import src.node.settings.errors as ERR

class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_URL = constants.core_server_url

    def test_list_organizations(self):
        req = requests.get(self.api_URL + "/organizations")
        self.assertEqual(200, req.status_code)
        resp = req.json()
        self.assertEqual(resp["result"], ERR.OK)
        # TODO заменить на аггрегацию
        found_mpei = False
        for item in resp['list']:
            if item['name'] == 'МЭИ':
                found_mpei = True
        self.assertTrue(found_mpei)

if __name__ == "__main__":
    unittest.main(verbosity = 1)

