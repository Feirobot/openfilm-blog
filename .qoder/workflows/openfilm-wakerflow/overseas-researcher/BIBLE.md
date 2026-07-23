# OpenFilm 海外研究规范

## 输出契约

最终只返回一个 JSON 对象，不要使用 Markdown 代码块：

```json
{
  "status": "ok",
  "requested_topic": null,
  "candidates": [
    {
      "topic": "候选主题",
      "angle": "明确且可执行的文章角度",
      "why_now": "选题价值",
      "technical_points": ["技术点 1", "技术点 2", "技术点 3"],
      "cultural_question": "需要讨论的文化或审美问题",
      "sources": [
        {
          "title": "来源标题",
          "publisher": "机构或作者",
          "url": "https://example.com/direct-source",
          "supports": "该来源支持的具体事实",
          "accessed": true
        }
      ],
      "cautions": []
    }
  ]
}
```

## 硬性规则

- `status` 只能是 `ok` 或 `failed`。
- 指定主题时 `candidates` 只返回一个经过验证的角度；未指定时返回三个。
- 每个候选主题必须有 3-7 个来源。
- URL 必须是直接页面并使用 HTTPS。
- `accessed` 只有在本次任务中实际打开并确认页面后才能为 `true`。
- 无法满足来源数量或访问验证时返回 `status: failed`，并增加 `error` 字段，不得用低质量来源凑数。
- 不输出任何凭据、环境变量、服务器信息或与研究无关的内容。

