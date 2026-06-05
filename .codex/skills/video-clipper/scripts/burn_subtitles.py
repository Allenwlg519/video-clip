#!/usr/bin/env python3
import argparse
import shutil
import subprocess
from pathlib import Path


def require_tool(name: str) -> None:
    if not shutil.which(name):
        raise SystemExit(f"Missing required tool: {name}")


def filter_path(path: Path) -> str:
    value = str(path.resolve()).replace("\\", "/")
    value = value.replace(":", r"\:")
    value = value.replace("'", r"\'")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Burn SRT subtitles into a video with FFmpeg.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--srt", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--font-size", type=int, default=28)
    parser.add_argument("--margin-v", type=int, default=48)
    args = parser.parse_args()

    require_tool("ffmpeg")
    input_path = Path(args.input)
    srt_path = Path(args.srt)
    output_path = Path(args.output)
    if not input_path.exists():
        raise SystemExit(f"Input does not exist: {input_path}")
    if not srt_path.exists():
        raise SystemExit(f"SRT does not exist: {srt_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    style = f"Fontsize={args.font_size},Outline=2,Shadow=1,MarginV={args.margin_v}"
    vf = f"subtitles='{filter_path(srt_path)}':force_style='{style}'"
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vf",
        vf,
        "-c:v",
        "libx264",
        "-crf",
        "18",
        "-preset",
        "medium",
        "-c:a",
        "copy",
        str(output_path),
    ]
    return subprocess.run(cmd).returncode


if __name__ == "__main__":
    raise SystemExit(main())
