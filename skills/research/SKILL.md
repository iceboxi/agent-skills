---
name: research
description: Investigate an external technical question against primary sources and return a cited decision-ready note. Use for platform, framework, SDK, language, toolchain, protocol, or vendor facts that repository code cannot establish.
---

# Research

本 skill 處理 repository 外部的 technical facts。

explore 回答「我們的 code 現在怎麼做」；research 回答「platform / SDK / spec / toolchain 真正怎麼規定」。

## Source priority

優先：

1. official documentation / specification
2. official source code / release notes / migration guide
3. first-party issue / engineering note
4. 高品質 secondary source，只用於補充脈絡，不用來取代 authoritative claim

對會改變 architecture、compatibility 或 implementation feasibility 的 claim，應能回到 primary source。

## Process

1. 定義 bounded research question。
2. 確認它不是 repository fact；若是，交 explore。
3. 查 primary sources，記錄版本 / date / platform constraints。
4. 對相互衝突或版本敏感的資料做 reconciliation。
5. 將結果整理成 decision-ready note，而不是 dump links。
6. 若 research 會被後續 design / wayfinder / implementation 引用，保存成 durable Markdown artifact；沿用 project research convention，沒有時預設 `.scratch/research/<slug>.md`。純即時查詢、不會被後續引用時可只回目前 session。

若環境支援 subagent，可將 reading legwork 交給 research subagent；不支援時就在目前 session 完成，不把 background 當必要條件。

## Output

Durable artifact（需要時）應包含：

- Question
- Short answer
- Confirmed facts
- Version / platform scope
- Implications for current design / implementation
- Unknown / ambiguous points
- Sources

Research 不自行做 architecture decision；它提供 evidence 給 design / prototype / implement。後續 artifact 應以 path / URL pointer 引用 research note，不要把全文複製進 Design Doc / handoff。

## Completion criterion

主要結論都能追溯到 authoritative source；版本敏感 claim 有明確 scope；剩餘 unknown 不被假裝成 fact；需要跨 phase 使用的 research 有 durable pointer。
