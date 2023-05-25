import unittest
from fastapi.testclient import TestClient
from main import app
from fastapi import  status



class TestApp(unittest.TestCase):
    client = TestClient(app)

    def test_hello(self):
        response = self.client.get("/hello")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '"Hello Radwa! FROM OMAR (I mean babe) hehee shhhh"')

if __name__ == '__main__':
    unittest.main()
