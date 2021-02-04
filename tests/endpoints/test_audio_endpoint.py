import os
import sys
sys.path.insert(0, os.getcwd())
import json
import unittest
from fastapi.testclient import TestClient
from src.main import app
from src.database.crud import delete_table_rows
from src.models.audio import AudioModel
client = TestClient(app)


class TestAudioEndpoint(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAudioEndpoint, self).__init__(*args, **kwargs)
        self.client = TestClient(app)
        # Test audio data
        self.test_audio = {"md5": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                           "file_name": "audio.wav",
                           "audio_format_id": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                           "duration": 214134,
                           "custom_property": json.dumps({"external_id": "external ID"}),
                           "organization_id": "2d6bb3c2-c168-457b-851d-78d29ded089e"}
        # Test Updated audio
        self.updated_test_audio = {"md5": "2d6bb3c2-c168-457b-851d-78d29ded089e",
                                   "file_name": "updated_audio.wav",
                                   "custom_property": json.dumps({"external_id": "updated external ID"})}
        # Test wrong param audio
        self.test_wrong_audio = {"md5": "1206a713-129e-445d-9532-8d682d911be9",
                                 "file_name": "wrong_audio.wav"}

    def setUp(self):
        # Clean table
        delete_table_rows(AudioModel)

    def tearDown(self):
        # Clean table
        delete_table_rows(AudioModel)

    def test_01_post_audio(self):
        # Create audio
        response = client.post("/audio", json.dumps(self.test_audio))
        assert response.status_code == 200

    def test_02_post_audio_with_wrong_parameter(self):
        # Create audio
        response = client.post("/audio", json.dumps(self.test_wrong_audio))
        assert response.status_code == 422

    def test_03_get_audio_all(self):
        # Get all annotators
        response = client.get("/audio")
        assert response.status_code == 200

    def test_04_get_audio_by_md5(self):
        # Create audio
        response = client.post("/audio", json.dumps(self.test_audio))
        assert response.status_code == 200
        # Get audio by md5
        response = client.get(f"/audio/md5/{self.test_audio['md5']}")
        assert response.status_code == 200

    def test_05_get_audio_by_wrong_md5(self):
        # Create audio
        response = client.post("/audio", json.dumps(self.test_audio))
        assert response.status_code == 200
        # Get audio by name
        response = client.get(f"/audio/md5/{self.test_wrong_audio['md5']}")
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_audio['md5']} does not exist"

    def test_06_get_audio_by_file_path(self):
        # Create audio
        response = client.post("/audio", json.dumps(self.test_audio))
        assert response.status_code == 200
        # Get audio by file path
        response = client.get(f"/audio/file_name/{self.test_audio['file_name']}")
        assert response.status_code == 200

    def test_07_get_audio_by_wrong_file_path(self):
        # Create audio
        response = client.post("/audio", json.dumps(self.test_audio))
        assert response.status_code == 200
        # Get audio by file path
        response = client.get(f"/audio/file_name/{self.test_wrong_audio['file_name']}")
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_audio['file_name']} does not exist"

    def test_08_update_audio(self):
        # Create audio
        response = client.post("/audio", json.dumps(self.test_audio))
        assert response.status_code == 200
        # Put audio
        response = client.put("/audio", json.dumps(self.updated_test_audio))
        assert response.status_code == 200
        # Get audio by updated md5
        response = client.get(f"/audio/md5/{self.test_audio['md5']}")
        assert response.status_code == 200
        assert json.loads(response.content)['file_name'] == self.updated_test_audio['file_name']

    def test_09_update_audio_wrong_name(self):
        # Create audio
        response = client.post("/audio", json.dumps(self.test_audio))
        assert response.status_code == 200
        # Put audio
        response = client.put("/audio", json.dumps(self.test_wrong_audio))
        assert response.status_code == 400
        assert json.loads(response.content)['detail'] == f"{self.test_wrong_audio['md5']} does not exist"

    def test_10_delete_annotator_by_md5(self):
        # Create audio
        response = client.post("/audio", json.dumps(self.test_audio))
        assert response.status_code == 200
        # Delete audio by ID
        response = client.delete(f"/audio/md5/{self.updated_test_audio['md5']}")
        assert response.status_code == 200

    def test_11_delete_annotator_wrong_md5(self):
        # Create audio
        response = client.post("/audio", json.dumps(self.test_audio))
        assert response.status_code == 200
        # Delete audio by ID
        response = client.delete(f"/audio/md5/{self.test_wrong_audio['md5']}")
        assert response.status_code == 400
