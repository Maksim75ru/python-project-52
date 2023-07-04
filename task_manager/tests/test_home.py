from django.test import SimpleTestCase


class SimpleTest(SimpleTestCase):

    def test_open_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)