#!/usr/bin/env python3
import argparse
import shutil
import subprocess
from pathlib import Path


def require_tool(name: str) -> None:
    if not shutil.which(name):
        raise SystemExit(f"Missing required tool: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract frames for visual video analysis.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--fps", type=float, default=1.0)
    parser.add_argument("--width", type=int, default=640)
    args = parser.parse_args()

    require_tool("ffmpeg")
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    pattern = str(out_dir / "frame_%06d.jpg")
    vf = f"fps={args.fps},scale={args.width}:-1"
    cmd = ["ffmpeg", "-y", "-i", args.input, "-vf", vf, "-q:v", "3", pattern]
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    raise SystemExit(main())
