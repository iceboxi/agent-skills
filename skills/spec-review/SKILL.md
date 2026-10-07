---
name: spec-review
description: Independently review an implementation spec against its accepted Design Doc, resolved decisions, repository reality, testing seams, and acceptance criteria. Use as a fidelity gate before work decomposition or implementation; do not redesign or decompose the work.
---

# Spec Review

Spec Review 判斷：這份 spec 是否**忠實保存已接受設計，而且足以交給 implementation**。

它不是 design review、work-breakdown review、code review。

## Inputs

需要：

- implementation spec；
- accepted Design Doc / decisions；
- design review acceptance basis / reopen conditions；
- relevant repository evidence（只查會影響 verdict 的 current facts）。

## Review axes

### 1. Decision fidelity

檢查 spec 是否：

- 遺漏 accepted owner / interface / lifecycle / migration invariant；
- 偷偷新增 owner、protocol、public capability、state copy；
- 把 implementation example 升格成 required contract；
- 弱化 negative requirement / ordering / numeric / compatibility detail；
- 把 unresolved recommendation 寫成 confirmed decision。

### 2. Testing decisions

檢查：

- agreed seams 是否真的對應 observable behavior；
- characterization / regression strategy 是否能抓 semantic drift；
- device / hardware / OS gate 沒被 unit tests 取代；
- expected values 有 independent source；
- planned validation 沒被寫成 completed evidence。

### 3. Acceptance & reopen conditions

檢查：

- acceptance criteria 可觀察；
- migration / compatibility 成功條件具體；
- implementation 發現哪些 evidence 必須停下回 design，有明確定義。

### 4. Traceability

高風險或 architecture-relevant statement 應能追到：

- accepted Design Doc；
- confirmed decision；
- prototype result；
- ADR / wayfinder resolution；
- repository current fact。

追不到就是 scope drift candidate，不因內容「看起來合理」而接受。

## Findings

每個 finding：severity、claim、source evidence、impact、required action。

Verdict：

- ACCEPT
- ACCEPT WITH NON-BLOCKING NOTES
- REVISE
- BLOCKED

若需要新 architecture decision → REQUIRES DESIGN。
若只是 spec 遺漏 / wording / fidelity → 回 spec。

## Completion criterion

ACCEPT 類型表示：

- spec 是 accepted design 的忠實 implementation contract；
- testing / acceptance 足以偵測主要 semantic drift；
- 沒有 task decomposition 或新 architecture decision 混入；
- 可以安全交給 work-breakdown 或 implement。
