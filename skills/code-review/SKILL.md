---
name: code-review
description: Independently review a code diff against correctness, the accepted spec/design, repository standards, architecture/locality, and verification quality. Use for PRs, branches, or work-in-progress diffs; do not modify code unless the user explicitly asks for fixes.
---

# Code Review

對 fixed-point diff 做獨立 review。Spec fidelity 只是其中一軸；符合 spec 不代表 code 正確。

## Setup

1. Pin fixed point（commit / branch / merge-base）與 diff scope。
2. 找 accepted spec / Design Doc / issue；若不存在，仍可做 correctness / quality review，但明確標示 fidelity axis unavailable。
3. 讀 project standards、AGENTS / lint / test conventions；若有 relevant GLOSSARY / ADR，一併讀取，檢查命名/decision 是否與既有 domain model 衝突。只讀與 diff 相關內容。

## Review axes

盡可能獨立執行各軸；環境支援 subagents 時可平行，避免一個 axis 的結論污染另一個。使用 Codex native review/subagent harness 執行即可，本 skill 定義 review rubric，不重造 diff/worktree engine。

### A. Correctness & runtime semantics

找：

- wrong branch / nil / bounds / error handling；
- concurrency、race、lifetime、retain、ordering；
- retry / timeout / cancellation；
- persistence / identity / stale callback；
- cross-language / ObjC / ABI / platform contract；
- behavior-preserving refactor 的 semantic drift。

### B. Spec & design fidelity

檢查：

- requirement / acceptance criteria 是否完整實作；
- scope creep；
- accepted ownership / dependency / capability surface 是否被繞過；
- implementation 是否偷偷新增 design decision；
- reopen condition 是否已發生但未停止。

### C. Design quality & locality

使用 `codebase-design` discipline：

- shotgun surgery；
- shallow / pass-through abstraction；
- speculative generality；
- duplicated ownership；
- bypass pressure；
- generic mechanism 吸收 feature policy；
- 一個 logical change 是否落在合理 owner。

不要只因 file count 多就找問題；wide migration 的 blast radius 可合理，重點是 target locality 是否改善。

### D. Verification quality

檢查：

- tests 是否驗 behavior 而非 private implementation；
- expected values 是否有 independent source；
- 是否缺 characterization / regression；
- test 是否真的會在錯誤 implementation 下 fail；
- build / integration / device gate 是否與 spec 對齊；
- 未執行項目沒有被宣稱通過。

## Findings

每個 finding 必須包含：

- Severity
- Claim
- Code evidence（file:line / diff hunk）
- Spec / design evidence（有 baseline 時）
- Impact
- Required action

Severity：

- **BLOCKING**：會造成錯誤 behavior、data / lifecycle / compatibility risk、違反 accepted contract，或重大未測 semantic drift。
- **NON-BLOCKING**：code 可接受但有局部 maintainability / verification risk。
- **NOTE**：值得注意但不要求此次修改。

Verdict：

- **PASS**
- **PASS WITH NOTES**
- **CHANGES REQUIRED**
- **BLOCKED**

Review 不自行改 code。使用者要求修正時，另進 implementation/fix workflow，再重新 review。

## Completion criterion

Final report 至少分開呈現：

- Correctness
- Spec / design fidelity
- Design quality / locality
- Verification

最後列 fixed point、reviewed scope、finding counts、最嚴重問題與 next action。
