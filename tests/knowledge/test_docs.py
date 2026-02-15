import pytest
from pathlib import Path


def test_development_rules_not_empty():
    path = Path("docs/DEVELOPMENT_RULES.md")
    assert path.exists(), "docs/DEVELOPMENT_RULES.md missing"
    assert "Clean Architecture" in path.read_text(encoding="utf-8"), (
        "Missing Clean Architecture rule"
    )
    assert "Test Coverage" in path.read_text(encoding="utf-8"), "Missing Testing rules"


def test_adr_existence():
    """Ensure docs/adr/ exists and has >= 1 ADR"""
    adr_path = Path("docs/adr")
    assert adr_path.exists(), "docs/adr directory must exist"

    # Check for index
    index = adr_path / "README.md"
    assert index.exists(), "docs/adr/README.md required as index"

    # Check for at least two functional ADRs (Meta-ADR + Clean Architecture)
    files = list(adr_path.glob("0*.md"))
    assert len(files) >= 2, "Should have at least 2 recorded ADRs"


def test_contributing_basics():
    path = Path("docs/CONTRIBUTING.md")
    assert path.exists(), "docs/CONTRIBUTING.md missing"
    assert "Conventional Commits" in path.read_text(encoding="utf-8")
    assert "Memory Stack" in path.read_text(encoding="utf-8"), (
        "CONTRIBUTING.md must mention Memory Stack"
    )
