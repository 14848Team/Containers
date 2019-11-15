import requests, unittest, json
from MySupport import MySupport

class LaunchTests(unittest.TestCase):
    HOSTNAME = "host"
    PORT = 80

    def suite():
        suite = unittest.TestSuite()
        suite.addTest(LaunchTests('test_main'))
        return suite

    def test_main(self):
        url_launch =  MySupport.url(self.HOSTNAME, self.PORT, "/launch")
        url_list =  MySupport.url(self.HOSTNAME, self.PORT, "/list")

        data = {}

        expected = {
            "instances": []
        }

        # get running instances - none
        response = requests.get(url_list)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)

        json = response.json()
        self.assertEqual(json, expected)

        # launch first
        first = MySupport.get_dict("first_launch")
        response = requests.post(url_launch, json=first)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)

        first_data = response.json()
        expected["instances"].append(first_data)

        self.assertEqual(first["name"], first_data["name"])
        self.assertEqual(first["major"], first_data["major"])
        self.assertEqual(first["minor"], first_data["minor"])

        # launch second
        second = MySupport.get_dict("second_launch")
        response = requests.post(url_launch, json=second)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)

        second_data = response.json()
        expected["instances"].append(second_data)

        self.assertEqual(second["name"], second_data["name"])
        self.assertEqual(second["major"], second_data["major"])
        self.assertEqual(second["minor"], second_data["minor"])

        # launch third
        third = MySupport.get_dict("third_launch")
        response = requests.post(url_launch, json=third)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)

        third_data = response.json()
        expected["instances"].append(third_data)

        self.assertEqual(third["name"], third_data["name"])
        self.assertEqual(third["major"], third_data["major"])
        self.assertEqual(third["minor"], third_data["minor"])

        # get running instances - three
        response = requests.get(url_list)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)

        json = response.json()
        self.assertEqual(json, expected)

        # test single destroy - not exist
        url_destroy =  MySupport.url(self.HOSTNAME, self.PORT, "/destroy/nope")
        response = requests.delete(url_destroy)
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.content)

        # test single destroy - first
        url_destroy =  MySupport.url(self.HOSTNAME, self.PORT, "/destroy/" + first_data["instance"])
        response = requests.delete(url_destroy)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)

        expected["instances"].pop() # remove first
        response = requests.get(url_list)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        json = response.json()
        self.assertEqual(json, expected)

        # test destroy all
        url_destroy =  MySupport.url(self.HOSTNAME, self.PORT, "/destroyall")
        response = requests.delete(url_destroy)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)

        expected["instances"].pop() # remove second
        expected["instances"].pop() # remove third
        response = requests.get(url_list)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        json = response.json()
        self.assertEqual(json, expected)


