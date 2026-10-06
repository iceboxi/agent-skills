---
name: design-doc
description: Create or update an independently reviewable Markdown Design Doc that synthesizes existing architecture or refactoring evidence, models, proposals, decisions, implementation mechanics, and verification strategy. Use when a Design Doc is requested or an offer to document architecture results is accepted; do not select this skill merely to persist another workflow's artifact.
---

# Design Document

將已有的 architecture understanding、decisions、evidence 與必要 implementation mechanics 整理成可獨立 review 的 Markdown Design Doc。主要讀者是不熟悉 repository 的工程師，同時讓熟悉 code 的 reviewer 與其他 AI／CLI 能追查 evidence。

這是 downstream architecture synthesis / persistence skill。它保存並具體化已完成或已確認的 architecture reasoning，不自行重做選型，也不因其他 workflow 需要 Markdown 就自動啟用。

## Selection boundary

適用：

- 使用者明確要求 Design Doc / architecture document；
- 已接受把 architecture / refactor 結果整理成可 review 文件；
- 需要把 current / target / ownership / behavior / state / implementation mechanics / verification 保存成長期技術文件。

不適用：

- 只是保存 implementation plan、review report、technical report 或其他 workflow artifact；
- 還需要決定 ownership、target architecture、contracts 或 alternatives：回到 `architecture`；
- 只需要 execution order / batches / rollback / task tracking：使用 planning workflow。

不得藉此修改 production code、agent instructions、CLI settings、開始 migration、commit 或發布。

## Source authority and evidence

接受使用者直接提供的材料，或 `architecture` 已有成果：scope、current model、evidence、decisions、proposals、unknowns、migration / verification strategy。

具體 codebase 的重要 technical claim 應對照相關 code；已提供的 code locations 可能過期，交付前重查重要 references / symbols。若無法查證，保留來源、assumption 或 limitation，不用一般知識補成 project fact。

Design Doc 可以保存：

- Resolved
- Draft / Pending Decisions
- Blocked
- PREMISE REJECTED
- current-state documentation

但不得把 proposal、planned validation、未執行 tests 或未實作 target 寫成 current fact。

## Core Design Questions

Design Doc 不要求固定章節名稱，但必須依 scope 回答足以 review design 的核心問題：

1. **Why / Goal**：為什麼值得改？完成後要解決什麼問題？
2. **Scope / Non-goals**：這次改什麼、不改什麼？
3. **Current**：目前 responsibility、dependency、runtime behavior 與 state 怎麼運作？
4. **Target**：完成後 components、boundaries、ownership 與 dependency 怎麼變？
5. **Change Scope**：哪些 responsibility / state / flow 會搬？哪些刻意維持原位？
6. **Behavior**：runtime ordering、success / failure / recovery、callbacks / events 怎麼走？
7. **State**：有哪些 meaningful state？誰擁有？何時建立、失效、提交、恢復？
8. **Implementation Mechanics**：哪些具體 type / function / algorithm / synchronization 機制是證明設計可落地所必需？
9. **Verification**：如何證明 target 符合設計，且 behavior-preserving refactor 沒有改壞既有 contract？
10. **Pending / Open Questions**：哪些問題仍會影響實作或需要 validation？

Architecture-change proposal 必須在前段提供 **Target Architecture Overview**。不要因 concrete API 尚未定案就省略已有足夠 evidence 支持的 conceptual target。

## Change Profiles

Core Design Questions 是共同骨架；依變更型態增加真正需要的內容，不套固定模板。

### UI / Feature

可視需要包含：

- UX / user journey
- screen / component hierarchy
- UI flow
- view / presentation state
- API interactions
- selectors / analytics / accessibility / test hooks

### Architecture / Refactor

優先包含：

- current → target architecture
- **What moves / What stays**
- ownership / responsibility boundaries
- representative before → after cases
- compatibility invariants
- migration boundary
- behavior parity / regression strategy

### Data / Persistence

可視需要包含：

- schema / model changes
- ownership / consistency
- migration / backward compatibility
- ordering / transaction / failure semantics
- rollback / recovery

### Service / API

可視需要包含：

- API / protocol contracts
- lifecycle
- concurrency / isolation
- error semantics
- backward compatibility
- consumers / implementations

同一份文件可以同時符合多個 profile。

## Reading narrative

Design Doc 是 synthesis artifact，不按 investigation chronology 傾倒證據。

Architecture / refactor 常見閱讀主線：

```text
Why / Problem
      ↓
Scope / Non-goals
      ↓
Current model
      ↓
Target architecture
      ↓
What moves / What stays
      ↓
Representative before → after
      ↓
Contracts / behavior / state
      ↓
Critical implementation mechanics
      ↓
Migration boundary
      ↓
Compatibility & verification
      ↓
Open questions
```

這是 narrative pattern，不是固定目錄。依 scope 合併、刪除或調整。

Reviewer 應該能在前段就理解 target；supporting protocols、flows、implementation sketches、alternatives、history、risks 往後 progressive disclosure。

## Change Scope: What moves / What stays

對 refactor，不能只給 Current 與 Target 兩張架構圖。應明確回答 responsibility / state / flow 到底怎麼搬。

可使用：

| Area | Current | Target | Intentionally unchanged |
| --- | --- | --- | --- |
| committed state | ... | ... | ... |
| draft / edit state | ... | ... | ... |
| operation workflow | ... | ... | ... |
| persistence | ... | ... | ... |

這個 section 的目的，是讓 reviewer 快速辨識 scope boundary 與 accidental redesign。

## Representative before → after

對 architecture/refactor，選 1–3 個代表性 operation / flow，具體說明設計如何落地。

每個 case 應回答：

```text
CURRENT
Who owns the logic/state today?
How does the runtime flow behave?

TARGET
What moves?
What stays?
Who becomes the owner?

INVARIANT
Which externally observable or contractual behavior must stay the same?
```

可使用 table、sequence diagram、state diagram、pseudocode 或 code sketch。

不要為完整而逐一展開全部 callers / panels；選足以證明 responsibility model 成立的 representative cases，其餘用 coverage / inventory 處理。

## Structure, behavior and state

依 scope 選擇互補視角：

| 視角 | 需要呈現的設計問題 |
| --- | --- |
| Structure | components、dependency direction、ownership、protocol、responsibility boundaries |
| Behavior | call ordering、async flow、notifications / callbacks / events、success / failure / recovery |
| State | meaningful states、owner、trigger、transition、guard、invalidation、terminal / error / recovery |

State ownership 是一級設計問題。不要只畫「A 呼叫 B」，還要回答：

- committed state 在哪裡？
- draft / temporary state 在哪裡？
- operation state 在哪裡？
- identity / session state 在哪裡？
- presentation state 是否只是 output，還是另一份 source of truth？

同一份 state 不應因文件方便而被描述成多個 canonical owner。

## Diagrams

Markdown Design Doc 預設使用 Mermaid fenced blocks，讓 topology 可 review、可 diff、可長期維護。

狀態標籤：

- **CURRENT**：repository evidence 支持的既有架構 / behavior。
- **PROPOSED — NOT YET ACCEPTED**：尚未接受的候選。
- **CONFIRMED TARGET**：已確認 target；仍需說明是否已實作。

常用：

| 問題 | Mermaid |
| --- | --- |
| component / dependency / ownership | `flowchart` |
| data flow | `flowchart` |
| ordering / interaction | `sequenceDiagram` |
| meaningful state transition | `stateDiagram-v2` |

規則：

- 每張圖回答一個主要問題。
- 不為完整補造 node / edge / state / message / ownership。
- Current 與 Target 若 behavior 不同，分開畫。
- 箭頭意義不明時，在相鄰 prose 說明是 dependency、ownership 還是 runtime flow。
- sequence 只畫有設計意義的 messages / failure branches，不列每個 function call。
- state diagram 必須指出 owner；sequential steps 不自動等於 persistent state machine。

Design Doc 以 Mermaid source 為 authoritative diagram representation。Static SVG / PNG 可作 preview 或 downstream artifact，但不取代 Mermaid source-of-truth。

## Protocol and boundary contracts

Scope 內真正定義 architecture boundary 的 protocols / interfaces 是主要內容，但不要逐一列舉 repository 所有 protocols。

視需要描述：

- Purpose
- Owner / Layer
- Implemented by
- Consumed by
- Responsibilities
- Non-responsibilities
- Operations / input-output semantics
- Lifecycle / Ordering
- State implications
- Error semantics
- Concurrency / isolation
- Current limitations
- Proposed changes
- Open questions

API / protocol declaration 必須標明：

- **CURRENT API**
- **PROPOSED API — NOT YET ACCEPTED**
- **CONFIRMED TARGET API**

只確認 responsibility 不代表已接受具體 signature。

## Concrete implementation sketches are design material

**不要因內容長得像 code，就把它排除在 Design Doc 外。**

當 implementation mechanics 會影響下列任一事項時，應提供 concrete type / function sketch、pseudocode 或 representative code：

- ownership
- ordering
- state transition
- concurrency / synchronization
- error / recovery semantics
- identity / lifecycle
- serialization / codec behavior
- compatibility
- feasibility of the proposed boundary

目的不是預先完成 implementation，而是讓 reviewer 能在 coding 前檢查 design 是否 coherent。

### Contract-level sketch

可以用簡短 declaration 顯示 boundary：

```swift
protocol SettingService {
    func value(for type: SettingType) -> SettingValue?
    func send(_ command: SettingCommand)
}
```

Declaration 必須搭配語意說明，不能取代 responsibility / ordering / error contract。

### Design-level code sketch

複雜 flow 應可具體到能 review ordering：

```swift
func handleEvent(_ event: Event, session: Session) {
    guard session.isValid else { return }
    let result = apply(event)
    emit(result)
    requestPersistenceSnapshot(result)
}
```

Reviewer 應能從 sketch 問：

- identity 從哪裡來？
- state 何時 mutation？
- event 何時 emit？
- persistence 是否是 gate？
- failure 是否 rollback？
- callback 是否可能重入？

### Implementation-level mechanism

若具體寫法本身就是 architecture decision，可再更具體，例如 lock scope、actor isolation、generation token、transaction ordering。

但 Design Doc 不應：

- 預寫每一個 method；
- 把 production implementation 複製進文件；
- 列出逐檔修改順序；
- 取代 implementation plan；
- 用大量 code 掩蓋未確認的 architecture decision。

判斷原則：

> **Design Doc 的 code 回答「這個設計具體怎麼成立？」；Implementation Plan 回答「用什麼順序把它做完？」**

## Behavior parity and verification

Behavior-preserving refactor 不應只列一串 tests 或 risk。Design Doc 要把 compatibility contract 寫成可 review 的設計內容。

優先使用：

| Behavior | Existing baseline | Target owner / shape | Invariant | Verification |
| --- | --- | --- | --- | --- |
| representative operation | current trace | new owner | what must stay identical | how to compare |

也就是：

```text
Baseline
   ↓
Target owner / implementation shape
   ↓
Invariant
   ↓
Verification
```

Verification 可包含：

- core equivalence：merge / codec / serialization / bytes
- workflow equivalence：ACK / timeout / retry / commit / rollback
- identity / lifecycle：switch / logout / late callback / stale work
- persistence / event ordering
- runtime / integration acceptance

Planned tests 不得寫成 existing coverage。

## Migration boundary

Design Doc 可以說明 migration shape、dependency、compatibility boundary 與 architectural gates，但不取代 execution plan。

Design Doc 可以回答：

- 哪些 ownership 必須 atomic takeover？
- 哪些 caller 可逐批遷移？
- 過渡期允許哪些 bridge？
- 哪些 dual-owner 狀態禁止進 production？
- 哪些 validation failure 會要求 reopen architecture？

Implementation Plan 再負責：

- 實際 work batches
- file / task order
- staffing
- rollback steps
- acceptance execution
- progress tracking

## Alternatives and decision state

Observed facts、interpretations、assumptions、proposed changes、confirmed decisions 與 unresolved questions必須區分。

有意義的 rejected alternative 應記錄：

- alternative
- why considered
- why rejected / deferred
- what evidence or constraint mattered

不要為了完整保留已失去價值的歷史辯論。

若仍有會決定 target responsibility、ownership、dependency 或 contract 的 blocking decision，文件必須維持 **Draft / Pending Decisions**，不能寫成 final target。

## Writing and traceability

以繁體中文寫作。使用短句、active voice、穩定 terminology 與明確條件。Code identifiers、API names 與 established engineering terms保持原樣。

重要 technical description 提供 repository-relative `file:line` / symbol，讓 reviewer 與 CLI 可追查。

Design Doc 必須自己可理解，但與 Technical Report 不同：**evidence / code reference 是正式 review material，不預設隱藏。**

Current fact 與 proposed behavior 分開；tests 區分 existing / planned / executed；保留環境限制與結果來源。

## Cross-reference consistency

Structure、behavior、state、protocol、code sketch、verification 必須描述同一套 design。

Reviewer 應能回答：

- 誰擁有責任 / state？
- 哪個 boundary 定義 contract？
- runtime ordering 怎麼走？
- failure / recovery 怎麼走？
- code sketch 是否真的符合 diagram / prose？
- verification 是否直接驗證 invariants？

若這些表示互相矛盾，修正文件；不要讓不同 section 各自演化成不同 architecture。

## Delivery

沒有既有文件慣例時，使用合適的 `docs/<topic>-design.md`。沿用一份主 Design Doc，不預設另產 AI 版或多份重複文件。

交付前確認：

1. Reviewer 無須讀原對話即可理解 Why、Scope、Current、Target。
2. What moves / What stays 是否清楚？
3. State ownership 是否清楚且沒有 duplicate canonical owner？
4. Representative before → after 是否足以證明 target responsibility model 可落地？
5. Critical implementation mechanics 是否有足夠 code sketch / pseudocode 可 review？
6. Protocol / API status 是否區分 current / proposed / confirmed target？
7. Behavior-preserving refactor 是否有 Baseline → Invariant → Verification？
8. Mermaid topology、prose、code sketch 是否一致？
9. 重要 current claims 是否有可追查 evidence？
10. Migration 是否停留在 architecture boundary，而沒有變成 implementation task list？
11. Open questions 是否保持可見，且標明是否 block implementation？

完成 Design Doc 不代表 implementation 已開始、tests 已執行或 external review 已通過。
