---
name: improve-codebase-architecture
description: Survey a codebase for deepening opportunities, present candidates in a visual HTML report, then grill through the candidate the user selects. Use for periodic architecture health, brownfield audits, or to make an upcoming change easier.
---

# Improve Codebase Architecture

這是 architecture **survey**，不是 refactor executor。它找值得投資的 deepening opportunities，先讓人比較，再對選中的 candidate 做 grilling；本 skill 不修改 production code。

開始前讀：

- [codebase-design](../codebase-design/SKILL.md)
- 若存在：GLOSSARY.md / GLOSSARY-MAP.md
- relevant ADRs

## 1. Scope the scan

YAGNI：先決定看哪裡。

- 使用者指定 subsystem / pain point / upcoming spec → 以該 scope 為主。
- 沒有方向 → 看近期 git history / change hotspots，優先掃真正會繼續變動的區域。
- Brownfield audit 才逐步擴大範圍。

探索時找：

- shallow module：interface 幾乎跟 implementation 一樣複雜；
- understanding 一個 concept 要跳很多 files；
- locality 差：logical change 散在多個 callers；
- seam leakage / bypass；
- 為 test 抽 pure helper，但真正 integration behavior 沒有 stable seam；
- tests 很難經 module interface 驗證。

對 candidate 套 deletion test：刪掉這層後，complexity 是集中到一個更深的 module，還是只是散回 callers？只有後者真的顯示它可能在賺取 depth。

## 2. Visual HTML report

**先出 report，再問使用者選哪個 candidate。不要先 grill 第一個建議。**

寫一份 self-contained HTML 到 OS temp directory，例如：

architecture-review-<timestamp>.html

實際開啟 / render 檢查。

每個 candidate 至少有：

- Domain / files involved
- Current friction
- Proposed deepening direction（plain English，不先鎖 exact interface）
- Locality / leverage payoff
- Testability implication
- Before / After visual
- Recommendation strength：
  - Strong
  - Worth exploring
  - Speculative
- ADR conflict / reopen warning（若 relevant）

Report 最後給 Top recommendation，但不自動選。

若所有 candidate 都只能列 Speculative，可以結論「目前沒有明顯值得投資的 deepening」。

Visual 應能看出 ownership / call concentration / seam，不只是裝飾。可用 inline CSS/SVG、Mermaid 或現有 renderer；優先可靠可開啟，不把 CDN 當必要條件。

## 3. User chooses candidate

Report 完成後停止，請使用者選 candidate。

選定後才開始：

- [grilling](../grilling/SKILL.md)
- [domain-modeling](../domain-modeling/SKILL.md)

Grilling 聚焦：

- constraints / non-goals
- candidate 是否真的值得做
- deepened module 的 responsibility
- seam location
- what complexity moves behind it
- which callers become simpler
- which tests should survive
- migration / compatibility implications
- alternative interface shape（需要時用 codebase-design design-it-twice discipline）

若使用者拒絕 candidate 且理由是 durable / surprising / real trade-off，才考慮 ADR，避免下次 survey 重提同一件事。

## Handoff

這個 skill 的輸出是 **architecture idea + settled candidate decisions**，不是 diff。

後續：

- candidate 可在一個 coherent design 裡完成 → grill-with-docs / design
- candidate 屬於超大型 foggy effort → wayfinder
- 只是想保留 survey，不做任何 refactor → 到此停止

## Completion criterion

成功的 run：

- report 真的提供多個可比較 candidate 或誠實說沒有；
- user 在 report 後才選方向；
- grilling 只針對選中的 candidate；
- domain language / ADR 按需要更新；
- production code 沒有改；
- 下一步能清楚交給 design / wayfinder，而不是直接跳 implementation。
