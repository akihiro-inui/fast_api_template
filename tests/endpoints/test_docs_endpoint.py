import os
import sys
sys.path.insert(0, os.getcwd())
import unittest
from fastapi.testclient import TestClient
from src.main import app


class TestDocsEndpoint(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDocsEndpoint, self).__init__(*args, **kwargs)
        self.client = TestClient(app)

    def test_01_get_docs(self):
        # Get docs
        response = self.client.get("/docs")
        assert response.status_code == 200

    def test_02_get_main(self):
        # Get docs
        response = self.client.get("/")
        assert response.status_code == 200
