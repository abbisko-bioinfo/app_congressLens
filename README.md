# Conference Scraper

从 [abstractsonline.com](https://www.abstractsonline.com/) 抓取学术会议（AACR、ASCO 等）的 presentation 和 session 信息，输出为 Excel 文件。

## 支持的会议

- AACR 2025 / 2026
- ASCO 2026

## 数据获取流程

1. **获取 presentation ID 列表** — 从会议日程 API 分页抓取所有 presentation ID
2. **获取 presentation 详情** — 逐个 ID 请求摘要、作者、摘要等信息
3. **获取 session 信息** — 根据 presentation 关联的 session ID 获取会场、类型、主题等信息
4. **合并输出** — 清理 HTML 标签，合并 presentation 和 session 数据，导出 Excel

## 使用方式

每个会议对应一个 Jupyter notebook（如 `AACR-2026.ipynb`），按顺序执行单元格即可。

### 认证

AACR 网站需要 `backpack`  header 验证真实用户。获取方式：

1. 浏览器打开会议网站并登录
2. 打开开发者工具 → Network → 找到任意 API 请求的 Headers
3. 复制 `backpack` 值，更新 notebook 中对应变量

> backpack 有效期约 1 天，长时间运行需关注是否过期。

### 日程 URL

不同日程对应的 API URL 没有规律，需要在浏览器开发者模式中手动获取 JSON 数据交换 URL。

## 输出

最终输出为 Excel 文件（如 `AACR_2026.xlsx`），包含：
- Presentation 信息（标题、摘要、作者、控制编号等）
- Session 信息（会场、日期、主题分类、类型等）
- 在线链接（presentation URL、session URL）

## 依赖

- Python 3
- requests
- pandas
- beautifulsoup4
- openpyxl
- tqdm
- jupyter
