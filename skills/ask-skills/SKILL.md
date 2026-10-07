---
name: ask-skills
description: Route a software-engineering task to the smallest useful skill or workflow. Inspect the actual candidate SKILL.md files before recommending; explain the phase, why the chosen skill fits, and why adjacent skills do not.
---

# Ask Skills

當 skill 數量多到不值得靠人記憶時，用本 skill 做 router。它不執行工作，只回答「現在該用哪個 skill / flow」。

## Routing rule

不要只靠本文件的摘要推薦。先判斷使用者現在處於哪個 engineering phase，找出 1–3 個最可能的 candidate，實際讀取 candidate 的 SKILL.md 再決定。

優先推薦「能完成當前目標的最小 skill」，不要因為存在完整 workflow 就強迫使用者從頭跑。

## Phase map

常見情境：

- 不知道 repository 現況 → explore
- 要做新功能 / refactor architecture → design
- 要檢查 module seam / interface depth / locality → codebase-design
- paper reasoning 無法回答一個 design / behavior question → prototype
- 需要 repository 外的官方技術事實 → research
- 已有 Design Doc，要做 acceptance → review
- 已確認 decisions 只需要同步回文件 → doc-sync
- accepted design 太大，需拆 executable work → spec
- 要驗 implementation spec 是否忠於 design → spec-review
- 要開始寫 accepted work → implement
- implementation 中的新 behavior / refactor regression loop → tdd
- 要 review branch / PR / fixed-point diff → code-review
- 要把 accepted Design Doc 做成 presentation → report
- 一次 agent session / workflow 暴露出反覆 failure mode → retro
- effort 大到一個 Design Doc / session 無法先看清完整 decision tree → wayfinder

這只是 navigation hint，不是 source of truth；實際推薦以前仍要讀 candidate skill。

## Flow examples

### Small feature / refactor

~~~
explore（需要時）
  ↓
design
  ↓
review
  ↓
implement
  ↓
code-review
~~~

### Larger implementation

~~~
explore
  ↓
design
  ↓
review
  ↓
spec
  ↓
spec-review
  ↓
implement
  ↓
code-review
~~~

### Huge / foggy architecture effort

~~~
wayfinder
  ↓
resolved decision map
  ↓
design / spec
  ↓
normal flow
~~~

### Design question that paper cannot settle

~~~
design
  ↓
prototype / research
  ↓
decision
  ↓
doc-sync or design update
~~~

## Output contract

回答：

1. Use：最適合的 skill，必要時給 2–4 step flow。
2. Why：它解決的當前問題。
3. Do not use：最容易誤用的鄰近 skill，以及原因。
4. Entry condition：開始前需要的 artifact / baseline。
5. Exit condition：完成後應該得到什麼。

如果沒有現有 skill 適合，明確說 NO MATCHING SKILL，不要硬套。
