from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_ac_004_01_simulate_frame():
    """
    Validation for AC-004-01: Endpoint Calculation
    POST /api/v1/simulate
    Input: Animation + elapsed_ms
    Output: FrameResult (index, progress)
    """

    # Arrange: Create payload matching AC
    payload = {
        "animation": {
            "name": "TestAnim",
            "type": "run",
            "frames": [
                {"index": 0, "duration_ms": 100},
                {"index": 1, "duration_ms": 100},
            ],
            "loop": True,
        },
        "elapsed_ms": 150,
    }

    # Act
    # This endpoint doesn't exist yet, we expect 404 or failing assertion
    response = client.post("/api/v1/simulate", json=payload)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["frame_index"] == 1
    assert data["frame_progress"] == 0.5
    assert data["is_finished"] is False


def test_ac_004_02_invalid_input():
    """
    Validation for AC-004-02: Invalid Input Handling
    """
    payload = {
        "animation": {"name": "TestAnim", "type": "custom", "frames": []},
        "elapsed_ms": "invalid-string",  # Invalid type
    }

    # Act
    response = client.post("/api/v1/simulate", json=payload)

    # Assert
    # Expect 422 standard validation from Pydantic
    assert response.status_code == 422
