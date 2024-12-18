import os
import requests

ENDPOINT = os.getenv("ENDPOINT", "http://localhost:5000")

def test_home_page():
    response = requests.get(f"{ENDPOINT}/")
    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
    assert "MultiClouds.Tech" in response.text, "Homepage content does not match expected text"


def test_nonexistent_page():
    response = requests.get(f"{ENDPOINT}/nonexistent")
    assert response.status_code == 404, f"Expected 404, but got {response.status_code}"
    assert "404 Not Found" in response.text, "Error page content does not include '404 Not Found'"