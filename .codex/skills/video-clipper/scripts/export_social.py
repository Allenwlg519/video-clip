#!/usr/bin/env python3
import argparse
import shutil
import subprocess
from pathlib import Path


TARGETS = {
    "vertical": ("1080", "1920"),
    "square": ("1080", "1080"),
    "horizontal": ("1920", "1080"),
}


def require_tool(name: str) -> None:
    if not shutil.which(name):
        raise SystemExit(f"Missing required tool: {name}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a video to 9:16, 1:1, or 16:9.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--format", choices=TARGETS.keys(), default="vertical")
    parser.add_argument("--mode", choices=["crop", "fit"], default="crop")
    parser.add_argument("--crf", type=int, default=18)
    args = parser.parse_args()

    require_tool("ffmpeg")
    width, height = TARGETS[args.format]
    if args.mode == "crop":
        vf = f"scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}"
    else:
        vf = f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black"

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        args.input,
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-crf",
        str(args.crf),
        "-preset",
        "medium",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        str(output),
    ]
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    raise SystemExit(main())
