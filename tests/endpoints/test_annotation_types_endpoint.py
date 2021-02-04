import os
import sys
sys.path.insert(0, os.getcwd())
import json
import unittest
from fastapi.testclient import TestClient
from src.main import app
from src.database.crud import delete_table_rows
from src.models.annotation_types import AnnotationTypeModel
client = TestClient(app)


class TestAnnotationTypesEndpoint(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAnnotationTypesEndpoint, self).__init__(*args, **kwargs)
        self.client = TestClient(app)
        # Test annotation type data
        self.test_annotation_type = {"id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                     "objective_name": "gr",
                                     "label_name": "genre",
                                     "value_type": "str"}
        # Test Updated annotation type
        self.updated_test_annotator = {"id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                       "objective_name": "ge",
                                       "label_name": "genre",
                                       "value_type": "str"}
        # Test wrong param annotation type
        self.test_wrong_annotation_type = {"id": "1206a713-129e-445d-9532-8d682d911be9",
                                           "objective_name": "gr"}

    def setUp(self):
        # Clean table
        delete_table_rows(AnnotationTypeModel)

    def tearDown(self):
        # Clean table
        delete_table_rows(AnnotationTypeModel)

    def test_01_post_annotation_type(self):
        # Create annotation type
        response = client.post("/annotation_types", json.dumps(self.test_annotation_type))
        assert response.status_code == 200

    def test_02_post_annotation_type_with_wrong_parameter(self):
        # Create annotation type
        response = client.post("/annotation_types", json.dumps(self.test_wrong_annotation_type))
        assert response.status_code == 422

    def test_03_get_annotation_type_all(self):
        # Get all annotation_types
        response = client.get("/annotation_types")
        assert response.status_code == 200

    def test_04_get_annotation_type_by_wrong_id(self):
        # Create annotation type
        response = client.post("/annotation_types", json.dumps(self.test_annotation_type))
        assert response.status_code == 200
        # Get annotation type by ID
        response = client.get(f"/annotation_types/id/{self.test_wrong_annotation_type['id']}")
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_annotation_type['id']} does not exist"

    def test_05_get_annotation_type_by_id(self):
        # Create annotation type
        response = client.post("/annotation_types", json.dumps(self.test_annotation_type))
        assert response.status_code == 200
        # Get annotation type by ID
        response = client.get(f"/annotation_types/id/{self.test_annotation_type['id']}")
        assert response.status_code == 200

    def test_06_get_annotation_type_by_wrong_id(self):
        # Create annotation type
        response = client.post("/annotation_types", json.dumps(self.test_annotation_type))
        assert response.status_code == 200
        # Get annotation type by ID
        response = client.get(f"/annotation_types/id/{self.test_wrong_annotation_type['id']}")
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_annotation_type['id']} does not exist"

    def test_07_update_annotation_type(self):
        # Create annotation type
        response = client.post("/annotation_types", json.dumps(self.test_annotation_type))
        assert response.status_code == 200
        # Put annotation type
        response = client.put("/annotation_types", json.dumps(self.updated_test_annotator))
        assert response.status_code == 200
        # Get annotation type by updated name
        response = client.get(f"/annotation_types/id/{self.updated_test_annotator['id']}")
        assert response.status_code == 200
        assert json.loads(response.content)['objective_name'] == self.updated_test_annotator['objective_name']

    def test_08_update_annotation_type_wrong_name(self):
        # Create annotation type
        response = client.post("/annotation_types", json.dumps(self.test_annotation_type))
        assert response.status_code == 200
        # Put annotation type
        response = client.put("/annotation_types", json.dumps(self.test_wrong_annotation_type))
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_annotation_type['id']} does not exist"

    def test_09_delete_annotation_type_by_id(self):
        # Create annotation type
        response = client.post("/annotation_types", json.dumps(self.test_annotation_type))
        assert response.status_code == 200
        # Delete annotation type by ID
        response = client.delete(f"/annotation_types/id/{self.updated_test_annotator['id']}")
        assert response.status_code == 200

    def test_10_delete_annotation_type_wrong_id(self):
        # Create annotation type
        response = client.post("/annotation_types", json.dumps(self.test_annotation_type))
        assert response.status_code == 200
        # Delete annotation type by ID
        response = client.delete(f"/annotation_types/id/{self.test_wrong_annotation_type['id']}")
        assert response.status_code == 400
