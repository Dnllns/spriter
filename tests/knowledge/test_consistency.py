import re
from pathlib import Path


def parse_manifest_phase(content):
    match = re.search(r"### Phase (\d+).*\(Current\)", content)
    if match:
        return match.group(1)
    return None


def parse_state_phase(content):
    match = re.search(r"## Phase: (\d+).*\(In Progress\)", content)
    if match:
        return match.group(1)
    return None


def test_semantic_consistency():
    manifest = Path("AI_MANIFEST.md").read_text(encoding="utf-8")
    state = Path("docs/STATE.md").read_text(encoding="utf-8")

    m_phase = parse_manifest_phase(manifest)
    s_phase = parse_state_phase(state)

    assert m_phase is not None, "AI_MANIFEST.md has no Current Phase"
    assert s_phase is not None, "docs/STATE.md has no Phase In Progress"
    assert m_phase == s_phase, (
        f"Phase mismatch: Manifest says {m_phase}, State says {s_phase}"
    )


def test_next_steps_references():
    """Ensure Next Steps contain actionable references (files, ADRs, tasks)."""
    state_content = Path("docs/STATE.md").read_text(encoding="utf-8")

    # Extract Next Steps section
    next_steps_section = re.search(
        r"### Next Actionable Steps\n(.+?)($|\n#)", state_content, re.DOTALL
    )
    assert next_steps_section, "Next Steps section missing"

    content = next_steps_section.group(1).strip()
    assert len(content) > 10, "Next steps description too short"

    # Basic heuristic: should contain code formatting `like this` or links [like this]
    # referencing artifacts.
    has_ref = "`" in content or "[" in content
    assert has_ref, (
        "Next steps should reference specific files/concepts using `code` or [links]."
    )
