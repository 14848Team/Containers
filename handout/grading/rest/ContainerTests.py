import requests, unittest, json
from MySupport import MySupport

class ContainerTests(unittest.TestCase):
    HOSTNAME = "host"
    PORT = 80

    def suite():
        suite = unittest.TestSuite()
        suite.addTest(ContainerTests('test_main'))
        return suite

    def test_main(self):
        url =  MySupport.url(self.HOSTNAME, self.PORT, "/launch")

        # launch first
        first_config = MySupport.get_dict("first_config")
        first_launch = MySupport.get_dict("first_launch")
        response = requests.post(url, json=first_launch)

        # launch second
        second_config = MySupport.get_dict("second_config")
        second_launch = MySupport.get_dict("second_launch")
        response = requests.post(url, json=second_launch)

        # launch third
        third_config = MySupport.get_dict("third_config")
        third_launch = MySupport.get_dict("third_launch")
        response = requests.post(url, json=third_launch)

        # check first
        url = MySupport.url("localhost", "10000", "/potato/potato.html")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertEqual(response.content.decode("utf-8").strip(), "ich bin ein kartoffel")

        # check second
        url = MySupport.url("localhost", "20000", "/cabbage/cabbage.html")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertEqual(response.content.decode("utf-8").strip(), "my cabbages!")

        url = MySupport.url("localhost", "20000", "/cabbage/potato/potato.html")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertEqual(response.content.decode("utf-8").strip(), "ich bin ein kartoffel")

        # check third
        url = MySupport.url("localhost", "30000", "/potato/potato.html")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertEqual(response.content.decode("utf-8").strip(), "ich bin ein kartoffel")

        url = MySupport.url("localhost", "30000", "/tomato/tomato.html")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertEqual(response.content.decode("utf-8").strip(), "heinzzz")

        url = MySupport.url("localhost", "30000", "/tomato/cabbage/cabbage.html")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertEqual(response.content.decode("utf-8").strip(), "my cabbages!")

