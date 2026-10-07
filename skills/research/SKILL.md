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

若環境支援 subagent，可將 reading legwork 交給 research subagent；不支援時就在目前 session 完成，不把 background 當必要條件。

## Output

- Question
- Short answer
- Confirmed facts
- Version / platform scope
- Implications for current design / implementation
- Unknown / ambiguous points
- Sources

Research 不自行做 architecture decision；它提供 evidence 給 design / prototype / implement。

## Completion criterion

主要結論都能追溯到 authoritative source；版本敏感 claim 有明確 scope；剩餘 unknown 不被假裝成 fact。
