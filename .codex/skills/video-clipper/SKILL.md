---
name: video-clipper
description: End-to-end video clipping and short-video editing workflow. Use when Codex needs to analyze source videos, design a clip plan, cut highlights, assemble short videos, burn subtitles, crop for social platforms, export FFmpeg commands, or produce executable editing artifacts from MP4/MOV/MKV/AVI media.
---

# Video Clipper

## Overview

Create practical video edits from raw footage or long-form videos. Prefer explicit clip plans, deterministic FFmpeg scripts, and verification over vague "AI editing" promises.

## Workflow

1. Clarify the deliverable: target platform, aspect ratio, duration, language/subtitles, whether to output a plan only or render files.
2. Probe the media with `scripts/probe_media.py` or `ffprobe`; record duration, codecs, resolution, audio tracks, and rotation.
3. Analyze candidate moments with scene boundaries, transcripts, user-provided timestamps, or visual frame samples.
4. Produce a JSON clip plan before rendering unless the user already supplied exact timestamps.
5. Render clips with `scripts/cut_clips.py`, then review duration, audio, and first/last frames when quality matters.
6. Add subtitles or platform formatting only after the base edit is correct.
7. Put final user-facing outputs in the requested directory, or in the project outputs folder if no destination is given.

## Clip Planning Rules

- Treat a clip as the smallest editing unit. Keep each clip under 30 seconds unless the user explicitly asks for longer continuity.
- Compose one short video from 3-8 clips when creating plot recaps, highlight reels, or social cuts.
- Place cut points on scene changes, emotional turns, speaker turns, pauses, applause, beats, or action completion.
- Avoid cutting inside a sentence unless the goal is a punchy social teaser.
- Prefer a coherent beginning, escalation, payoff, and clean ending over raw "highest score" moments.
- When using copyrighted source material, help the user create transformative summaries, commentary, or personal edits; do not promise rights clearance.

Use `references/clip_plan_schema.json` for structured plans. Include executable commands only after paths and timestamps are concrete.

## Script Quick Start

Probe media:

```bash
python scripts/probe_media.py --input source.mp4 --output media.json
```

Cut one clip:

```bash
python scripts/cut_clips.py --input source.mp4 --start 12.5 --end 28.0 --output clip_01.mp4
```

Cut from a JSON plan:

```bash
python scripts/cut_clips.py --input source.mp4 --plan clip_plan.json --output clips --concat short_01.mp4
```

Burn SRT subtitles:

```bash
python scripts/burn_subtitles.py --input short_01.mp4 --srt captions.srt --output short_01_subtitled.mp4
```

Export social formats:

```bash
python scripts/export_social.py --input short_01.mp4 --format vertical --output short_01_vertical.mp4
```

Extract analysis frames:

```bash
python scripts/extract_frames.py --input source.mp4 --output frames --fps 1
```

## Output Standards

- Deliver `clip_plan.json` plus rendered videos when possible.
- Name clips with stable IDs: `clip_01.mp4`, `clip_02.mp4`, `short_01.mp4`.
- Report exact source path, output path, timestamps, duration, aspect ratio, and any skipped step.
- Verify rendered files with `ffprobe` before saying the edit is complete.

## Troubleshooting

- If `ffmpeg` or `ffprobe` is missing, stop and tell the user what must be installed.
- If paths contain spaces or non-ASCII characters, pass arguments as arrays in scripts rather than shell-concatenated strings.
- If audio drifts after concatenation, re-encode clips with the same frame rate, audio sample rate, and codecs.
- If subtitle paths fail on Windows, use the provided `burn_subtitles.py`; it escapes paths for FFmpeg filters.
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Codex for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Codex's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Codex should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Codex produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
