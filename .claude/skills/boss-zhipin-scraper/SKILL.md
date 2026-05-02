---
name: boss-zhipin-scraper
description: Batch scrape BOSS直聘 job listings from search results into Excel. Extracts 13 fields per job including title, company, salary, experience, education, description, HR, location, benefits, company info, business registration, and URL. Use when user wants to collect job listings from BOSS直聘, batch scrape positions, or build a job database from zhipin.com.
---

# BOSS直聘 Job Scraper

Batch collects job listings from BOSS直聘 search results into Excel, with all 13 fields extracted from detail pages.

## Quick start

```
python3 .claude/skills/boss-zhipin-scraper/scripts/scrape.py \
    --query "数据标注师" \
    --city 101210600 \
    --count 20 \
    --output 职位详情.xlsx
```

## Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `--query` | Yes | URL-encoded search keyword | `%E6%95%B0%E6%8D%AE%E6%A0%87%E6%B3%A8%E5%B8%88` |
| `--city` | Yes | BOSS直聘 city code | `101210600` (台州) |
| `--count` | No | Number of jobs (default: 20) | `50` |
| `--output` | No | Excel output path (default: 职位详情.xlsx) | `jobs.xlsx` |

## Extracted fields

岗位名称, 公司名称, 薪资, 经验, 学历, 岗位描述, HR, 工作地点, 福利, 公司基本信息, 公司介绍, 工商信息, 网址

## Workflow

1. Opens Chrome and navigates to BOSS直聘 search results page
2. Scrolls to load enough job listings (at least `count` unique ones)
3. Collects all unique job detail page URLs
4. Visits each detail page, extracts 13 fields using DOM queries
5. Writes to Excel, skipping duplicates

## Requirements

- macOS with Google Chrome running
- Python 3 with `openpyxl` installed
- BOSS直聘 must be logged in (in Chrome)

## Notes

- BOSS直聘 uses custom font encoding for salaries on search results; detail pages render real numbers
- Rate limiting: ~4s per job (page load + extraction)
- Some fields (公司介绍, 工商信息) are only present for registered companies
- Individual postings may lack HR name and benefits
