import json
from pathlib import Path

from scripts.generate_knowledge_snapshot import (
    generate,
)


def test_snapshot_can_be_generated():
    generate()
    snapshot_path = Path("knowledge_snapshot.json")
    assert snapshot_path.exists()

    data = json.loads(snapshot_path.read_text())
    assert "current_phase" in data
    assert "next_steps" in data
    assert "vision" in data


def test_simulated_ai_reading():
    """
    Simulates an AI Agent reading the snapshot.
    The assertions represent questions the AI must be able to answer.
    """
    # 1. READ SNAPSHOT
    generate()
    data = json.loads(Path("knowledge_snapshot.json").read_text())

    # Q1: What is this project?
    assert "Spriter" in data["project"]
    assert "clean arch" in data["vision"].lower()

    # Q2: Where are we?
    assert data["current_phase"]["manifest_phase"] is not None
    assert data["current_phase"]["consistent"] is True, (
        "AI detects inconsistency in project state!"
    )

    # Q3: What is the latest architectural decision?
    assert data["knowledge_status"]["latest_adr"] is not None
    assert (
        "0*.md" not in data["knowledge_status"]["latest_adr"]
    )  # Should check real filename format if possible
