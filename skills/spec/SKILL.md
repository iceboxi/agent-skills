---
name: spec
description: Synthesize an accepted Design Doc, resolved grilling/wayfinder decisions, and confirmed constraints into a durable implementation spec. Do not interview, redesign, or decompose the work into tickets/packages.
---

# Implementation Spec

Spec 的工作是 **synthesis, not discovery**。

輸入的 decisions 已經由 grilling / wayfinder / design / review 收斂；本 skill 把它們整理成 implementer 可依循的 durable contract，不重新 interview、不補 architecture、不拆 task graph。

## Preconditions

優先取得：

- accepted Design Doc / accepted technical baseline；
- design review verdict / reopen conditions；
- relevant resolved decisions / prototypes / ADRs；
- implementation scope。

若仍有會改 target architecture 的 unresolved decision，回 design / wayfinder，不在 spec 中解。

## Process

1. **Pin sources**：記錄 canonical Design Doc/version、review basis、prototype / ADR / decision-map pointers。
2. **Recover scope**：problem、target outcome、non-goals、compatibility constraints。
3. **Synthesize decisions**：只保留 implementation 必須知道的 ownership、module/interface、state、runtime/lifecycle、persistence、migration semantics。
4. **Testing decisions**：列 agreed seams、characterization / regression strategy、device/integration gates。優先既有 seam；若 seam 本身仍有 design uncertainty，回 design。
5. **Acceptance**：把 observable behavior / compatibility / migration success 寫成 acceptance criteria。
6. **Reopen conditions**：明確列出哪些 implementation evidence 會要求回 design。
7. **Traceability check**：每個 implementation decision 都能追到 accepted source；追不到的內容不得加入。

## What belongs here

- Problem / outcome
- Accepted implementation decisions
- Accepted module / interface contracts
- Runtime / lifecycle invariants
- Testing decisions / agreed seams
- Migration / compatibility constraints
- Acceptance criteria
- Out of scope
- Reopen conditions
- Source pointers

## What does not belong here

- 新 architecture decision
- 新 interview / grilling
- task / ticket / work-package graph
- branch / worktree orchestration
- detailed file-by-file implementation recipe
- speculative cleanup

Prototype 若有一小段 state machine / type shape 比 prose 更精確，可以保留 decision-rich fragment 並指回 prototype source；不要貼 working demo。

## Handoff

- 小型、單一 context 可完成 → implement
- 需要多個 fresh-context slices / dependency graph → work-breakdown
- spec fidelity 需要獨立驗證 → spec-review

## Completion criterion

Spec 完成時：

- implementer 不需要重新做 architecture decision；
- 每個重要 contract / invariant 都能 trace 到 accepted source；
- testing seam / acceptance / reopen condition 足以判斷 implementation drift；
- 沒有 task decomposition 混進 spec；
- 沒有因「看起來缺東西」而 invent 新 design。
