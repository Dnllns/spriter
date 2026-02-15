import json
import re
from datetime import datetime
from pathlib import Path


def parse_phase_from_manifest():
    content = Path("AI_MANIFEST.md").read_text(encoding="utf-8")
    match = re.search(r"### Phase (\d+).*\(Current\)", content)
    if match:
        return match.group(1), match.group(0)
    return None, None


def parse_state_data():
    content = Path("docs/STATE.md").read_text(encoding="utf-8")

    # Phase
    phase_match = re.search(r"## Phase: (\d+).*\(In Progress\)", content)
    phase_num = phase_match.group(1) if phase_match else "unknown"

    # Pending Items
    pending_items = []
    lines = content.split("\n")
    in_pending = False
    for line in lines:
        if "### Pending" in line:
            in_pending = True
            continue
        if line.startswith("### "):  # Next section
            in_pending = False

        if in_pending and line.strip().startswith("- [ ]"):
            pending_items.append(line.replace("- [ ]", "").strip())

    # Next Steps
    next_steps = []
    in_next = False
    for line in lines:
        if "### Next Actionable Steps" in line:
            in_next = True
            continue
        if in_next and line.startswith("#"):
            break
        if in_next:
            stripped = line.strip()
            if not stripped:
                continue
            # Support bullets (- ) or numbered lists (1. , 2., etc)
            is_list_item = stripped.startswith("- ") or (
                len(stripped) > 2
                and stripped[0].isdigit()
                and stripped[1] in [".", ")"]
            )
            if is_list_item:
                next_steps.append(stripped)

    return phase_num, pending_items, next_steps


def get_latest_adr():
    adr_dir = Path("docs/adr")
    if not adr_dir.exists():
        return None
    adrs = sorted(adr_dir.glob("0*.md"))
    if not adrs:
        return None
    return adrs[-1].name


def generate():
    manifest_phase, manifest_line = parse_phase_from_manifest()
    state_phase, pending, next_steps = parse_state_data()
    latest_adr = get_latest_adr()

    snapshot = {
        "generated_at": datetime.now().isoformat(),
        "project": "Spriter",
        "vision": "Advanced Sprite Repository & Simulator (Clean Arch, Full Python)",
        "current_phase": {
            "manifest_phase": manifest_phase,
            "state_phase": state_phase,
            "consistent": manifest_phase == state_phase,
        },
        "knowledge_status": {
            "latest_adr": latest_adr,
            "pending_items_count": len(pending),
            "next_steps_count": len(next_steps),
        },
        "next_steps": next_steps,
        "pending_features": pending,
    }

    output_path = Path("knowledge_snapshot.json")
    output_path.write_text(json.dumps(snapshot, indent=2))
    print(f"Knowledge Snapshot generated at {output_path}")


if __name__ == "__main__":
    generate()
