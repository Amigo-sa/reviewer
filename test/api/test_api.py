import context
import unittest
import requests
from node.settings import constants
import node.settings.errors as ERR


class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Загрузка адреса сервера
        cls.api_URL = constants.core_server_url
        # Получение часто используемых и не предусматривающих изменение при тестировании _id
        resp = requests.get(cls.api_URL + '/organizations').json()
        cls.mpei_id = cls.find_by_name(resp, 'МЭИ')
        cls.assertTrue(unittest.TestCase(),cls.mpei_id)

    # TODO Возможно, с учётом поиска объектов при инициализации, этот и схожие тесты лишние
    def test_list_organizations(self):
        req = requests.get(self.api_URL + '/organizations')
        self.assertEqual(200, req.status_code)
        resp = req.json()
        self.assertEqual(resp["result"], ERR.OK)
        self.assertTrue(self.find_by_name(resp, 'МЭИ'))

    def test_add_del_organization_normal(self):
        resp = requests.get(self.api_URL + "/organizations").json()
        self.assertEqual(resp["result"], ERR.OK)

        mephi_id = self.find_by_name(resp, 'МИФИ')
        if mephi_id:
            resp = requests.delete(self.api_URL + '/organizations/' + str(mephi_id)).json()
            self.assertEqual(resp['result'], ERR.OK)

        post_data = {'name': 'МИФИ'}
        req = requests.post(url=self.api_URL + '/organizations', json=post_data)
        self.assertEqual(200, req.status_code)
        resp = req.json()
        self.assertEqual(resp['result'], ERR.OK)

        resp = requests.get(self.api_URL + '/organizations').json()
        mephi_id = self.find_by_name(resp, 'МИФИ')
        self.assertTrue(mephi_id)

        req = requests.delete(self.api_URL + '/organizations/' + str(mephi_id))
        self.assertEqual(200, req.status_code)
        resp = req.json()
        self.assertEqual(resp['result'], ERR.OK)

        resp = requests.get(self.api_URL + '/organizations').json()
        mephi_id = self.find_by_name(resp, 'МИФИ')
        self.assertFalse(mephi_id)

    def test_add_organization_malformed(self):
        post_data = {'noname': 'МИФИ'}
        resp = requests.post(url=self.api_URL + '/organizations', json=post_data).json()
        self.assertEqual(resp['result'], ERR.INPUT)

    def test_add_organization_duplicate(self):
        post_data = {'name': 'МЭИ'}
        resp = requests.post(url=self.api_URL + '/organizations', json=post_data).json()
        self.assertEqual(resp['result'], ERR.DB)

    def test_add_organization_no_data(self):
        post_data = {'name': 'МИФИ'}
        resp = requests.post(url=self.api_URL + '/organizations', json=post_data).json()
        self.assertEqual(resp['result'], ERR.OK)
        mephi_id = resp['id']
        resp = requests.delete(self.api_URL + '/organizations/' + str(mephi_id)).json()
        self.assertEqual(resp['result'], ERR.OK)
        resp = requests.delete(self.api_URL + '/organizations/' + str(mephi_id)).json()
        self.assertEqual(resp['result'], ERR.NO_DATA)

    def test_list_departments(self):
        req = requests.get(self.api_URL + '/organizations/' + self.mpei_id + '/departments')
        self.assertEqual(200, req.status_code)
        resp = req.json()
        self.assertEqual(resp['result'], ERR.OK)
        self.assertTrue(self.find_by_name(resp, 'Кафедра ИИТ'))

    def test_add_del_department_normal(self):
        resp = requests.get(self.api_URL + '/organizations/' + self.mpei_id + '/departments').json()
        self.assertEqual(resp["result"], ERR.OK)

        rtf_id = self.find_by_name(resp, 'РТФ')
        if rtf_id:
            resp = requests.delete(self.api_URL + '/departments/' + str(rtf_id)).json()
            self.assertEqual(resp['result'], ERR.OK)

        post_data = {'name': 'РТФ'}
        req = requests.post(url=self.api_URL + '/organizations/' + self.mpei_id + '/departments', json=post_data)
        self.assertEqual(200, req.status_code)
        resp = req.json()
        self.assertEqual(resp['result'], ERR.OK)

        resp = requests.get(self.api_URL + '/organizations/' + self.mpei_id + '/departments').json()
        rtf_id = self.find_by_name(resp, 'РТФ')
        self.assertTrue(rtf_id)

        req = requests.delete(self.api_URL + '/departments/' + str(rtf_id))
        self.assertEqual(200, req.status_code)
        resp = req.json()
        self.assertEqual(resp['result'], ERR.OK)

        resp = requests.get(self.api_URL + '/organizations/' + self.mpei_id + '/departments').json()
        rtf_id = self.find_by_name(resp, 'РТФ')
        self.assertFalse(rtf_id)

    def test_add_department_malformed(self):
        post_data = {'noname': 'РТФ'}
        resp = requests.post(url=self.api_URL + '/organizations/' + self.mpei_id + '/departments', json=post_data).json()
        self.assertEqual(resp['result'], ERR.INPUT)

    def test_add_department_wrong_org(self):
        resp = requests.get(self.api_URL + "/organizations").json()
        mephi_id = self.find_by_name(resp, 'МИФИ')
        if not mephi_id:
            post_data = {'name': 'МИФИ'}
            resp = requests.post(url=self.api_URL + '/organizations', json=post_data).json()
            self.assertEqual(resp['result'], ERR.OK)
            mephi_id = resp['id']
            print("added mephi " + str(mephi_id))
        resp = requests.delete(self.api_URL + '/organizations/' + str(mephi_id)).json()
        self.assertEqual(resp['result'], ERR.OK)
        post_data = {'name': 'РТФ'}
        resp = requests.post(url=self.api_URL + '/organizations/' + mephi_id + '/departments', json=post_data).json()
        self.assertEqual(resp['result'],ERR.DB)


    @staticmethod
    def find_by_name(resp, name):
        for item in resp['list']:
            if item['name'] == name:
                return item['id']

if __name__ == "__main__":
    unittest.main(verbosity=1)
