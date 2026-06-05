Video Clipper Skill
一个用于视频剪辑和短视频制作的完整工作流工具集。

功能特性
🎬 媒体探测: 使用 FFmpeg 分析视频文件的时长、编码、分辨率、音轨等信息
✂️ 精准剪辑: 支持基于时间戳的精确视频切割
📋 剪辑计划: 支持 JSON 格式的剪辑计划文件，实现批量剪辑
📝 字幕烧录: 将 SRT 字幕文件嵌入到视频中
📱 社交导出: 支持多种社交平台格式（横屏、竖屏等）
🖼️ 帧提取: 用于视频分析的帧提取功能
快速开始
依赖
Python 3.7+
FFmpeg (需安装并配置到 PATH)
安装
# 克隆仓库
git clone https://github.com/Allenwlg519/video-clip.git
cd video-clip
使用示例
探测媒体信息

python scripts/probe_media.py --input source.mp4 --output media.json
切割单个片段

python scripts/cut_clips.py --input source.mp4 --start 12.5 --end 28.0 --output clip_01.mp4
从 JSON 计划批量切割

python scripts/cut_clips.py --input source.mp4 --plan clip_plan.json --output clips --concat short_01.mp4
烧录字幕

python scripts/burn_subtitles.py --input short_01.mp4 --srt captions.srt --output short_01_subtitled.mp4
导出社交格式

python scripts/export_social.py --input short_01.mp4 --format vertical --output short_01_vertical.mp4
提取分析帧

python scripts/extract_frames.py --input source.mp4 --output frames --fps 1
项目结构
video-clip/
├── agents/              # 代理配置
│   └── openai.yaml      # OpenAI 代理配置
├── references/          # 参考文档
│   ├── clip_plan_schema.json  # 剪辑计划 JSON 模式
│   └── ffmpeg_recipes.md      # FFmpeg 命令配方
├── scripts/             # 核心脚本
│   ├── burn_subtitles.py      # 字幕烧录
│   ├── cut_clips.py           # 视频切割
│   ├── export_social.py       # 社交格式导出
│   ├── extract_frames.py      # 帧提取
│   └── probe_media.py         # 媒体探测
├── SKILL.md             # Skill 描述文件
└── README.md            # 项目说明
剪辑计划格式
剪辑计划是一个 JSON 文件，定义了多个剪辑片段：

{
  "source": "source.mp4",
  "clips": [
    {
      "id": "clip_01",
      "start": 10.5,
      "end": 25.0,
      "label": "精彩片段1"
    },
    {
      "id": "clip_02",
      "start": 45.0,
      "end": 60.0,
      "label": "精彩片段2"
    }
  ]
}
许可证
MIT License
