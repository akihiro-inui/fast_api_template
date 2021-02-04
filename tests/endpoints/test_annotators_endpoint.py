import os
import sys
sys.path.insert(0, os.getcwd())
import json
import unittest
from fastapi.testclient import TestClient
from src.main import app
from src.database.crud import delete_table_rows
from src.models.organizations import OrganizationModel
from src.models.annotators import AnnotatorModel
client = TestClient(app)


class TestAnnotatorsEndpoint(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAnnotatorsEndpoint, self).__init__(*args, **kwargs)
        self.client = TestClient(app)
        # Test organization data
        self.test_organization = {"id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                  "name": "test organization"}
        # Test annotator data
        self.test_annotator = {"id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                               "name": "test annotator",
                               "age": 28,
                               "gender": "male",
                               "organization_id": "2d6bb3c2-c168-457b-851d-78d29ded089e"}
        # Test Updated annotator
        self.updated_test_annotator = {"id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                       "name": "updated test annotator",
                                       "age": 26}
        # Test wrong param annotator
        self.test_wrong_annotator = {"id": "1206a713-129e-445d-9532-8d682d911be9",
                                     "name": "wrong annotator",
                                     "age": 20}

    def setUp(self):
        # Clean table
        delete_table_rows(OrganizationModel)
        delete_table_rows(AnnotatorModel)

    def tearDown(self):
        # Clean table
        delete_table_rows(OrganizationModel)
        delete_table_rows(AnnotatorModel)

    def test_01_post_annotator(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Create annotator
        response = client.post("/annotators", json.dumps(self.test_annotator))
        assert response.status_code == 200

    def test_02_post_annotator_with_wrong_parameter(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Create annotator
        response = client.post("/annotators", json.dumps(self.test_wrong_annotator))
        assert response.status_code == 422

    def test_03_get_annotator_all(self):
        # Get all annotators
        response = client.get("/annotators")
        assert response.status_code == 200

    def test_04_get_annotator_by_name(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Create annotator
        response = client.post("/annotators", json.dumps(self.test_annotator))
        assert response.status_code == 200
        # Get annotator by name
        response = client.get(f"/annotators/name/{self.test_annotator['name']}")
        assert response.status_code == 200

    def test_05_get_annotator_by_wrong_name(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Create annotator
        response = client.post("/annotators", json.dumps(self.test_annotator))
        assert response.status_code == 200
        # Get annotator by name
        response = client.get(f"/annotators/name/{self.test_wrong_annotator['name']}")
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_annotator['name']} does not exist"

    def test_06_get_annotator_by_id(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Create annotator
        response = client.post("/annotators", json.dumps(self.test_annotator))
        assert response.status_code == 200
        # Get annotator by ID
        response = client.get(f"/annotators/id/{self.test_annotator['id']}")
        assert response.status_code == 200

    def test_07_get_annotator_by_wrong_id(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Create annotator
        response = client.post("/annotators", json.dumps(self.test_annotator))
        assert response.status_code == 200
        # Get annotator by ID
        response = client.get(f"/annotators/id/{self.test_wrong_annotator['id']}")
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_annotator['id']} does not exist"

    def test_08_update_annotator(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Create annotator
        response = client.post("/annotators", json.dumps(self.test_annotator))
        assert response.status_code == 200
        # Put annotator
        response = client.put("/annotators", json.dumps(self.updated_test_annotator))
        assert response.status_code == 200
        # Get annotator by updated name
        response = client.get(f"/annotators/name/{self.updated_test_annotator['name']}")
        assert response.status_code == 200
        assert json.loads(response.content)['name'] == self.updated_test_annotator['name']
        assert json.loads(response.content)['age'] == self.updated_test_annotator['age']

    def test_09_update_annotator_wrong_name(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Create annotator
        response = client.post("/annotators", json.dumps(self.test_annotator))
        assert response.status_code == 200
        # Put annotator
        response = client.put("/annotators", json.dumps(self.test_wrong_annotator))
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_annotator['id']} does not exist"

    def test_10_delete_annotator_by_id(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Create annotator
        response = client.post("/annotators", json.dumps(self.test_annotator))
        assert response.status_code == 200
        # Delete annotator by ID
        response = client.delete(f"/annotators/id/{self.updated_test_annotator['id']}")
        assert response.status_code == 200

    def test_11_delete_annotator_wrong_id(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Create annotator
        response = client.post("/annotators", json.dumps(self.test_annotator))
        assert response.status_code == 200
        # Delete annotator by ID
        response = client.delete(f"/annotators/id/{self.test_wrong_annotator['id']}")
        assert response.status_code == 400
