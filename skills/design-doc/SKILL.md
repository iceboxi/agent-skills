---
name: design-doc
description: Create or update an independently reviewable Markdown Design Doc that synthesizes existing architecture or refactoring evidence, decisions, implementation mechanics, diagrams, and verification strategy. Use when a Design Doc is requested or architecture results should be documented; do not use merely to persist another workflow's artifact.
---

# Design Document

將既有 architecture understanding、decisions、evidence 與必要 implementation mechanics 整理成可獨立 review、可追查、可長期維護的 Markdown Design Doc。

主要讀者是不熟悉 repository 的工程師；同時應讓熟悉 code 的 reviewer 與 AI / CLI 能追查 evidence。

本 skill 是 downstream architecture synthesis / persistence。它具體化已存在的 design reasoning，不自行重做 architecture selection，也不取代 implementation planning。

## 1. Boundary and source authority

適用：

- 使用者明確要求 Design Doc / architecture document；
- 已接受把 architecture / refactor 結果整理成可 review 文件；
- 需要保存 current / target / ownership / behavior / state / implementation mechanics / verification。

不適用：

- 只是保存 implementation plan、review report、technical report 或其他 workflow artifact；
- ownership、target architecture、contracts 或 alternatives 尚待決定：回 `architecture`；
- 只需要 execution order、batches、rollback 或 task tracking：使用 planning workflow。

不得藉此修改 production code、agent instructions、CLI settings、開始 migration、commit 或發布。

Source precedence 沿用上游已確認結果與使用者指定。重要 project-specific claim 應對照 repository evidence；過期 code locations 要重查。無法查證時保留 assumption / limitation，不用一般知識補成 project fact。

文件可保存：

- Resolved
- Draft / Pending Decisions
- Blocked
- PREMISE REJECTED
- current-state documentation

不得把 proposal、planned validation、未執行 tests 或未實作 target 寫成 current fact。

## 2. Core design contract

Design Doc 不要求固定章節名稱，但依 scope 必須回答足以 review design 的問題：

1. **Why / Goal**：為什麼改？完成後解決什麼？
2. **Scope / Non-goals**：改什麼、不改什麼？
3. **Current**：目前 responsibility、dependency、runtime behavior、state 怎麼運作？
4. **Target**：完成後 components、boundaries、ownership、dependency 怎麼變？
5. **Change Scope**：哪些 responsibility / state / flow 會搬？哪些刻意不動？
6. **Interfaces / Dependencies**：重要 module、protocol、API、hardware / software boundary 怎麼互動？
7. **Behavior / Scenarios**：代表 runtime scenario 的 ordering、success / failure / recovery、callbacks / events 怎麼走？
8. **State**：有哪些 meaningful state？誰擁有？何時建立、失效、提交、恢復？
9. **Implementation Mechanics**：哪些 type / function / algorithm / synchronization 細節是證明 design 可落地所必需？
10. **Verification**：怎麼證明 target 成立，behavior-preserving refactor 沒改壞既有 contract？
11. **Constraints / Known Limitations**：哪些限制必須接受？
12. **Pending / Open Questions**：哪些問題仍影響實作？

Architecture-change proposal 應在前段提供 **Target Architecture Overview**。不要因 exact API 尚未定案就省略 conceptual target。

## 3. Change profiles

Core contract 是共同骨架；依變更型態增加需要的內容，不套固定模板。

### UI / Feature

視需要包含：

- UX / user journey
- representative user scenarios
- screen / component hierarchy
- UI flow
- presentation state
- API interactions
- selectors / analytics / accessibility / test hooks

### Architecture / Refactor

優先包含：

- current → target architecture
- **What moves / What stays**
- ownership / responsibility boundaries
- module / package boundaries（若 dependency structure 重要）
- representative before → after
- representative runtime scenarios
- compatibility invariants
- migration boundary
- behavior parity / regression strategy

### Data / Persistence

視需要包含 schema / model、consistency、migration / backward compatibility、transaction / ordering、failure / recovery。

### Service / API

視需要包含 API / protocol contracts、lifecycle、concurrency / isolation、error semantics、compatibility、consumers / implementations。

同一份文件可同時符合多個 profile。

## 4. Architecture / refactor narrative

Architecture / refactor 常見閱讀主線：

```text
Why / Problem
→ Scope / Non-goals
→ Current
→ Target
→ What moves / What stays
→ Representative before → after
→ Contracts / behavior / state
→ Critical implementation mechanics
→ Migration boundary
→ Compatibility / verification
→ Open questions
```

這是 narrative pattern，不是固定目錄。Reviewer 應在前段理解 target，technical deep dives 往後 progressive disclosure。

### What moves / What stays

對 refactor，不只提供 Current / Target diagrams；應直接呈現 responsibility / state / flow 怎麼搬。

可用：

| Area | Current | Target | Intentionally unchanged |
| --- | --- | --- | --- |
| committed state | ... | ... | ... |
| draft / edit state | ... | ... | ... |
| operation workflow | ... | ... | ... |
| persistence | ... | ... | ... |

目的：快速辨識 scope boundary 與 accidental redesign。

### Representative before → after

選 1–3 個足以代表 target responsibility model 的 operation / flow：

```text
CURRENT
- who owns logic/state?
- runtime behavior?

TARGET
- what moves?
- what stays?
- new owner?

INVARIANT
- what contractual behavior must remain?
```

可搭配 table、sequence、state diagram、pseudocode 或 code sketch。不要為完整而逐一展開所有 callers / panels；其餘用 coverage / inventory。

## 5. Structure, behavior and state

Design Doc 應依 scope選擇互補視角：

| View | Review question |
| --- | --- |
| Structure | components、dependency、ownership、protocol、responsibility boundary |
| Behavior | runtime ordering、async interaction、callback / event、success / failure / recovery |
| State | meaningful state、owner、trigger、guard、invalidation、recovery |

State ownership 是一級設計問題。至少要能回答：

- committed state 在哪裡？
- draft / temporary state 在哪裡？
- operation state 在哪裡？
- identity / session state 在哪裡？
- presentation state 是否只是 output，還是另一個 source of truth？

不要讓同一份 state 出現多個 canonical owner。

## 6. Diagram strategy

Diagram 是 review 的共同語言，不是 UML checklist。**先問 reviewer 需要理解什麼關係，再選 representation。** 如果 table、code sketch 或 prose 更清楚，就不要為湊圖而畫圖。

Markdown Design Doc 預設使用 Mermaid fenced blocks，讓 topology 可 review、可 diff。

| Design question | Representation |
| --- | --- |
| component / dependency / ownership | block-style `flowchart` |
| module / package / target boundary | `flowchart` + `subgraph` |
| type / protocol / inheritance / composition | `classDiagram` |
| data / persistence path | `flowchart` |
| runtime ordering / callback / async interaction | `sequenceDiagram` |
| lifecycle / meaningful state transition | `stateDiagram-v2` |
| representative scenario | ordering → sequence；routing / branching → flowchart |

Guidelines：

- 每張圖回答一個主要 design question。
- Current / Proposed / Confirmed Target 狀態要明確。
- Current 與 Target 若 behavior 不同，分開畫。
- 不補造 node、edge、state、message、ownership。
- component node 應表達 responsibility，不只列 class name。
- class diagram 只放影響 boundary / ownership / API / lifecycle 的 types。
- module diagram 表達 logical boundary 與 dependency，不複製 folder tree。
- sequence 要呈現有語意的 ordering、sync / async boundary、callback / event、failure / recovery；不列每個 function call。
- state diagram 必須指出 owner；transient control-flow step 不自動升格為 state。
- Arrow semantics 不清楚時，說明是 dependency、ownership 還是 runtime flow。
- 正式 UML 若比簡單 block / flow representation 更難懂，優先清楚而不是形式完整。

Architecture/refactor 至少考慮 Current structure、Target structure、以及一個最能暴露 ordering / ownership 的 representative sequence；其他圖只有在回答新的 design question 時才加入。

Design Doc 以 Mermaid source 為 authoritative diagram representation。SVG / PNG 可作 preview 或 downstream artifact，但不取代 source-of-truth。

## 7. Protocols and implementation sketches

真正定義 architecture boundary 的 protocols / interfaces 是主要內容，但不要逐一列 repository 所有 protocols。

視需要描述：

- purpose / owner / layer
- implemented by / consumed by
- responsibilities / non-responsibilities
- operations / input-output semantics
- lifecycle / ordering
- state implications
- error semantics
- concurrency / isolation
- limitations / proposed changes / open questions

API / protocol declaration 必須區分 **CURRENT API**、**PROPOSED — NOT YET ACCEPTED**、**CONFIRMED TARGET API**。Responsibility confirmed 不等於 exact signature accepted。

### Concrete code is valid design material

**不要因內容像 code 就排除。**

當 implementation mechanics 會影響 ownership、ordering、state transition、concurrency、error / recovery、identity / lifecycle、serialization / codec、compatibility 或 feasibility 時，應提供 concrete type / function sketch、pseudocode 或 representative code。

例如：

```swift
// DESIGN-LEVEL SKETCH
func handleEvent(_ event: Event, session: Session) {
    guard session.isValid else { return }
    let result = apply(event)
    emit(result)
    requestPersistenceSnapshot(result)
}
```

Code sketch 應讓 reviewer 能檢查：

- identity 從哪裡來？
- state 何時 mutation？
- event 何時 emit？
- persistence 是否是 gate？
- failure 是否 rollback？
- callback 是否可能 re-enter？

若具體機制本身是 architecture decision，可進一步描述 lock scope、actor isolation、generation token、transaction ordering。

但不要：

- 預寫每一個 method；
- 複製大量 production implementation；
- 列逐檔修改順序；
- 用 code 掩蓋未確認的 architecture decision。

> **Design Doc 的 code 回答「這個 design 具體怎麼成立？」；Implementation Plan 回答「用什麼順序做完？」**

## 8. Behavior parity and verification

Behavior-preserving refactor 的 compatibility contract 是 design 內容，不只是 test list。

優先用：

| Behavior | Existing baseline | Target owner / shape | Invariant | Verification |
| --- | --- | --- | --- | --- |
| representative operation | current trace | new owner | what must stay identical | how to compare |

Verification 可包含：

- core equivalence：merge / codec / serialization / bytes
- workflow equivalence：ACK / timeout / retry / commit / rollback
- identity / lifecycle：switch / logout / late callback / stale work
- persistence / event ordering
- runtime / integration acceptance

Planned tests 不得寫成 existing coverage。

## 9. Migration boundary

Design Doc 可以描述 migration shape、dependency、compatibility boundary 與 architecture gates，但不取代 execution plan。

Design Doc回答：

- 哪些 ownership 必須 atomic takeover？
- 哪些 caller 可逐批遷移？
- 過渡期允許哪些 bridge？
- 哪些 dual-owner 狀態禁止進 production？
- 哪些 validation failure 需要 reopen architecture？

Implementation Plan 再負責 work batches、file / task order、staffing、rollback steps、acceptance execution、progress tracking。

## 10. Decisions, limitations and open questions

Observed facts、interpretations、assumptions、proposed changes、confirmed decisions 與 unresolved questions 必須區分。

有價值的 rejected alternative 記錄：

- alternative
- why considered
- why rejected / deferred
- decisive evidence / constraint

Known limitations 應正式留在文件中，不要全部降級成 implementation risk。

若仍有會決定 target responsibility、ownership、dependency 或 contract 的 blocking decision，文件維持 **Draft / Pending Decisions**。

## 11. Writing, traceability and consistency

以繁體中文寫作；使用短句、active voice、穩定 terminology。Code identifiers、API names 與 established engineering terms 保持原樣。

重要 technical description 提供 repository-relative `file:line` / symbol。Design Doc 必須自己可理解，但 evidence / code reference 是正式 review material，不預設隱藏。

Current / proposed / target 與 existing / planned / executed tests 必須分開。

Structure、behavior、state、protocol、diagram、code sketch、verification 要描述同一套 design。若互相矛盾，修正文件，不讓不同 section 各自演化。

## 12. Delivery checklist

沒有既有文件慣例時，使用 `docs/<topic>-design.md`。沿用一份主 Design Doc，不預設另產 AI 版或重複文件。

交付前確認：

1. Reviewer 無須讀原對話即可理解 Why、Scope、Current、Target。
2. What moves / What stays 與 state ownership 是否清楚？
3. Representative before → after 是否足以證明 target model 可落地？
4. Critical implementation mechanics 是否有足夠 code sketch / pseudocode？
5. Protocol / API status 是否準確？
6. Behavior parity 是否有 Baseline → Invariant → Verification？
7. Diagram 是否各自回答明確問題，且與 prose / code sketch 一致？
8. 重要 current claims 是否有可追查 evidence？
9. Constraints / known limitations / open questions 是否保持可見？
10. Migration 是否停在 architecture boundary，而沒有變成 task list？

完成 Design Doc 不代表 implementation 已開始、tests 已執行或 external review 已通過。
