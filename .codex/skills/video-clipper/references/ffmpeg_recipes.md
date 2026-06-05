# FFmpeg Recipes

Use these only after confirming concrete paths and timestamps.

## Probe

```bash
ffprobe -v error -print_format json -show_format -show_streams input.mp4
```

## Accurate Clip

```bash
ffmpeg -y -ss 12.5 -to 28.0 -i input.mp4 -map 0 -c:v libx264 -preset medium -crf 18 -c:a aac -b:a 192k clip_01.mp4
```

## Concat Re-encoded Clips

Create a UTF-8 text file:

```text
file '/absolute/path/clip_01.mp4'
file '/absolute/path/clip_02.mp4'
```

Then run:

```bash
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy short_01.mp4
```

## 9:16 Center Crop

```bash
ffmpeg -y -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" -c:v libx264 -crf 18 -preset medium -c:a aac output_vertical.mp4
```

## 9:16 Fit With Padding

```bash
ffmpeg -y -i input.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black" -c:v libx264 -crf 18 -preset medium -c:a aac output_vertical_fit.mp4
```
