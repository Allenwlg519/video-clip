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


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe media with ffprobe and write JSON metadata.")
    parser.add_argument("--input", required=True, help="Input media file")
    parser.add_argument("--output", help="Optional JSON output path")
    args = parser.parse_args()

    require_tool("ffprobe")
    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(f"Input does not exist: {input_path}")

    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(input_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode != 0:
        sys.stderr.write(result.stderr)
        return result.returncode

    data = json.loads(result.stdout)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
