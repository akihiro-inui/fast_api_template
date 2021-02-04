import os
import sys
sys.path.insert(0, os.getcwd())
import json
import unittest
from fastapi.testclient import TestClient
from src.main import app
from src.database.crud import delete_table_rows
from src.models.organizations import OrganizationModel
client = TestClient(app)


class TestOrganizationsEndpoint(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestOrganizationsEndpoint, self).__init__(*args, **kwargs)
        self.client = TestClient(app)

        # Test organization data
        self.test_organization = {"id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                  "name": "test organization"}
        # Test Updated data
        self.updated_test_organization = {"id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                          "name": "updated test organization"}
        # Test wrong param data
        self.test_wrong_organization = {"id": "1206a713-129e-445d-9532-8d682d911be9"}

    def setUp(self):
        # Clean table
        delete_table_rows(OrganizationModel)

    def tearDown(self):
        # Clean table
        delete_table_rows(OrganizationModel)

    def test_01_post_organization(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200

    def test_02_post_organization_with_wrong_parameter(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_wrong_organization))
        assert response.status_code == 422

    def test_03_get_organization_all(self):
        # Get all organizations
        response = client.get("/organizations")
        assert response.status_code == 200

    def test_04_get_organization_by_name(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Get organization by name
        response = client.get(f"/organizations/name/{self.test_organization['name']}")
        assert response.status_code == 200

    def test_05_get_organization_by_wrong_name(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Get organization by name
        response = client.get(f"/organizations/name/wrong_organization_name")
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"wrong_organization_name does not exist"

    def test_06_get_organization_by_id(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Get organization by ID
        response = client.get(f"/organizations/id/{self.test_organization['id']}")
        assert response.status_code == 200

    def test_07_get_organization_by_wrong_id(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Get organization by ID
        response = client.get(f"/organizations/id/{self.test_wrong_organization['id']}")
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_organization['id']} does not exist"

    def test_08_update_organization(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Put organization
        response = client.put("/organizations", json.dumps(self.updated_test_organization))
        assert response.status_code == 200
        # Get organization by updated name
        response = client.get(f"/organizations/name/{self.updated_test_organization['name']}")
        assert response.status_code == 200
        assert json.loads(response.content)['name'] == self.updated_test_organization['name']

    def test_09_update_organization_wrong_name(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Put organization
        response = client.put("/organizations", json.dumps(self.test_wrong_organization))
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_organization['id']} does not exist"

    def test_10_delete_organization_by_id(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Delete organization by ID
        response = client.delete(f"/organizations/id/{self.updated_test_organization['id']}")
        assert response.status_code == 200

    def test_11_delete_organization_wrong_id(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Delete organization by ID
        response = client.delete(f"/organizations/id/{self.test_wrong_organization['id']}")
        assert response.status_code == 400
