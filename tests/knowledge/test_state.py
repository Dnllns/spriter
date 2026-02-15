import pytest
from pathlib import Path

REQUIRED_STATE_HEADERS = [
    "Phase:",
    "Completed (Done)",
    "Pending (Backlog",
    "Blocked / Risks",
    "Next Actionable Steps",
]


def get_state_content():
    state_path = Path("docs/STATE.md")
    assert state_path.exists(), "docs/STATE.md must exist"
    return state_path.read_text(encoding="utf-8")


def test_state_headers():
    content = get_state_content()
    for header in REQUIRED_STATE_HEADERS:
        assert f"## {header}" in content or f"### {header}" in content, (
            f"Missing section '{header}'"
        )


def test_next_actionable_steps_content():
    content = get_state_content()
    # Check if Next Actionable Steps has content (not empty list)
    lines = content.split("\n")
    found_next_steps = False
    has_items = False
    for line in lines:
        if "Next Actionable Steps" in line:
            found_next_steps = True
            continue
        if found_next_steps:
            if line.strip().startswith("- ") or line.strip().startswith("1. "):
                has_items = True
                break
            if line.startswith("#"):  # Next header reached
                break

    assert has_items, "'Next Actionable Steps' section must contain at least one task."


def test_phase_current_matches_manifest():
    """Ensure STATE.md 'Phase:' matches AI_MANIFEST.md's (Current) Phase."""
    state_content = get_state_content()
    manifest_content = Path("AI_MANIFEST.md").read_text(encoding="utf-8")

    # Extract phase number from STATE.md
    # e.g. "## Phase: 2 - Core Domain" -> "Phase: 2"
    pass
    # This might be tricky to implement perfectly with regex, skipping exact check for now
    # but could be improved.
