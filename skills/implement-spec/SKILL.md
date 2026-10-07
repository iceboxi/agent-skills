---
name: implement-spec
description: Implement an accepted spec and work graph end-to-end by working the ready frontier, using isolated Codex subagents/worktrees where appropriate, integrating continuously, and finishing with whole-branch code review.
---

# Implement Spec

這是 whole-spec orchestration。它消費：

- accepted spec
- accepted work breakdown / dependency graph

它不重新拆 architecture，也不需要 issue tracker。

## Goal

把整份 spec 落到一個 coherent integration result，work graph 上所有 in-scope items 完成，最後跑 whole-result verification 與 code-review。

## 1. Load the graph

讀 spec + work graph，只載入必要 pointers。

辨識：

- ready frontier：所有 blockers 都已完成的 items；
- integration-sensitive items；
- device / manual gates；
- items 可否安全平行。

不要因為 graph 上有多個 ready items 就一律 parallel；write-heavy work 若 overlap ownership / files / migration state，序列化比較安全。

## 2. Execution model

優先使用 Codex native capabilities：

- subagents
- isolated worktrees / branches
- native context management

本 skill 定義 **what may run concurrently and how to integrate**，不重造 Git/worktree framework。

每個 implementer：

1. 只拿自己的 work item + spec/source pointers；
2. 使用 implement + tdd discipline；
3. 不重新做 design；
4. 跑 item-level verification；
5. 回報 changed scope、verification、reopen issue。

## 3. Integration loop

每個 item 完成後：

- 先整合到 integration line；
- 跑受影響的 regression / build gate；
- 更新 completed blockers；
- 重算 frontier；
- 再啟動新 ready work。

若 integration evidence 觸發 spec/design reopen condition：

- spec omission → pause affected frontier, update/review spec；
- architecture contradiction → stop affected branch, return design/review。

不要讓 downstream items建立在已知漂移的 baseline 上。

## 4. Whole-result verification

所有 graph items 完成後：

- 跑 full relevant test/build suite；
- 跑 spec 定義的 integration/device gates；
- 驗 migration/compatibility criteria；
- 確認 old path / bridge 的 retirement conditions（relevant 時）；
- 檢查 work graph 沒有遺漏 in-scope item。

## 5. Whole-branch review

最後對 integration fixed point 跑 code-review。

Item-level review 可依風險做，但 whole-branch review 不能省，因為跨 item interaction 只有整合後才看得到。

修正 blocking findings 後重跑 affected verification。

## Completion report

回報：

- Spec baseline
- Completed work graph
- Parallel / sequential execution decisions
- Integration verification
- Whole-branch code-review verdict
- Device/manual gates completed / remaining
- Any accepted deviations
- Reopen items

除非使用者要求，不自動 push / release。

## Completion criterion

整份 spec 的 acceptance criteria 在 integration result 上成立，而不是只證明每張 work item 各自完成。
