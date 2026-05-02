# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目阶段

本项目正在从单一 BOSS直聘 MCP 服务器重构为**求职助手平台**。完整规划见 `TASK_PLAN.md`，实现时如有偏离需同步更新该文件。旧代码已 `git rm` 暂存但未提交。

## 当前可用

BOSS直聘采集脚本（macOS + Chrome）：

```bash
python3 .claude/skills/boss-zhipin-scraper/scripts/scrape.py \
    --query "数据标注师" --city 101210600 --count 20 --output 职位详情.xlsx
```

## 目标架构

| 层 | 技术 |
|---|---|
| 后端 | Python FastAPI + Celery + Redis |
| 前端 | Next.js |
| 数据 | PostgreSQL + pgvector + Redis + MinIO |
| AI | Claude API / GPT-4o / Whisper / Edge TTS |
| 自动化 | Playwright |

## 注意事项

- 每完成一个小功能点即 commit，message 用中文
- 实现方案如与 `TASK_PLAN.md` 有出入，需同步更新
