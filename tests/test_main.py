# test_main.py

from fastapi.testclient import TestClient
from app.main import app
import os
import io

client = TestClient(app)


def test_upload_csv():
    file_path = os.path.join("uploads", "img.csv")
    assert os.path.exists(file_path), f"Test file {file_path} does not exist."

    with open(file_path, "rb") as f:
        response = client.post(
            "/upload_csv/", files={"file": ("img.csv", f, "text/csv")}
        )
    assert (
        response.status_code == 200
    ), f"Response status code was {response.status_code}, expected 200."
    assert (
        response.headers["content-type"] == "image/png"
    ), "Response content-type is not 'image/png'."
    assert response.content != b"", "Response content is empty."


def test_get_images_by_depth():
    file_path = os.path.join("uploads", "img.csv")
    with open(file_path, "rb") as f:
        upload_response = client.post(
            "/upload_csv/", files={"file": ("img.csv", f, "text/csv")}
        )
    assert (
        upload_response.status_code == 200
    ), f"Upload failed with status code {upload_response.status_code}."

    depth_min = 0.0
    depth_max = 10000.0

    response = client.get(f"/images/?depth_min={depth_min}&depth_max={depth_max}")
    assert (
        response.status_code == 200
    ), f"GET /images/ failed with status code {response.status_code}."
    data = response.json()
    assert isinstance(data, list), "Response data is not a list."
    assert len(data) > 0, "No images returned in the specified depth range."
    for image_info in data:
        assert "id" in image_info, "'id' not in image info."
        assert "depth_min" in image_info, "'depth_min' not in image info."
        assert "depth_max" in image_info, "'depth_max' not in image info."
        assert "filename" in image_info, "'filename' not in image info."
        assert (
            depth_min <= image_info["depth_min"] <= depth_max
        ), "Image 'depth_min' not within range."
        assert (
            depth_min <= image_info["depth_max"] <= depth_max
        ), "Image 'depth_max' not within range."


def test_get_image_by_id():
    file_path = os.path.join("uploads", "img.csv")
    with open(file_path, "rb") as f:
        upload_response = client.post(
            "/upload_csv/", files={"file": ("img.csv", f, "text/csv")}
        )
    assert (
        upload_response.status_code == 200
    ), f"Upload failed with status code {upload_response.status_code}."

    depth_min = 0.0
    depth_max = 10000.0
    images_response = client.get(
        f"/images/?depth_min={depth_min}&depth_max={depth_max}"
    )
    assert (
        images_response.status_code == 200
    ), f"GET /images/ failed with status code {images_response.status_code}."
    images = images_response.json()
    assert len(images) > 0, "No images returned to retrieve an ID from."
    image_id = images[0]["id"]

    response = client.get(f"/images/{image_id}")
    assert (
        response.status_code == 200
    ), f"GET /images/{image_id} failed with status code {response.status_code}."
    assert (
        response.headers["content-type"] == "image/png"
    ), "Response content-type is not 'image/png'."
    assert response.content != b"", "Response content is empty."
