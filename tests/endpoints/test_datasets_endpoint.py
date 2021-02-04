import os
import sys
sys.path.insert(0, os.getcwd())
import json
import datetime
import unittest
from fastapi.testclient import TestClient
from src.main import app
from src.database.crud import delete_table_rows
from src.models.annotators import AnnotatorModel
from src.models.annotation_types import AnnotationTypeModel
from src.models.organizations import OrganizationModel
from src.models.audio import AudioModel
from src.models.datasets import DatasetsModel
from src.models.audio_annotations import AudioAnnotationsModel

client = TestClient(app)


class TestDatasetsEndpoint(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDatasetsEndpoint, self).__init__(*args, **kwargs)
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
        # Test annotation type data
        self.test_annotation_type = {"id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                     "objective_name": "gr",
                                     "label_name": "genre",
                                     "value_type": "str"}

        # Test audio data
        self.test_audio = {"md5": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                           "file_name": "audio.wav",
                           "audio_format_id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                           "duration": 214134,
                           "custom_property": json.dumps({"external_id": "external ID"}),
                           "organization_id": "2d6bb3c2-c168-457b-851d-78d29ded089e"}

        # Test audio_annotation data
        self.test_audio_annotation = {"id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                      "annotation_type_id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                      "annotator_id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                      "dataset_id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                      "value": "Rock",
                                      "start_time": json.dumps((datetime.datetime.min + datetime.timedelta(seconds=0 / 1000.0)).time(), default=str),
                                      "stop_time": json.dumps((datetime.datetime.min + datetime.timedelta(seconds=209280 / 1000.0)).time(), default=str),
                                      "md5": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                      "version": 1}
        # Test dataset data
        self.test_dataset = {"id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                             "name": "genre_classification",
                             "type": "classification",
                             "description": "Music Genre Classification"}
        # Test Updated dataset
        self.updated_test_dataset = {"id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                     "name": "key_classification"}
        # Test wrong param dataset
        self.test_wrong_dataset = {"id": "1206a713-129e-445d-9532-8d682d911be9",
                                   "name": "key_detection"}

    def setUp(self):
        # Clean table
        delete_table_rows(AnnotatorModel)
        delete_table_rows(AnnotationTypeModel)
        delete_table_rows(OrganizationModel)
        delete_table_rows(AudioModel)
        delete_table_rows(DatasetsModel)
        delete_table_rows(AudioAnnotationsModel)

    def tearDown(self):
        # Clean table
        delete_table_rows(AnnotatorModel)
        delete_table_rows(AnnotationTypeModel)
        delete_table_rows(OrganizationModel)
        delete_table_rows(AudioModel)
        delete_table_rows(DatasetsModel)
        delete_table_rows(AudioAnnotationsModel)

    def test_01_post_dataset(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Create annotator
        response = client.post("/annotators", json.dumps(self.test_annotator))
        assert response.status_code == 200
        # Create audio
        response = client.post("/audio", json.dumps(self.test_audio))
        assert response.status_code == 200
        # Create annotation type
        response = client.post("/annotation_types", json.dumps(self.test_annotation_type))
        assert response.status_code == 200
        # Create dataset
        response = client.post("/datasets", json.dumps(self.test_dataset))
        assert response.status_code == 200
        # Create audio annotation
        response = client.post("/audio_annotations", json.dumps(self.test_audio_annotation))
        assert response.status_code == 200

    def test_02_post_dataset_with_wrong_parameter(self):
        # Create organization
        response = client.post("/organizations", json.dumps(self.test_organization))
        assert response.status_code == 200
        # Create annotator
        response = client.post("/annotators", json.dumps(self.test_annotator))
        assert response.status_code == 200
        # Create audio
        response = client.post("/audio", json.dumps(self.test_audio))
        assert response.status_code == 200
        # Create annotation type
        response = client.post("/annotation_types", json.dumps(self.test_annotation_type))
        assert response.status_code == 200
        # Create annotator
        response = client.post("/datasets", json.dumps(self.test_wrong_dataset))
        assert response.status_code == 422

    def test_03_get_dataset_all(self):
        # Get all Datasets
        response = client.get("/datasets")
        assert response.status_code == 200

    def test_04_get_dataset_by_name(self):
        # Create annotator
        response = client.post("/datasets", json.dumps(self.test_dataset))
        assert response.status_code == 200
        # Get annotator by name
        response = client.get(f"/datasets/name/{self.test_dataset['name']}")
        assert response.status_code == 200

    def test_05_get_dataset_by_wrong_name(self):
        # Create annotator
        response = client.post("/datasets", json.dumps(self.test_dataset))
        assert response.status_code == 200
        # Get annotator by name
        response = client.get(f"/datasets/name/{self.test_wrong_dataset['name']}")
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_dataset['name']} does not exist"

    def test_06_get_dataset_by_id(self):
        # Create annotator
        response = client.post("/datasets", json.dumps(self.test_dataset))
        assert response.status_code == 200
        # Get annotator by ID
        response = client.get(f"/datasets/id/{self.test_dataset['id']}")
        assert response.status_code == 200

    def test_07_get_dataset_by_wrong_id(self):
        # Create annotator
        response = client.post("/datasets", json.dumps(self.test_dataset))
        assert response.status_code == 200
        # Get annotator by ID
        response = client.get(f"/datasets/id/{self.test_wrong_dataset['id']}")
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_dataset['id']} does not exist"

    def test_08_update_dataset(self):
        # Create annotator
        response = client.post("/datasets", json.dumps(self.test_dataset))
        assert response.status_code == 200
        # Put annotator
        response = client.put("/datasets", json.dumps(self.updated_test_dataset))
        assert response.status_code == 200
        # Get annotator by updated name
        response = client.get(f"/datasets/id/{self.updated_test_dataset['id']}")
        assert response.status_code == 200
        assert json.loads(response.content)['name'] == self.updated_test_dataset['name']

    def test_09_update_dataset_wrong_name(self):
        # Create annotator
        response = client.post("/datasets", json.dumps(self.test_dataset))
        assert response.status_code == 200
        # Put annotator
        response = client.put("/datasets", json.dumps(self.test_wrong_dataset))
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_dataset['id']} does not exist"

    def test_10_delete_dataset_by_id(self):
        # Create annotator
        response = client.post("/datasets", json.dumps(self.test_dataset))
        assert response.status_code == 200
        # Delete annotator by ID
        response = client.delete(f"/datasets/id/{self.test_dataset['id']}")
        assert response.status_code == 200

    def test_11_delete_dataset_wrong_id(self):
        # Create annotator
        response = client.post("/datasets", json.dumps(self.test_dataset))
        assert response.status_code == 200
        # Delete annotator by ID
        response = client.delete(f"/datasets/id/{self.test_wrong_dataset['id']}")
        assert response.status_code == 400
