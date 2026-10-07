---
name: work-breakdown
description: Break an accepted implementation spec into bounded fresh-context work items with blocking edges, using tracer-bullet vertical slices by default and expand-contract for wide refactors. Do not redesign the system.
---

# Work Breakdown

把 accepted spec 拆成可執行 work graph。這一階段解決的是 **how to sequence the work**，不是 architecture。

## Preconditions

需要：

- accepted implementation spec；
- relevant design/review basis；
- project build/test constraints。

若 spec 尚未 accepted，或 decomposition 暴露新的 architecture decision，停止並回 spec / design。

## 1. Choose the slicing model

### Tracer-bullet vertical slice — default

每個 slice：

- 穿過完成 behavior 所需的 relevant layers；
- 完成後可 demo / observe / verify；
- 可在一個 fresh context 中理解與完成；
- 有自己的 acceptance / verification；
- 不依賴 implementer 記得上一個 session 的 reasoning。

避免 layer-by-layer horizontal slicing，例如「先做所有 models，再做所有 repositories，再補 tests」。

### Wide refactor — exception

若是 mechanical / ownership migration，任何單一 vertical slice 都無法保持 coherent green state，使用 expand-contract：

1. Expand：加入新 form / seam，舊路徑仍可工作。
2. Migrate：依 blast radius 分批移 callers / data / ownership。
3. Contract：所有 consumers 遷移後刪掉舊 form。
4. 若中間批次無法 individually green，明確設 integration verification gate，不假裝每一步都是 independently shippable。

## 2. Build the graph

每個 work item 包含：

- Title
- What it delivers
- Inherited spec decisions
- Blocked by
- Acceptance criteria
- Verification seam / command / device gate
- Relevant owner / likely touchpoints
- Non-goals
- Stop / reopen condition

Blocking edge 只表達 genuine prerequisite，不要把「我想照這個順序做」假裝成 dependency。

## 3. Prefactoring

若 small prefactor 能顯著 make the change easy，而且不改 behavior / architecture，可以成為前置 item。

若 prefactor 本身需要新的 seam / owner / contract decision，回 design，不在 decomposition 階段決定。

## 4. Locality check

利用 codebase-design：

- 一般 logical change 是否落在合理 owner；
- work graph 是否暴露 shotgun surgery；
- target design 的 extension exercise 是否在 implementation breakdown 中仍成立。

若 spec 預期的 ordinary extension 仍需大量 unrelated edits，這可能不是 decomposition 問題，而是 design locality failure：標 REQUIRES DESIGN REVIEW。

## 5. Human check

提出完整 work graph 後，請使用者 review：

- granularity 是否太粗 / 太碎；
- blocking edges 是否真的是 blockers；
- 哪些 items 應 merge / split；
- 哪些需要 device/manual gate；
- 是否有 rollout / release constraint 影響 sequencing。

確認後才視為 ready work graph。

## Artifact

不強迫 issue tracker。

優先沿用 project convention；沒有時可寫：

.scratch/<feature>/work/

每個 item 可以獨立 Markdown，也可以在一份 work-graph.md 中，只要 fresh implementer 能單獨取得所需 context pointer。

如果團隊使用 GitHub/GitLab Issues，可 mirror / publish，但 tracker 不是本 skill contract。

## Completion criterion

完成時：

- 每個 ready item 可由 fresh context 執行；
- dependency frontier 可判定；
- normal work 優先 vertical slice，wide refactor 有明確 expand-contract 理由；
- work items 沒有 invent architecture；
- 使用者已確認 granularity / blocking graph。
