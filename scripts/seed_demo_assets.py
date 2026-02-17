import requests
import json
import uuid

BASE_URL = "http://localhost:8000/api/v1"
AUTH_HEADERS = {"Authorization": "Bearer test-user"}

ASSETS = [
    {
        "name": "Kenney Pixel Characters",
        "description": "The classic characters from Kenney's Pixel Platformer pack.",
        "tags": ["Character", "Kenney", "PixelArt"],
        "url": "https://raw.githubusercontent.com/uheartbeast/Pixel-Platformer/master/characters_packed.png",
        "frame_w": 24,  # Pixel Platformer characters are often 24x24 or 18x18. Let's try 24 based on common knowledge of this specific repo.
        "frame_h": 24,
    },
    {
        "name": "Kenney Tiny Dungeon",
        "description": "Tiles and characters from the Tiny Dungeon set.",
        "tags": ["Environment", "Kenney", "TinyDungeon"],
        "url": "https://raw.githubusercontent.com/cassidoo/thirteen-potions/main/tilemap_packed.png",
        "frame_w": 16,  # Tiny Dungeon is 16x16
        "frame_h": 16,
    },
]


def register_asset(asset):
    print(f"Registering {asset['name']}...")

    # 1. Create Sprite
    create_payload = {
        "name": asset["name"],
        "description": asset["description"],
        "tags": asset["tags"],
    }
    resp = requests.post(
        f"{BASE_URL}/sprites", json=create_payload, headers=AUTH_HEADERS
    )
    if resp.status_code != 201:
        print(f"Failed to create sprite: {resp.text}")
        return

    sprite_id = resp.json()["id"]
    print(f"Created sprite {sprite_id}")

    # 2. Download Image
    img_resp = requests.get(asset["url"])
    if img_resp.status_code != 202 and img_resp.status_code != 200:
        print(f"Failed to download image: {img_resp.status_code}")
        return

    # 3. Upload Version
    # Mock some animations
    animations = [
        {
            "name": "all_frames",
            "fps": 5,
            "frames": [
                {
                    "index": i,
                    "x": (i % 5) * asset["frame_w"],
                    "y": (i // 5) * asset["frame_h"],
                    "w": asset["frame_w"],
                    "h": asset["frame_h"],
                }
                for i in range(10)  # first 10 frames
            ],
            "loop": True,
        }
    ]

    files = {"file": ("sheet.png", img_resp.content, "image/png")}
    data = {
        "metadata": json.dumps(
            {"frame_w": asset["frame_w"], "frame_h": asset["frame_h"]}
        ),
        "animations": json.dumps(animations),
        "changelog": "Initial import from Kenney Assets",
    }

    upload_resp = requests.post(
        f"{BASE_URL}/sprites/{sprite_id}/versions",
        files=files,
        data=data,
        headers=AUTH_HEADERS,
    )
    if upload_resp.status_code == 201:
        print(f"Successfully uploaded version for {asset['name']}")
    else:
        print(f"Failed to upload version: {upload_resp.text}")


if __name__ == "__main__":
    # Ensure server is running or we assume it is for this task context
    for asset in ASSETS:
        try:
            register_asset(asset)
        except Exception as e:
            print(f"Error: {e}")
