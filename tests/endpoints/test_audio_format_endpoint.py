import os
import sys
sys.path.insert(0, os.getcwd())
import json
import unittest
from fastapi.testclient import TestClient
from src.main import app
from src.database.crud import delete_table_rows
from src.models.audio_format import AudioFormatModel
client = TestClient(app)


class TestAudioFormatTypesEndpoint(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAudioFormatTypesEndpoint, self).__init__(*args, **kwargs)
        self.client = TestClient(app)
        # Test audio_format type data
        self.test_audio_format_type = {"id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                       "bit_rate": 16,
                                       "sample_rate": 44100,
                                       "channels": 2}
        # Test Updated audio_format type
        self.updated_test_audio_format = {"id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                          "bit_rate": 16,
                                          "sample_rate": 22500,
                                          "channels": 2}
        # Test wrong param audio_format type
        self.test_wrong_audio_format_type = {"id": "1206a713-129e-445d-9532-8d682d911be9",
                                             "bit_rate": 16}

    def setUp(self):
        # Clean table
        delete_table_rows(AudioFormatModel)

    def tearDown(self):
        # Clean table
        delete_table_rows(AudioFormatModel)

    def test_01_post_audio_format(self):
        # Create audio_format type
        response = client.post("/audio_format", json.dumps(self.test_audio_format_type))
        assert response.status_code == 200

    def test_02_post_audio_format_with_wrong_parameter(self):
        # Create audio_format type
        response = client.post("/audio_format", json.dumps(self.test_wrong_audio_format_type))
        assert response.status_code == 422

    def test_03_get_audio_format_all(self):
        # Get all audio_format
        response = client.get("/audio_format")
        assert response.status_code == 200

    def test_04_get_audio_format_by_wrong_id(self):
        # Create audio_format type
        response = client.post("/audio_format", json.dumps(self.test_audio_format_type))
        assert response.status_code == 200
        # Get audio_format type by ID
        response = client.get(f"/audio_format/id/{self.test_wrong_audio_format_type['id']}")
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_audio_format_type['id']} does not exist"

    def test_05_get_audio_format_by_id(self):
        # Create audio_format type
        response = client.post("/audio_format", json.dumps(self.test_audio_format_type))
        assert response.status_code == 200
        # Get audio_format type by ID
        response = client.get(f"/audio_format/id/{self.test_audio_format_type['id']}")
        assert response.status_code == 200

    def test_06_get_audio_format_by_wrong_id(self):
        # Create audio_format type
        response = client.post("/audio_format", json.dumps(self.test_audio_format_type))
        assert response.status_code == 200
        # Get audio_format type by ID
        response = client.get(f"/audio_format/id/{self.test_wrong_audio_format_type['id']}")
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_audio_format_type['id']} does not exist"

    def test_07_update_audio_format(self):
        # Create audio_format type
        response = client.post("/audio_format", json.dumps(self.test_audio_format_type))
        assert response.status_code == 200
        # Put audio_format type
        response = client.put("/audio_format", json.dumps(self.updated_test_audio_format))
        assert response.status_code == 200
        # Get audio_format type by updated name
        response = client.get(f"/audio_format/id/{self.updated_test_audio_format['id']}")
        assert response.status_code == 200
        assert json.loads(response.content)['sample_rate'] == self.updated_test_audio_format['sample_rate']

    def test_08_update_audio_format_wrong_name(self):
        # Create audio_format type
        response = client.post("/audio_format", json.dumps(self.test_audio_format_type))
        assert response.status_code == 200
        # Put audio_format type
        response = client.put("/audio_format", json.dumps(self.test_wrong_audio_format_type))
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_audio_format_type['id']} does not exist"

    def test_09_delete_audio_format_by_id(self):
        # Create audio_format type
        response = client.post("/audio_format", json.dumps(self.test_audio_format_type))
        assert response.status_code == 200
        # Delete audio_format type by ID
        response = client.delete(f"/audio_format/id/{self.updated_test_audio_format['id']}")
        assert response.status_code == 200

    def test_10_delete_audio_format_wrong_id(self):
        # Create audio_format type
        response = client.post("/audio_format", json.dumps(self.test_audio_format_type))
        assert response.status_code == 200
        # Delete audio_format type by ID
        response = client.delete(f"/audio_format/id/{self.test_wrong_audio_format_type['id']}")
        assert response.status_code == 400
