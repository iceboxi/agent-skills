---
name: ask-skills
description: Route an engineering task to the smallest useful skill or flow. Before recommending or skipping a candidate, inspect its actual SKILL.md; account for phase boundaries, working-directory state, and whether the problem is a fact, decision, runnable uncertainty, build, review, or environment failure.
---

# Ask Skills

你不需要記住所有 skill。這支 skill 只做 routing，不執行 substantive work。

推薦或跳過某 skill 前，實際讀 1–3 個最可能 candidate 的 SKILL.md；本文件摘要只用來 shortlist。

## Main flow

### Idea / change in a repository

若 requirement / decision 尚未充分收斂：

grill-with-docs
→ design
→ review

若 requirement 已很精確，且沒有需要 HITL decision tree 的 ambiguity，可直接 design。

Design ACCEPT 後：

- small / single-context → implement
- durable implementation contract needed → spec → spec-review
- multi-context / dependency graph → spec → spec-review → work-breakdown
  - 手動逐 item → implement
  - whole graph orchestration → implement-spec

Implementation 使用 tdd / characterization，最後 code-review。

完成後、尤其有 friction / failure 時 → retro。

## On-ramps

- 不理解 repository current state → explore
- hard bug / flake / regression → diagnosing-bugs
- 不知道 codebase 哪裡值得 architecture 投資 → improve-codebase-architecture
- effort 多 session 且 route 還在 fog → wayfinder

## Shared primitives

- human decision tree → grilling
- repository 中 grilling + glossary/ADR → grill-with-docs
- stateless decision interview → grill-me
- domain terminology / ADR → domain-modeling
- deep module / seam / locality → codebase-design
- external authoritative fact → research
- runnable uncertainty → prototype
- behavior implementation / regression seam → tdd
- agent-facing docs / skills → writing-for-agents

## Supporting transitions

- confirmed decisions 只要同步回 existing doc → doc-sync
- cross harness / directory / colleague / mid-phase side task → handoff
- accepted Design Doc → presentation → report
- knowledge only another person has → questionnaire
- genuinely human-only provisioning / dashboard / cutover → wizard
- PR / MR body after implementation/review → change-summary

## Phase boundaries

在 phase 結束時才決定 context 怎麼處理。見 [phase-boundaries.md](phase-boundaries.md)。

核心原則：

- 下一 phase 需要目前 reasoning 作 primary source，而且 context 還健康 → continue。
- Context 對下一 phase完全沒用 → clear / fresh context。
- Context 要搬到別的 harness / directory / colleague → handoff。
- bounded AFK side task → subagent。
- 同 harness / directory、context relevant 但太大 → compact。

不要 mid-phase 為了整理而 compact / handoff。

## Adjacent distinctions

- grilling ≠ design：前者 resolve human decisions；後者 synthesis target architecture。
- design ≠ spec：design decides architecture；spec忠實轉成 implementation contract。
- spec ≠ work-breakdown：spec保存 contract；work-breakdown決定 execution graph。
- implement ≠ implement-spec：前者一個 ready unit；後者 orchestrate whole graph。
- explore ≠ research：前者 repository current fact；後者 external fact。
- diagnosing-bugs ≠ prototype：debug要先有 red-capable exact symptom loop；prototype只回答 design question。
- questionnaire ≠ research：前者取 knowledge from a person；後者查 authoritative external sources。
- wizard ≠ implement：wizard只處理 agent 無法代做的人類操作；可由 agent 執行的工作仍由 implement/tooling 完成。
- review ≠ spec-review ≠ code-review：分別是 design、spec、diff acceptance。

## Output contract

回答：

1. Use：最適合的 skill / flow。
2. Why：它解決目前哪一個 phase problem。
3. Do not use：最容易誤用的鄰近 skill。
4. Entry condition。
5. Exit condition。
6. Context move：continue / fresh / handoff / subagent / compact（只有真的在 phase boundary 時）。

沒有現有 skill 適合 → NO MATCHING SKILL。
