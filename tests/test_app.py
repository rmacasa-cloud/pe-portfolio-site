# tests/test_app.py

import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Red" in html
        assert "About Me" in html
        assert "CS @ UC Santa Barbara · MLH Fellow" in html
        assert "<p>Originally from Oregon" in html


    def test_timeline(self):
        # Initial retrieval has nothing
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert len(json) == 0

        # Add 2 timeline posts
        response = self.client.post("/api/timeline_post", json={
            "name": "Test1",
            "email": "test1@email.com",
            "content": "This is the first test",
        })
        assert response.status_code == 201
        assert response.is_json
        json = response.get_json()
        assert json["name"] == "Test1" and json["email"] == "test1@email.com" and json["content"] == "This is the first test"

        response = self.client.post("/api/timeline_post", json={
            "name": "Test2",
            "email": "test2@email.com",
            "content": "This is the second test",
        })
        assert response.status_code == 201
        assert response.is_json
        json = response.get_json()
        assert json["name"] == "Test2" and json["email"] == "test2@email.com" and json["content"] == "This is the second test"

        # Check if we now have 2 timeline posts
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert len(json) == 2

        # Delete timeline post
        response = self.client.delete("/api/timeline_post/2")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert json["deleted"] == 2


        # Check timeline post count after deletion
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert len(json) == 1

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", json={"email": "john@example.com", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", json={"name": "John Doe", "email": "john@example.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", json={"name": "John Doe", "email": "not-an-email", "content": "Hello world, I'm John!"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html

