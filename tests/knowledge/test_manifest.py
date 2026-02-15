from pathlib import Path

MANIFEST_REQUIRED_HEADERS = [
    "Vision",
    "Project Memory Stack",
    "Core Pillars",
    "Roadmap & Phases",
]


def get_manifest_content():
    manifest_path = Path("AI_MANIFEST.md")
    assert manifest_path.exists(), "AI_MANIFEST.md must exist at root"
    return manifest_path.read_text(encoding="utf-8")


def test_manifest_exists_and_not_empty():
    content = get_manifest_content()
    assert len(content) > 100, "AI_MANIFEST.md seems too short"


def test_manifest_required_headers():
    content = get_manifest_content()
    for header in MANIFEST_REQUIRED_HEADERS:
        assert f"## {header}" in content or f"# {header}" in content, (
            f"AI_MANIFEST.md missing required header: {header}"
        )


def test_manifest_phases_structure():
    content = get_manifest_content()
    assert "### Phase 1" in content, "Phase 1 missing"
    assert "### Phase 2" in content, "Phase 2 missing"
    assert "### Phase 3" in content, "Phase 3 missing"


def test_manifest_current_phase_marker():
    """Ensure at least one phase is marked as Current"""
    content = get_manifest_content()
    assert "(Current)" in content, "No phase marked as '(Current)' in AI_MANIFEST.md"
