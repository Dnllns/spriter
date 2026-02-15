import pytest
from pathlib import Path
import re

VALID_ADR_STATUSES = ["Accepted", "Proposed", "Superseded", "Deprecated", "Rejected"]


def test_development_rules_not_empty():
    path = Path("docs/DEVELOPMENT_RULES.md")
    assert path.exists(), "docs/DEVELOPMENT_RULES.md missing"
    assert "Clean Architecture" in path.read_text(encoding="utf-8"), (
        "Missing Clean Architecture rule"
    )
    assert "Test Coverage" in path.read_text(encoding="utf-8"), "Missing Testing rules"


def test_adr_compliance():
    """
    Validates ADR Decision Status Lifecycle.
    Each ADR must have a Status section with a valid value.
    """
    adr_dir = Path("docs/adr")
    assert adr_dir.exists(), "docs/adr directory must exist"

    # Check for index
    index = adr_dir / "README.md"
    assert index.exists(), "docs/adr/README.md required as index"

    files = list(adr_dir.glob("0*.md"))
    assert len(files) >= 2, "Should have at least 2 recorded ADRs"

    for adr_file in files:
        content = adr_file.read_text(encoding="utf-8")
        # Check Status Header
        match = re.search(r"## Status\s*\n\s*(\w+)", content)
        assert match, f"ADR {adr_file.name} missing '## Status' section"

        status = match.group(1)
        assert status in VALID_ADR_STATUSES, (
            f"ADR {adr_file.name} has invalid status '{status}'. Must be one of {VALID_ADR_STATUSES}"
        )


def test_contributing_basics():
    path = Path("docs/CONTRIBUTING.md")
    assert path.exists(), "docs/CONTRIBUTING.md missing"
    assert "Conventional Commits" in path.read_text(encoding="utf-8")
    assert "Memory Stack" in path.read_text(encoding="utf-8"), (
        "CONTRIBUTING.md must mention Memory Stack"
    )
