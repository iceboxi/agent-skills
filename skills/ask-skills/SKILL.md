---
name: ask-skills
description: Route an engineering task across the pinned Matt upstream catalog and our local architecture overlay. Inspect the actual candidate SKILL.md files before recommending; do not rely on this summary alone.
---

# Ask Skills

這支 skill 只做 routing，不執行 substantive work。它可以由自然語言 engineering request implicit 觸發，用來避免 model-invoked skill 把 explicit-only workflow 吃掉。推薦或跳過某 skill 前，實際讀 1–3 個最可能 candidate 的 SKILL.md。

若最佳 target skill 明確標示為 user-invoked / disable-model-invocation，**不要用鄰近 implicit skill 代替**。回傳明確的 `$skill-name` 入口與理由，等待使用者啟動該 workflow。

## Main flow

### Repository change

Requirement / trade-off 尚未充分收斂：

grill-with-docs → explore（需要 repository grounding 時）→ design → review

Requirement 已精確、current model 也已清楚時，可直接 design。

Design ACCEPT 後：

- small / single-context → implement → code-review
- durable implementation contract → to-spec → spec-review
- multi-context / dependency graph → to-spec → spec-review → to-tickets
  - 手動逐 item → implement
  - whole graph → implement-spec

Implementation 中：
- new behavior → local tdd 的 red-green branch
- legacy behavior-preserving refactor / iOS device-sensitive work → local tdd discipline
- 完成後 → code-review
- difficult / surprising session → retro

## On-ramps

- 不理解 repository current state → explore
- hard bug / flake / performance regression → diagnosing-bugs
- 不知道 codebase 哪裡值得 architecture 投資、要求「找 hotspot / 找下一個值得重構的區域 / 掃 architecture friction」→ improve-codebase-architecture。即使使用者要求「只看原始碼、忽略既有重構文件」，仍然是 architecture survey，不是 explore。
- effort 多 session、route 還在 fog，而且不想綁 tickets → local wayfinder
- GitHub/GitLab issue / external PR-MR intake → triage
- project 第一次設定 Matt tracker/domain docs → setup-matt-pocock-skills

## Shared capabilities

- human decision tree → grilling
- repository alignment + glossary/ADR → grill-with-docs
- stateless interview → grill-me
- domain terminology / ADR → domain-modeling
- deep module / seam / locality → codebase-design
- external authoritative fact → research
- design / runtime / integration / UI uncertainty → local prototype（保留 iOS/Swift-ObjC adaptation）
- behavior implementation / regression seam → tdd
- agent-facing docs / skills → writing-for-agents
- stateful learning → teach
- explanation did not land → wait-what

## Supporting transitions

- accepted decisions 只要同步 existing Design Doc → doc-sync
- cross harness / directory / colleague → handoff
- accepted Design Doc → presentation → report
- knowledge only another person has → to-questionnaire
- human-only provisioning / dashboard / cutover → wizard
- PR / MR body → pr

## Phase boundaries

在 phase 結束時才決定 context 怎麼處理。見 [phase-boundaries.md](phase-boundaries.md)。

- 下一 phase 仍需要 primary reasoning，context 健康 → continue
- 舊 context 無關 → fresh
- 跨 harness / directory / colleague → handoff
- bounded AFK side task → subagent
- context relevant 但太大 → compact

不要 mid-phase 為了整理而 handoff / compact。

## Adjacent distinctions

- grilling ≠ design：前者 resolve human decisions；後者形成正式 target architecture。
- design ≠ to-spec：design 做 architecture decision；to-spec 只 synthesis settled decisions。
- to-spec ≠ to-tickets：前者保存 implementation contract；後者拆 execution graph。
- explore ≠ improve-codebase-architecture：explore 回答「這裡現在怎麼運作」；improve-codebase-architecture 回答「整個 codebase / scope 哪裡最值得 architecture 投資」。後者可內部做 exploration，但不應被 explore 取代。
- explore ≠ research：前者 repository current fact；後者 external fact。
- diagnosing-bugs ≠ prototype：debug 先建立 exact symptom 的 red feedback loop；prototype 解 design uncertainty。
- review ≠ spec-review ≠ code-review：分別是 Design Doc、implementation spec、diff acceptance。
- local wayfinder ≠ to-tickets：wayfinder 清 fog / decisions；to-tickets 拆已知 work。

## Output contract

回答：

1. Use：最適合的 skill / flow
2. Why
3. Do not use：最容易誤用的鄰近 skill
4. Entry condition
5. Exit condition
6. Context move（只在真正 phase boundary 時）

沒有適合 skill → NO MATCHING SKILL。
