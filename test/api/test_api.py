import context
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
        self.assertTrue(self.find_org(resp,'МЭИ'))

    def test_add_del_organization_normal(self):
        resp = requests.get(self.api_URL + "/organizations").json()
        self.assertEqual(resp["result"], ERR.OK)

        mephi_id = self.find_org(resp, 'МИФИ')
        if mephi_id:
            resp = requests.delete(self.api_URL + "/organizations/" + str(mephi_id)).json()
            self.assertEqual(resp['result'], ERR.OK)

        post_data = {'name' : 'МИФИ'}
        resp = requests.post(url=self.api_URL + '/organizations',json = post_data).json()
        self.assertEqual(resp['result'], ERR.OK)

        resp = requests.get(self.api_URL + '/organizations').json()
        mephi_id = self.find_org(resp, 'МИФИ')
        self.assertTrue(mephi_id)

        resp = requests.delete(self.api_URL + "/organizations/" + str(mephi_id)).json()
        self.assertEqual(resp['result'], ERR.OK)

        resp = requests.get(self.api_URL + '/organizations').json()
        mephi_id = self.find_org(resp, 'МИФИ')
        self.assertFalse(mephi_id)


    @staticmethod
    def find_org(resp, name):
        for item in resp['list']:
            if item['name'] == name:
                return item['id']


if __name__ == "__main__":
    unittest.main(verbosity = 1)

