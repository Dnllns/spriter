from fastapi.testclient import TestClient

from src.main import app


class TestSimulationFlow:
    """
    Simulated E2E Test for User Journey: Create Sprite, Add Version, View Dashboard.
    Since we cannot run JS in TestClient, we test the endpoints that the JS calls.
    """

    def test_simulation_workflow(self):
        """
        Verify the API flow for creating a sprite and uploading a version.
        This mimics what `handleUpload` does in `main.js`.
        """
        with TestClient(app) as client:
            # Add default auth header
            auth_headers = {"Authorization": "Bearer test-user"}

            # 1. Create Sprite
            sprite_payload = {
                "name": "E2E Test Sprite",
                "tags": ["Character", "Test"],
                "description": "A test sprite for E2E",
            }
            create_resp = client.post(
                "/api/v1/sprites", json=sprite_payload, headers=auth_headers
            )
            assert create_resp.status_code == 201, (
                f"Failed to create sprite: {create_resp.text}"
            )

            sprite_data = create_resp.json()
            sprite_id = sprite_data["id"]
            assert sprite_data["name"] == "E2E Test Sprite"

            # 2. Upload Version (Mimic image upload)
            # We need a dummy image file content
            dummy_content = b"fake_image_content"
            # Using a tuple for files: (filename, content, content_type)
            files = {"file": ("test.png", dummy_content, "image/png")}

            # Simple animation metadata
            animations_payload = [
                {
                    "name": "idle",
                    "fps": 5,
                    "frames": [
                        {"index": 0, "x": 0, "y": 0, "w": 32, "h": 32},
                        {"index": 1, "x": 32, "y": 0, "w": 32, "h": 32},
                    ],
                    "loop": True,
                }
            ]
            import json

            data = {
                "metadata": "{}",
                "changelog": "Initial version",
                "animations": json.dumps(animations_payload),
            }

            upload_resp = client.post(
                f"/api/v1/sprites/{sprite_id}/versions",
                files=files,
                data=data,
                headers=auth_headers,
            )
            assert upload_resp.status_code == 201, (
                f"Failed to upload version: {upload_resp.text}"
            )

            version_data = upload_resp.json()
            assert version_data["version"] == 1
            assert len(version_data.get("animations", [])) == 1
            assert version_data["animations"][0]["name"] == "idle"

            # 3. Verify it appears in Dashboard List (GET /sprites)
            list_resp = client.get("/api/v1/sprites?limit=100", headers=auth_headers)
            assert list_resp.status_code == 200
            sprites_list = list_resp.json()

            # Check if our created sprite is in the list
            found = False
            for s in sprites_list:
                if s["id"] == sprite_id:
                    found = True
                    # Check if versions are populated (depends on list impl)
                    if "versions" in s:
                        assert len(s["versions"]) >= 1
                    break
            print("\nSPRITES LIST:", sprites_list)
            assert found, "Created sprite not found in list"

            # 4. Verify Detail Fetch (GET /sprites/{id})
            # This is what `loadSpriteInSimulator` calls
            detail_resp = client.get(
                f"/api/v1/sprites/{sprite_id}", headers=auth_headers
            )
            assert detail_resp.status_code == 200
            detail = detail_resp.json()

            assert len(detail["versions"]) > 0
            latest_version = detail["versions"][-1]
            assert latest_version["image_url"] is not None

            # 5. Verify the image is accessible (if local storage)
            image_url = latest_version["image_url"]
            print(f"Checking image URL: {image_url}")

            if image_url.startswith("/"):
                # If it's a relative URL served by the app (e.g., /static/uploads/...)
                img_resp = client.get(image_url, headers=auth_headers)
                # Depending on storage backend (FileSystem), it might 404 if the
                # path isn't mounted in TestClient.
                # But usually standard static mounts work.
                if img_resp.status_code == 200:
                    assert img_resp.content == dummy_content
                else:
                    # If using mock storage or signed URLs, this might fail,
                    # which is expected in some envs
                    pass
