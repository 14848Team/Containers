import requests, unittest, json
from MySupport import MySupport

class ConfigTests(unittest.TestCase):
    HOSTNAME = "host"
    PORT = 80

    def suite():
        suite = unittest.TestSuite()
        suite.addTest(ConfigTests('test_invalid'))
        suite.addTest(ConfigTests('test_config'))

        return suite

    def test_invalid(self):
        url =  MySupport.url(self.HOSTNAME, self.PORT, "/config")

        # create - not JSON
        response = requests.post(url, data="omgwtfbbq")
        self.assertEqual(response.status_code, 409)
        self.assertFalse(response.content)

        # missing major version
        response = requests.post(url, json=MySupport.get_dict("invalid"))
        self.assertEqual(response.status_code, 409)
        self.assertFalse(response.content)

    def test_config(self):
        url =  MySupport.url(self.HOSTNAME, self.PORT, "/config")
        url_info=  MySupport.url(self.HOSTNAME, self.PORT, "/cfginfo")

        expected = {
             "files": []
        }

        # get cfg info - empty
        response = requests.get(url_info)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)

        json = response.json()
        self.assertEqual(json, expected)

        # create - success
        response = requests.post(url, json=MySupport.get_dict("first_config"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.content)

        # create - success
        response = requests.post(url, json=MySupport.get_dict("second_config"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.content)

        # create - already exist
        response = requests.post(url, json=MySupport.get_dict("first_config"))
        self.assertEqual(response.status_code, 409)
        self.assertFalse(response.content)

        # create - success
        response = requests.post(url, json=MySupport.get_dict("third_config"))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.content)

        # get cfg info
        response = requests.get(url_info)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)


        expected["files"].append("sensiblename-1-01.cfg")
        expected["files"].append("terriblename-5-23.cfg")
        expected["files"].append("terriblename-5-78.cfg")

        json = response.json()
        self.assertEqual(json, expected)


