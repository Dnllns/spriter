import io
import json
import math
import random

import requests
from PIL import Image, ImageDraw

BASE_URL = "http://localhost:8000/api/v1"
AUTH_HEADERS = {"Authorization": "Bearer test-user"}


def generate_procedural_sprite(width=128, height=128, frames=10, frame_size=32):
    """Generates a procedural 'amorphous' spritesheet."""
    # Create a sheet large enough for the frames
    cols = 5
    rows = (frames + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * frame_size, rows * frame_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sheet)

    for i in range(frames):
        col = i % cols
        row = i // cols
        left = col * frame_size
        top = row * frame_size

        # Center of the frame
        cx = left + frame_size // 2
        cy = top + frame_size // 2

        # Draw some 'mathematical/amorphous' shape
        color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255),
            255,
        )

        # Draw a wobbling circle/blob
        points = []
        num_points = 8
        radius = frame_size // 3
        for p in range(num_points):
            angle = (p / num_points) * 2 * math.pi
            # Add some wobble based on frame index
            offset = math.sin(angle * 3 + i * 0.5) * 5
            px = cx + (radius + offset) * math.cos(angle)
            py = cy + (radius + offset) * math.sin(angle)
            points.append((px, py))

        draw.polygon(points, fill=color, outline=(255, 255, 255, 255))

        # Add a moving 'nucleus'
        nx = cx + math.cos(i * 0.8) * 5
        ny = cy + math.sin(i * 0.8) * 5
        draw.ellipse([nx - 2, ny - 2, nx + 2, ny + 2], fill="white")

    img_byte_arr = io.BytesIO()
    sheet.save(img_byte_arr, format="PNG")
    return img_byte_arr.getvalue()


ASSETS = [
    {
        "name": "Procedural Blob Alpha",
        "description": (
            "A mathematically generated wobbling blob for testing storage slicing."
        ),
        "tags": ["Procedural", "Mathematical", "Test"],
        "frame_w": 32,
        "frame_h": 32,
        "frames": 12,
    },
    {
        "name": "Geometric Pulsar",
        "description": "An amorphous geometric shape that pulses across frames.",
        "tags": ["Amorphous", "Geometry", "Test"],
        "frame_w": 64,
        "frame_h": 64,
        "frames": 8,
    },
    {
        "name": "Fractal Fern Fragment",
        "description": (
            "A recursive fractal-like structure generated with L-system logic."
        ),
        "tags": ["Fractal", "Math", "Recursive"],
        "frame_w": 48,
        "frame_h": 48,
        "frames": 15,
    },
    {
        "name": "Matrix Rain Ripple",
        "description": "Sequential vertical patterns simulating mathematical cascade.",
        "tags": ["Grid", "Pattern", "Matrix"],
        "frame_w": 32,
        "frame_h": 64,
        "frames": 10,
    },
    {
        "name": "Orbital Vortex",
        "description": "Spinning particles following a strange attractor formula.",
        "tags": ["Physics", "Simulation", "Vortex"],
        "frame_w": 64,
        "frame_h": 64,
        "frames": 20,
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

    # 2. Generate Procedural Image
    img_content = generate_procedural_sprite(
        frames=asset["frames"], frame_size=asset["frame_w"]
    )

    # 3. Upload Version
    animations = [
        {
            "name": "main_loop",
            "fps": 8,
            "frames": [
                {
                    "index": i,
                    "x": (i % 5) * asset["frame_w"],
                    "y": (i // 5) * asset["frame_h"],
                    "w": asset["frame_w"],
                    "h": asset["frame_h"],
                }
                for i in range(asset["frames"])
            ],
            "loop": True,
        }
    ]

    files = {"file": ("procedural.png", img_content, "image/png")}
    data = {
        "metadata": json.dumps(
            {"frame_w": asset["frame_w"], "frame_h": asset["frame_h"]}
        ),
        "animations": json.dumps(animations),
        "changelog": "Generated procedural testing sprite",
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
    for asset in ASSETS:
        try:
            register_asset(asset)
        except Exception as e:
            print(f"Error: {e}")
