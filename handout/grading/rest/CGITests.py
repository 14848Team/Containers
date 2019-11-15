import requests, unittest, json
from MySupport import MySupport

class CGITests(unittest.TestCase):
    HOSTNAME = "host"
    PORT = 80

    def suite():
        suite = unittest.TestSuite()
        suite.addTest(CGITests('test_main'))
        return suite

    def test_main(self):
        first_config = MySupport.get_dict("first_config")
        second_config = MySupport.get_dict("second_config")
        third_config = MySupport.get_dict("third_config")

        # check first
        url = MySupport.url("localhost", "10000", "/cgi-bin/ps.sh")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertEqual(response.content.decode("utf-8").count("tiny"), 1)

        # check second
        url = MySupport.url("localhost", "20000", "/cgi-bin/ps.sh")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertEqual(response.content.decode("utf-8").count("tiny"), 1)

        # check third
        url = MySupport.url("localhost", "30000", "/cgi-bin/ps.sh")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertEqual(response.content.decode("utf-8").count("tiny"), 1)

        # kill server 1
        url = MySupport.url("localhost", "10000", "/cgi-bin/pkill.sh")
        response = requests.get(url)

        try:
            url = MySupport.url("localhost", "10000", "/cgi-bin/ps.sh")
            response = requests.get(url)
            self.fail("Server 1 should be dead")
        except requests.ConnectionError as e: pass

        # check second
        url = MySupport.url("localhost", "20000", "/cgi-bin/ps.sh")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertEqual(response.content.decode("utf-8").count("tiny"), 1)

        # check third
        url = MySupport.url("localhost", "30000", "/cgi-bin/ps.sh")
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.content)
        self.assertEqual(response.content.decode("utf-8").count("tiny"), 1)


