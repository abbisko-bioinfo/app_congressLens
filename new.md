# CongressLens 数据导入 — API 方式

## 逻辑流程

```
创建 Congress → 创建 Session(s) → 创建 Presentation(s) + Authors
```

Session 挂在 Congress 下，Presentation 挂在 Session（或直接挂在 Congress）下，Authors 挂在 Presentation 下。

## API 端点一览

Base URL: `http://localhost:8000/api`

| 方法 | 端点 | 说明 |
|------|------|------|
| POST | `/conferences` | 创建 Congress |
| GET | `/conferences` | 列表（支持 acronym + year 查重） |
| POST | `/sessions` | 创建 Session |
| POST | `/presentations` | 创建 Presentation |

> 注：当前 Presentation POST 端点不处理 authors。实际导入建议用 `/import/conferences/{id}/presentations` 文件导入接口（会自动解析 authors），或者扩展 PresentationCreate schema 增加 authors 字段。

---

## 数据格式

### 1. Congress

```json
{
  "acronym": "AACR",
  "name": "AACR Annual Meeting 2026",
  "year": 2026,
  "location": "San Diego, CA",
  "start_date": "2026-04-17",
  "end_date": "2026-04-22",
  "timezone": "America/Los_Angeles",
  "website": "https://www.aacr.org",
  "description": "American Association for Cancer Research Annual Meeting 2026"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| acronym | string | **是** | 缩写，如 AACR、ASCO、ESMO |
| name | string | **是** | 全称 |
| year | int | **是** | 年份，用于去重 |
| location | string | 否 | 举办城市/地点 |
| start_date | date | 否 | 开始日期 YYYY-MM-DD |
| end_date | date | 否 | 结束日期 |
| timezone | string | 否 | 时区，如 America/Chicago |
| website | string | 否 | 官网 URL |
| description | string | 否 | 描述 |

---

### 2. Session

```json
{
  "conference_id": "550e8400-e29b-41d4-a716-446655440000",
  "source_session_id": "AACR2026-S01",
  "title": "Plenary Session: Next-Gen Immunotherapy",
  "session_type": "plenary",
  "track": "Immunology",
  "subtrack": "Checkpoint Inhibitors",
  "room": "Hall A",
  "start_time": "2026-04-18T08:00:00",
  "end_time": "2026-04-18T10:00:00",
  "timezone": "America/Los_Angeles",
  "description": "Keynote and invited talks on cutting-edge immunotherapy approaches",
  "is_on_demand": false
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| conference_id | UUID | **是** | 所属 Congress ID |
| source_session_id | string | 否 | 源系统 session 标识 |
| title | string | **是** | Session 标题 |
| session_type | string | 否 | 类型：plenary, oral, poster, educational 等 |
| track | string | 否 | 主赛道 |
| subtrack | string | 否 | 子赛道 |
| room | string | 否 | 会议厅/房间 |
| start_time | datetime | 否 | 开始时间 ISO 8601 |
| end_time | datetime | 否 | 结束时间 |
| timezone | string | 否 | 时区 |
| description | string | 否 | 描述 |
| is_on_demand | bool | 否 | 是否点播（默认 false） |

---

### 3. Presentation

```json
{
  "conference_id": "550e8400-e29b-41d4-a716-446655440000",
  "session_id": "660e8400-e29b-41d4-a716-446655440001",
  "source_presentation_id": "AACR2026-CT001",
  "source_content_id": "AACR2026-ABS-001",
  "title": "PD-L1 blockade combined with CAR-T in solid tumors: a phase II trial",
  "abstract_text": "Background: ... Methods: ... Results: ... Conclusion: ...",
  "abstract_html": "<p>Background: ...</p>",
  "presentation_number": "CT001",
  "abstract_number": "1234",
  "poster_board_number": "PB-12",
  "presentation_type": "oral",
  "activity": "Clinical Trials",
  "status": "presented",
  "position_in_session": 3,
  "start_time": "2026-04-18T09:30:00",
  "end_time": "2026-04-18T09:45:00",
  "timezone": "America/Los_Angeles",
  "presenter_name": "Jane Doe",
  "first_author_name": "Jane Doe",
  "author_block_html": "<p>Jane Doe<sup>1</sup>, John Smith<sup>2</sup></p>",
  "institution_block": "<p><sup>1</sup>Harvard Medical School, <sup>2</sup>Stanford University</p>",
  "disclosure_block_html": "<p>J. Doe: Consultancy fees from Pfizer</p>",
  "funding_sources": ["NIH R01-CA123456", "Pfizer"],
  "additional_funding_source": null,
  "doi": "10.1200/JCO.2026.12345",
  "journal_citation": "J Clin Oncol 44, 2026 (suppl 16; abstr 1234)",
  "clinical_trial_registry_number": "NCT01234567",
  "source_url": "https://www.abstractsonline.com/pp8/#!/AACR26/presentation/1234",
  "disclosure_url": null,
  "has_abstract": true,
  "has_slides": false,
  "has_posters": false,
  "has_videos": false,
  "summary_status": "none"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| conference_id | UUID | **是** | 所属 Congress |
| session_id | UUID | 否 | 所属 Session |
| source_presentation_id | string | 否 | 源系统 presentation ID |
| source_content_id | string | 否 | 源系统 content ID |
| title | string | **是** | 演讲/海报标题 |
| abstract_text | string | 否 | 纯文本摘要 |
| abstract_html | string | 否 | HTML 格式摘要 |
| presentation_number | string | 否 | 演讲编号 |
| abstract_number | string | 否 | 摘要编号 |
| poster_board_number | string | 否 | 海报板编号 |
| presentation_type | string | 否 | 类型：oral, poster, poster_presentation 等 |
| activity | string | 否 | 活动分类，如 "Clinical Trials" |
| status | string | 否 | 状态 |
| position_in_session | int | 否 | 在 session 中的顺序 |
| start_time | datetime | 否 | 开始时间 |
| end_time | datetime | 否 | 结束时间 |
| timezone | string | 否 | 时区 |
| presenter_name | string | 否 | 报告人姓名 |
| first_author_name | string | 否 | 第一作者姓名 |
| author_block_html | string | 否 | HTML 格式作者块 |
| institution_block | string | 否 | HTML 格式机构块 |
| disclosure_block_html | string | 否 | HTML 披露信息 |
| funding_sources | list[str] | 否 | 资助来源 |
| additional_funding_source | string | 否 | 额外资助 |
| doi | string | 否 | DOI |
| journal_citation | string | 否 | 期刊引用 |
| clinical_trial_registry_number | string | 否 | 临床试验注册号 |
| source_url | string | 否 | 源 URL |
| disclosure_url | string | 否 | 披露信息 URL |
| has_abstract | bool | 否 | 有摘要（默认 false） |
| has_slides | bool | 否 | 有幻灯片（默认 false） |
| has_posters | bool | 否 | 有海报（默认 false） |
| has_videos | bool | 否 | 有视频（默认 false） |
| summary_status | string | 否 | AI 摘要状态（默认 "none"） |

---

### 4. Author（嵌入 Presentation 导入）

```json
{
  "display_name": "Jane Doe",
  "normalized_name": "doe jane",
  "role": "presenter",
  "author_order": 1,
  "organization": "Harvard Medical School",
  "city": "Boston",
  "country": "United States",
  "is_first_author": true,
  "is_presenter": true,
  "source_author_id": "AACR2026-AU-001"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| display_name | string | **是** | 展示名 |
| normalized_name | string | 否 | 归一化名（小写，便于搜索） |
| role | string | 否 | 角色：presenter, author 等 |
| author_order | int | 否 | 作者排序 |
| organization | string | 否 | 所属机构/公司/单位 |
| city | string | 否 | 城市 |
| country | string | 否 | 国家 |
| is_first_author | bool | 否 | 是否第一作者（默认 false） |
| is_presenter | bool | 否 | 是否报告人（默认 false） |
| source_author_id | string | 否 | 源系统 author ID |

---

## 独立 Python 脚本

### 设计思路

脚本按三步走：

1. **upsert Congress** — 按 acronym + year 去重，存在则复用 ID，不存在则创建
2. **upsert Session** — 按 conference_id + source_session_id（或 title）去重
3. **创建 Presentation + Authors** — 调用带 authors 的导入接口

### 完整脚本

```python
#!/usr/bin/env python3
"""
CongressLens API 数据导入脚本

Usage:
    python import_congress.py --input congress_data.json --base-url http://localhost:8000/api

JSON 输入格式见文档末尾示例。
"""

import argparse
import json
import os
import sys
from datetime import date, datetime
from typing import Any
from uuid import UUID

import requests


class CongressLensAPI:
    """CongressLens REST API 客户端"""

    def __init__(self, base_url: str, token: str | None = None):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers["Content-Type"] = "application/json"
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    # ── Congress ────────────────────────────────────────────

    def list_conferences(self) -> list[dict]:
        r = self.session.get(f"{self.base_url}/conferences")
        r.raise_for_status()
        return r.json()["items"]

    def create_conference(self, data: dict) -> dict:
        r = self.session.post(f"{self.base_url}/conferences", json=data)
        r.raise_for_status()
        return r.json()

    def upsert_conference(self, data: dict) -> dict:
        """按 acronym + year 去重，存在则返回已有记录，否则创建"""
        existing = self.list_conferences()
        acronym = data.get("acronym", "")
        year = data.get("year")
        for item in existing:
            if item["acronym"] == acronym and item["year"] == year:
                print(f"  [skip] Congress {acronym}-{year} 已存在: {item['id']}")
                return item
        result = self.create_conference(data)
        print(f"  [created] Congress {acronym}-{year}: {result['id']}")
        return result

    # ── Session ──────────────────────────────────────────────

    def list_sessions(self, conference_id: str) -> list[dict]:
        r = self.session.get(
            f"{self.base_url}/sessions", params={"conference_id": conference_id}
        )
        r.raise_for_status()
        return r.json()["items"]

    def create_session(self, data: dict) -> dict:
        r = self.session.post(f"{self.base_url}/sessions", json=data)
        r.raise_for_status()
        return r.json()

    def upsert_session(self, conference_id: str, data: dict) -> dict:
        """按 conference_id + source_session_id / title 去重"""
        existing = self.list_sessions(conference_id)
        source_id = data.get("source_session_id")
        title = data.get("title", "")
        for item in existing:
            if source_id and item.get("source_session_id") == source_id:
                print(f"  [skip] Session 已存在: {item['id']} ({title})")
                return item
            if item.get("title") == title:
                print(f"  [skip] Session 已存在(title): {item['id']} ({title})")
                return item
        result = self.create_session(data)
        print(f"  [created] Session: {result['id']} ({title})")
        return result

    # ── Presentation ─────────────────────────────────────────

    def create_presentation(self, data: dict) -> dict:
        """创建 presentation（当前 API 不含 authors）"""
        r = self.session.post(f"{self.base_url}/presentations", json=data)
        r.raise_for_status()
        return r.json()

    # ── 批量导入（走文件接口，自动处理 session + authors）─────

    def import_presentations(
        self,
        conference_id: str,
        source: str,
        folder_path: str,
        max_files: int = 0,
        offset: int = 0,
    ) -> dict:
        r = self.session.post(
            f"{self.base_url}/import/conferences/{conference_id}/presentations",
            params={
                "source": source,
                "folder_path": folder_path,
                "max_files": max_files,
                "offset": offset,
            },
        )
        r.raise_for_status()
        return r.json()

    def import_sessions(
        self,
        conference_id: str,
        source: str,
        folder_path: str,
        max_files: int = 0,
        offset: int = 0,
    ) -> dict:
        r = self.session.post(
            f"{self.base_url}/import/conferences/{conference_id}/sessions",
            params={
                "source": source,
                "folder_path": folder_path,
                "max_files": max_files,
                "offset": offset,
            },
        )
        r.raise_for_status()
        return r.json()


# ── 序列化辅助 ────────────────────────────────────────────────

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)


# ── 主流程 ────────────────────────────────────────────────────

def import_via_rest(api: CongressLensAPI, input_data: dict) -> dict:
    """通过 REST API 逐条创建 Congress → Sessions → Presentations

    适用场景：少量数据、需要精确控制每条记录
    限制：当前 Presentation POST 不含 authors，authors 需要通过文件导入接口
    """
    result = {"conference_id": None, "session_ids": [], "presentation_ids": []}

    # Step 1: Congress
    congress = input_data["congress"]
    created_congress = api.upsert_conference(congress)
    conference_id = created_congress["id"]
    result["conference_id"] = conference_id

    # Step 2: Sessions
    for session_data in input_data.get("sessions", []):
        session_data["conference_id"] = conference_id
        created = api.upsert_session(conference_id, session_data)
        result["session_ids"].append(created["id"])

        # Step 3: Presentations (under this session)
        for pres_data in session_data.get("presentations", []):
            pres_data["conference_id"] = conference_id
            pres_data["session_id"] = created["id"]
            # authors 单独处理
            authors = pres_data.pop("authors", [])
            created_pres = api.create_presentation(pres_data)
            result["presentation_ids"].append(created_pres["id"])
            if authors:
                print(
                    f"    [warn] Authors not sent via REST (当前 API 不支持): "
                    f"{created_pres['id']} has {len(authors)} authors"
                )
            pres_data["authors"] = authors  # 恢复

    return result


def import_via_file(api: CongressLensAPI, input_data: dict) -> dict:
    """通过文件导入接口创建 Congress → 导入 Sessions → 导入 Presentations

    适用场景：批量数据、需要自动解析 authors
    需要服务器能访问 folder_path
    """
    result = {"conference_id": None}

    # Step 1: Congress
    congress = input_data["congress"]
    created_congress = api.upsert_conference(congress)
    conference_id = created_congress["id"]
    result["conference_id"] = conference_id

    source = input_data.get("source", "aacr")
    folder = input_data.get("folder_path", "")

    if not folder:
        print("[error] folder_path is required for file-based import")
        return result

    # Session 文件夹（AACR 有独立 session 文件）
    session_folder = input_data.get("session_folder_path")
    if session_folder:
        r = api.import_sessions(conference_id, source, session_folder)
        print(f"  [import] Sessions: {r}")

    # Presentation + Authors
    r = api.import_presentations(conference_id, source, folder)
    print(f"  [import] Presentations: {r}")

    return result


# ── CLI ───────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="CongressLens API 数据导入脚本"
    )
    parser.add_argument(
        "--input", "-i", required=True,
        help="JSON 输入文件路径"
    )
    parser.add_argument(
        "--base-url", default="http://localhost:8000/api",
        help="CongressLens API 根地址"
    )
    parser.add_argument(
        "--token", help="Bearer token（如需认证）"
    )
    parser.add_argument(
        "--mode", choices=["rest", "file"], default="file",
        help="导入模式: rest=逐条API创建, file=文件导入接口(默认)"
    )
    args = parser.parse_args()

    with open(args.input) as f:
        input_data = json.load(f)

    api = CongressLensAPI(args.base_url, args.token)

    print(f"=== CongressLens 数据导入 ===")
    print(f"Mode: {args.mode}")
    print(f"Congress: {input_data['congress'].get('acronym')}-{input_data['congress'].get('year')}")

    if args.mode == "rest":
        result = import_via_rest(api, input_data)
    else:
        result = import_via_file(api, input_data)

    print(f"\n=== 导入完成 ===")
    print(json.dumps(result, indent=2, cls=JSONEncoder))


if __name__ == "__main__":
    main()
```

---

## JSON 输入文件示例

### REST 模式输入 (`congress_data.json`)

```json
{
  "congress": {
    "acronym": "AACR",
    "name": "AACR Annual Meeting 2026",
    "year": 2026,
    "location": "San Diego, CA",
    "start_date": "2026-04-17",
    "end_date": "2026-04-22",
    "timezone": "America/Los_Angeles",
    "description": "American Association for Cancer Research 2026"
  },
  "sessions": [
    {
      "source_session_id": "AACR2026-PL",
      "title": "Plenary Session: Advances in Cancer Immunotherapy",
      "session_type": "plenary",
      "track": "Immunology",
      "start_time": "2026-04-18T08:00:00",
      "end_time": "2026-04-18T10:00:00",
      "room": "Hall A",
      "presentations": [
        {
          "source_presentation_id": "CT001",
          "title": "PD-L1 + CAR-T in solid tumors",
          "presentation_type": "oral",
          "presentation_number": "CT001",
          "abstract_text": "Background: ...",
          "presenter_name": "Jane Doe",
          "first_author_name": "Jane Doe",
          "authors": [
            {
              "display_name": "Jane Doe",
              "role": "presenter",
              "author_order": 1,
              "organization": "Harvard Medical School",
              "is_first_author": true,
              "is_presenter": true
            },
            {
              "display_name": "John Smith",
              "author_order": 2,
              "organization": "Stanford University",
              "is_first_author": false,
              "is_presenter": false
            }
          ]
        }
      ]
    }
  ]
}
```

### 文件导入模式输入

```json
{
  "congress": {
    "acronym": "AACR",
    "name": "AACR Annual Meeting 2026",
    "year": 2026,
    "location": "San Diego, CA",
    "start_date": "2026-04-17",
    "end_date": "2026-04-22",
    "timezone": "America/Los_Angeles"
  },
  "source": "aacr",
  "folder_path": "/data/attachmentFiles/AACR-2026",
  "session_folder_path": "/data/attachmentFiles/AACR-2026/session"
}
```

---

## 执行示例

```bash
# REST 逐条模式（精确控制，适合小批量）
python import_congress.py --input congress_data.json --mode rest

# 文件导入模式（批量，自动解析 authors + sessions）
python import_congress.py \
  --input congress_batch.json \
  --base-url http://localhost:8000/api \
  --mode file
```

---

## 当前限制与建议

1. **REST API 不支持 author 创建**：`POST /api/presentations` 只创建 Presentation 本身，不创建 PresentationAuthor。文件导入接口 (`POST /api/import/conferences/{id}/presentations`) 则完整处理了 authors + sessions。

2. **建议扩展 PresentationCreate**：在 schema 中增加 `authors: list[AuthorCreate] | None = None` 字段，在 `create_presentation` 端点中循环创建 PresentationAuthor 记录，这样 REST 模式也能完整导入。

3. **去重策略**：Congress 按 acronym+year 去重，Session 按 source_session_id 或 title 去重，Presentation 按 source_presentation_id 去重（当前未实现，可扩展）。
