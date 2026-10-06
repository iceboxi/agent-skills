---
name: design
description: Design a concrete, implementable software solution for a new feature or refactor from repository evidence and requirements. Produces the Design Doc itself: current-state analysis when relevant, target architecture, responsibility boundaries, protocols/interfaces, runtime flows, migration strategy, implementation phases, and verification. Use before implementation; do not merely reformat an already-decided design.
---

# Software Design

本 skill 負責 **software design 本身**，不是只把別的 workflow 結果整理成文件。

輸入通常是 requirement + repository。輸出是可獨立 review、可實作的 Design Doc。

核心流程：

```text
Requirement
    ↓
Repository evidence
    ↓
Current model / integration context
    ↓
Design decisions
    ↓
Target architecture
    ↓
Protocols / interfaces / runtime flows
    ↓
Migration / implementation phases
    ↓
Verification
    ↓
Design Doc
```

預設使用繁體中文，保留 code identifiers、API names 與 repository terminology。

## 1. Core responsibility

Design 必須：

1. 理解需求、scope、non-goals 與 compatibility constraints。
2. 讀取 relevant repository code；若缺 current model，先完成必要的 explore 工作。
3. 找出 responsibilities、dependencies、state ownership、extension points 與主要 runtime flows。
4. 根據實際問題提出 target architecture。
5. 只有在確實解決 boundary / testability / extensibility 問題時才引入 abstraction / protocol / pattern。
6. 提供 concrete protocols / interfaces / type sketches。
7. 說明每個重要 abstraction 為什麼存在、解決什麼問題、誰 consume、誰 implement。
8. 讓每個 protocol / type 都能在 target architecture 或 interaction flow 中找到位置。
9. 對 refactor 提供 Current → Target 對照與 migration。
10. 從 architecture dependency 與 migration safety 推導 implementation phases。
11. 提供可驗證的 acceptance / regression strategy。
12. 產出正式 Markdown Design Doc；Design Doc 是 design 的產物，不是另一個 downstream skill。

## 2. Do not design by pattern name

不要從「我要 MVVM / Clean Architecture / Repository」開始硬套。

優先順序應是：

```text
problem / requirement
    ↓
responsibility boundary
    ↓
state ownership
    ↓
dependency direction
    ↓
abstraction / interface
    ↓
pattern (only if useful)
```

可使用 Clean Architecture、MVVM、Repository、Coordinator、Strategy、Adapter、State、Factory 等任何合理 pattern，但必須能說明它在此 repository 解決的具體問題。

現有 concrete type / helper 已足夠時，不為抽象而新增 protocol。

## 3. Evidence discipline

Project-specific technical conclusion 必須來自 repository evidence。

區分：

- **CURRENT**：實際存在的 code / behavior。
- **INTERPRETATION**：由 evidence 推導的 current model。
- **PROPOSED**：尚未實作的 target。
- **CONFIRMED DECISION**：使用者已確認的重要取捨。
- **PENDING**：仍可能改變 target 的 decision。
- **PLANNED VALIDATION**：未執行的 test / spike / prototype。

不要把 proposed API、planned tests 或 target behavior 寫成 current fact。

重要 current-state claim 使用 `file:line` + symbol evidence。

## 4. New feature vs refactor

### New feature

至少建立：

- requirement / user or system goal
- relevant existing integration context
- affected owners / extension points
- target architecture
- interfaces / contracts
- runtime / data / event flow
- state ownership
- failure / recovery semantics
- impact on existing components
- implementation phases
- verification

新功能不一定需要完整 Current Architecture，但必須清楚說明「新功能插進現有系統哪裡」。

### Refactor

先驗證 premise。成立後至少建立：

- current architecture
- current responsibility / state ownership
- representative current runtime flows
- concrete problems / coupling / limitations
- target architecture
- target responsibility / state ownership
- current → target mapping
- representative before → after flow
- migration / transitional architecture
- behavior invariants
- implementation phases
- regression strategy

若 premise 被 evidence 推翻，交付 PREMISE REJECTED，不虛構 refactor target。

## 5. Target architecture contract

Target design 必須回答：

- 完成後有哪些 components？
- 每個 component 的 responsibility 是什麼？
- 誰依賴誰？
- canonical state 在哪裡？
- temporary / editing / operation state 在哪裡？
- 哪些 side effects 屬於哪個 owner？
- 哪些 dependency 是 input / output boundary？
- important runtime event 如何穿過系統？
- failure / recovery / lifecycle 怎麼處理？
- 未來增加相似功能時，修改點在哪裡？

優先最簡單、可讀、可驗證、可擴充的方案，而不是理論上最純的方案。

## 6. Protocol / interface contract

每個 significant protocol / interface 必須說明：

- **Purpose**：為什麼存在？
- **Problem solved**：解決哪個 coupling / responsibility 問題？
- **Consumer**：誰依賴它？
- **Implementer**：誰實作？
- **Responsibilities**：它保證什麼？
- **Non-responsibilities**：刻意不處理什麼？
- **Contract**：key methods / data types / events。
- **Error semantics**：錯誤如何表達 / 傳遞？
- **Concurrency / lifecycle**：若 relevant，誰可呼叫、callback domain、ownership / cancellation 等。

提供足以 review 的 concrete code sketch，例如：

```swift
protocol ScooterSettingRepository {
    func load() async throws -> ScooterSettings
    func save(_ settings: ScooterSettings) async throws
}
```

但 code sketch 必須服務 architecture，不要求把完整 implementation 寫進 Design Doc。

### No orphan abstraction

每個新 protocol / type 必須至少出現在：

- Target Architecture Diagram，或
- Design Realization Diagram，或
- Runtime / Sequence Flow

之一。

如果 reader 看完 protocol 還不知道「它在系統哪裡、誰用它」，design 不完整。

## 7. Diagrams

Markdown Design Doc 預設使用 Mermaid。

依 scope 至少提供：

### Refactor
- Current Architecture
- Target Architecture
- Representative Current Flow
- Equivalent Target Flow
- Current → Target responsibility mapping

### New feature
- Existing Integration Context
- Target Architecture
- Important Runtime / Sequence Flow

若 lifecycle / state transition 重要，再加入 state diagram。

圖中的 component / protocol 名稱要與本文與 code sketch 一致，不另造第二套 vocabulary。

每張圖回答一個主要問題；不要把整個系統塞成一張巨型圖。

## 8. Current → Target mapping

Refactor 應直接展示 responsibility 怎麼搬，例如：

| Area | Current | Target | Reason / invariant |
| --- | --- | --- | --- |
| committed state | ... | ... | ... |
| editing state | ... | ... | ... |
| operation workflow | ... | ... | ... |
| persistence | ... | ... | ... |

並指出：

- retained components
- modified components
- moved responsibilities
- introduced components
- removed / retired components
- intentionally unchanged boundaries

## 9. Representative runtime flows

不要只畫 static boxes。

至少選最能驗證 design 的代表 scenario，說明：

- trigger
- call / event order
- state reads / writes
- side effects
- success
- error / timeout / retry / recovery
- observable invariant

Refactor 優先使用 before → after 對照。

## 10. Design decisions and alternatives

有實質替代方案時比較：

- responsibility / ownership
- dependency direction
- complexity
- migration impact
- testability
- extensibility
- regression risk

不要為了形式製造假選項。

重大 design-blocking choice 如果 repository 無法決定，提出 recommendation 與理由，保留為 Pending，除非使用者已明確授權你做該 engineering trade-off。

Implementation-only details 不需要阻塞 Design Doc。

## 11. Implementation phases are part of design

Implementation plan 不再是另一隻 skill。

Phase 必須從 architecture dependencies、migration safety 與 validation gates 推導，而不是隨意分 P1 / P2 / P3。

每個 phase 說明：

- Goal
- Preconditions
- Components changed
- New / changed interfaces
- Behavior preserved / introduced
- Verification
- Migration / compatibility
- Rollback / stop condition
- Dependency on earlier phases

避免 big-bang；但也不要為了「incremental」製造 dual owner / dual writer。

若某個 phase 需要 temporary bridge，明確說明其 scope、owner、retirement condition。

## 12. Verification

區分：

- existing tests / fixtures
- characterization tests to add
- new unit / integration tests
- manual / device validation
- planned spike / prototype

不要宣稱未執行的驗證已通過。

對 behavior-preserving refactor，至少回答：

```text
existing baseline
    ↓
target invariant
    ↓
verification method
    ↓
failure / stop condition
```

## 13. Design Doc output contract

章節可依任務調整，但 reviewer 最終必須能回答：

- 為什麼要做？
- scope / non-goals 是什麼？
- 現在怎麼運作？
- current limitation 是什麼？
- target architecture 是什麼？
- responsibility / state owner 怎麼改？
- 每個新 protocol 為什麼存在？
- protocol 在 architecture 哪裡？
- important runtime flow 怎麼走？
- failure / lifecycle 怎麼處理？
- refactor 怎麼安全遷移？
- implementation 如何分階段？
- 每階段怎麼驗證？
- 哪些 decision / limitation 仍 unresolved？

若這些問題無法回答，Design Doc 尚未完成。

## 14. Handoff

完成 Design Doc 後：

```text
design
   ↕
 review
   ↓
implementation

Design Doc
   ↓
 report
   ↓
presentation
```

`review` 是獨立 acceptance gate；若 verdict = REVISE，回到 design 修正受影響的 decision / section，而不是由 reviewer 重做 target。

`report` 只能從 Design Doc 提取 presentation，不重新設計 architecture。

本 skill 不授權 production code implementation、migration、branch、commit 或 release；除非使用者另行明確要求。