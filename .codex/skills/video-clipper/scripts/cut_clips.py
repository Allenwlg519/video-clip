#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


def require_tool(name: str) -> None:
    if not shutil.which(name):
        raise SystemExit(f"Missing required tool: {name}")


def run(cmd: list[str]) -> None:
    result = subprocess.run(cmd, text=True)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def safe_id(value: str, fallback: str) -> str:
    allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-"
    cleaned = "".join(ch if ch in allowed else "_" for ch in value).strip("_")
    return cleaned or fallback


def cut_clip(source: Path, start: float, end: float, output: Path, crf: int) -> None:
    if end <= start:
        raise ValueError(f"Clip end must be greater than start: {start}-{end}")
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        str(start),
        "-to",
        str(end),
        "-i",
        str(source),
        "-map",
        "0",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-crf",
        str(crf),
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-movflags",
        "+faststart",
        str(output),
    ]
    run(cmd)


def load_plan(path: Path) -> tuple[Path | None, list[dict]]:
    plan = json.loads(path.read_text(encoding="utf-8"))
    source = Path(plan["source"]) if plan.get("source") else None
    return source, plan.get("clips", [])


def concat_clips(clips: list[Path], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    list_path = output.with_suffix(".concat.txt")
    lines = []
    for clip in clips:
        escaped = str(clip.resolve()).replace("'", "'\\''")
        lines.append(f"file '{escaped}'")
    list_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    try:
        run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_path), "-c", "copy", str(output)])
    finally:
        list_path.unlink(missing_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser(description="Cut one clip or all clips from a JSON plan.")
    parser.add_argument("--input", help="Source video. Overrides source in --plan when both are provided.")
    parser.add_argument("--start", type=float, help="Single clip start time in seconds")
    parser.add_argument("--end", type=float, help="Single clip end time in seconds")
    parser.add_argument("--plan", help="Clip plan JSON with source and clips")
    parser.add_argument("--output", required=True, help="Output file for one clip, or output directory for a plan")
    parser.add_argument("--concat", help="Optional assembled output video when using --plan")
    parser.add_argument("--crf", type=int, default=18, help="H.264 CRF quality; lower is higher quality")
    args = parser.parse_args()

    require_tool("ffmpeg")
    rendered: list[Path] = []

    if args.plan:
        plan_source, clips = load_plan(Path(args.plan))
        source = Path(args.input) if args.input else plan_source
        if source is None:
            raise SystemExit("No source video provided in --input or plan.source")
        out_dir = Path(args.output)
        for index, clip in enumerate(clips, start=1):
            clip_id = safe_id(str(clip.get("id", "")), f"clip_{index:02d}")
            out = out_dir / f"{clip_id}.mp4"
            cut_clip(source, float(clip["start"]), float(clip["end"]), out, args.crf)
            rendered.append(out)
            print(f"Rendered {out}")
        if args.concat:
            concat_clips(rendered, Path(args.concat))
            print(f"Assembled {args.concat}")
        return 0

    if not args.input or args.start is None or args.end is None:
        raise SystemExit("For a single clip, provide --input --start --end --output")
    cut_clip(Path(args.input), args.start, args.end, Path(args.output), args.crf)
    print(f"Rendered {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
