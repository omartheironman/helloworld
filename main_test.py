import unittest
from fastapi.testclient import TestClient
from main import app
from fastapi import  status



class TestApp(unittest.TestCase):
    client = TestClient(app)

    def test_healthz(self):
        response = self.client.get("/healthz")
        self.assertEqual(response.status_code, 200)

    def test_readyz(self):
        response = self.client.get("/readyz")
        self.assertEqual(response.status_code, 200)

    def test_enable_readyz(self):
        with TestClient(app) as client:
            response = client.get("/readyz/enable")
            self.assertTrue(response.status_code == 200 or response.status_code == 409)

    def test_disable_readyz(self):
        response = self.client.get("/readyz/disable")
        self.assertEqual(response.status_code, 200)

    def test_env(self):
        response = self.client.get("/env")
        self.assertEqual(response.status_code, 200)

    def test_headers(self):
        response = self.client.get("/headers")
        self.assertEqual(response.status_code, 200)

    def test_delay(self):
        response = self.client.get("/delay/1")
        self.assertEqual(response.status_code, 200)

    def test_cache(self):
        response = self.client.put("/cache/test_key", data="test_value")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/cache/test_key")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, '"test_value"')

    def test_delete_key(self):
        response = self.client.put("/cache/test_key", data=b"test_value")
        self.assertEqual(response.status_code, 200)
        response = self.client.delete("/cache/test_key")
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/cache/test_key")
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()