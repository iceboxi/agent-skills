---
name: design
description: Design a concrete, implementable software solution for a new feature or refactor from repository evidence and requirements. Produce a Markdown Design Doc with architecture, ownership, interfaces, runtime flows, migration, estimates, and verification. Use before implementation; do not merely reformat an already-decided design.
---

# Software Design

本 skill 負責 **software design 本身**。輸入通常是 requirement + repository；輸出是可獨立 review、可實作的 Markdown Design Doc。

預設使用繁體中文，保留 code identifiers、API names 與 repository terminology。

## Contents

- Core contract
- Evidence discipline
- Degrees of freedom
- New feature vs refactor
- Architecture & visual coverage
- Interfaces & ownership
- Decisions & uncertainty
- Migration / estimates / verification
- Design Doc output
- Self-correction loop
- References

## 1. Core contract

Design 必須：

1. 理解 requirement、scope、non-goals、compatibility constraints；先讀 relevant `GLOSSARY.md` / `GLOSSARY-MAP.md` 與 ADR，沿用既有 domain language，不重新爭論已 accepted durable decision。
2. 讀取 relevant repository code；缺 current model 時先做必要 explore。
3. 找出 responsibilities、dependencies、state ownership、extension points 與主要 runtime flows。
4. 先建立 target responsibility model，再決定 abstraction / protocol / pattern。
5. 用足夠的 architecture / sequence views 讓 reviewer 看懂 **placement、ownership、interaction、migration**；不要用 table 取代本來需要圖才能理解的 relationship。
6. 只有在確實解決 seam / ownership / testability / extensibility 問題時才引入 abstraction；需要判斷 module depth、locality、interface surface 時使用 `codebase-design` discipline。
7. 提供可 review 的 concrete interfaces / type sketches，並對已確認的「可擴充／易維護」目標用代表性 change-locality exercise 驗證修改半徑。
8. 對 refactor 提供 Current → Target mapping、behavior invariants 與 migration。
9. 從 architecture dependency 與 migration safety 推導 implementation phases。
10. 提供 engineering estimate 與 verification / regression strategy。
11. 主動處理會改變 architecture / migration / estimate 的 uncertainty；不要只列 Pending。
12. 交付前執行 self-audit；有 architecture gap 就先修文件。

核心流程：

```text
Requirement
    ↓
Repository evidence
    ↓
Current model / integration context
    ↓
Target responsibility & ownership
    ↓
Architecture views
    ↓
Interfaces / runtime flows
    ↓
Migration / phases / estimate
    ↓
Verification
    ↓
Self-audit & revise
    ↓
Design Doc
```

## 2. Evidence discipline

Project-specific technical conclusion 必須來自 repository evidence。

區分：

- **CURRENT**：實際存在的 code / behavior。
- **INTERPRETATION**：由 evidence 推導的 current model。
- **PROPOSED**：尚未實作的 target。
- **CONFIRMED DECISION / REQUIREMENT**：使用者已確認的重要要求或取捨。
- **PENDING**：仍可能改變 target 的 decision。
- **PLANNED VALIDATION**：未執行的 test / spike / prototype。

不要把 proposed API、planned tests 或 target behavior 寫成 current fact。重要 current-state claim 使用 `file:line` + symbol evidence。

## 3. Degrees of freedom

Software design 是高 freedom reasoning task。只鎖死會影響 correctness / comprehensibility 的 invariant。

### Low freedom — 必須遵守

- evidence status 不混淆；
- canonical state 不形成無意義的雙 owner / 雙 writer；
- significant protocol / collaborator 有 purpose、consumer、implementer、placement；
- refactor 的重要 behavior invariant 被保留或明確改變；
- architecture / runtime / migration view 語意清楚；
- placement / interaction 問題不能只靠 prose / table 取代圖；
- 未驗證事項不得寫成已完成。

### Medium freedom — 給 preferred shape

- interface sketch 深度；
- phase granularity；
- diagram decomposition；
- error / lifecycle detail；
- migration / validation strategy；
- file organization。

依 scope / risk 調整，不要求每份 Design Doc 同形。

### High freedom — 由 repository evidence 決定

- pattern 名稱；
- class / protocol 數量；
- concrete type vs protocol；
- naming；
- section ordering；
- helper implementation；
- exact file split。

不要因 skill 形式要求而製造不必要 abstraction 或 governance。

## 4. New feature vs refactor

### New feature

至少回答：

- goal / requirement
- existing integration context
- affected owners / extension points
- target architecture
- state ownership
- interfaces / contracts
- important runtime flow
- failure / lifecycle semantics
- implementation phases
- estimate
- verification

### Refactor

先驗證 premise。成立後至少回答：

- current architecture / responsibility / state ownership
- representative current runtime flow
- concrete coupling / limitation
- target external architecture
- target internal realization
- target responsibility / state ownership
- Current → Target mapping
- representative before → after flow
- migration / transitional architecture（若非一次切換）
- behavior invariants
- implementation phases
- estimate
- regression strategy

若 premise 被 evidence 推翻，交付 **PREMISE REJECTED**，不虛構 target。

## 5. Architecture & visual coverage

**Tables explain properties; diagrams explain placement and interaction.**

Target Architecture Overview 可以簡化，但它只是第一層，不是唯一一層。若 overview 為了清楚省略了重要 internal collaborators / protocols / workflow owners，後續必須用 Design Realization 或局部 architecture view 補回位置感。

對 non-trivial refactor，Design Doc 必須讓 reviewer 能視覺回答：

1. Current problem structure 在哪裡？
2. Target external owner / boundary / dependency direction 是什麼？
3. Target internal collaborators / protocols / state owners 怎麼組合？
4. Representative behavior 在 Current / Target 怎麼流？
5. 有 transitional coexistence 時，新舊 world 怎麼接、何時退役？

**不以固定圖數驗收。** 一張圖可回答相容問題，但不得因「已有 table / mapping」就省略 placement / interaction 所需的圖。

複雜 subsystem（例如 retry / timeout / progress、auto/manual shared mechanics、persistence / background task、multi-step ACK、special workflow）若主圖看不懂 ownership / interaction，增加局部 architecture / sequence view。

Diagram 詳細規則請讀 [architecture.md](architecture.md)。

## 6. Interfaces & ownership

不要從 MVVM / Clean Architecture / Repository 等 pattern 名稱開始。

優先順序：

```text
problem / requirement
    ↓
responsibility boundary
    ↓
state / workflow / policy ownership
    ↓
dependency direction
    ↓
interface / abstraction
    ↓
pattern（only if useful）
```

分別檢查：

- **State ownership**
- **Workflow ownership**
- **Policy ownership**
- **Integration ownership**
- **Presentation ownership**

Single domain / single canonical state owner 不代表所有 workflow 都由同一 class 承擔。

每個 significant protocol / interface 至少說明 purpose、consumer、implementer、responsibilities、non-responsibilities 與 key contract；error / concurrency / lifecycle 在 relevant 時補充。

Consumer-facing boundary 只暴露真實 consumer 需要的 capability。Owner-only mutation、ingress、hydration、persistence、migration control、raw event stream 預設保持 internal / narrower boundary。

詳細 interface 與 abstraction guidance 請讀 [interfaces.md](interfaces.md)。

## 7. Decisions & uncertainty

有實質替代方案時比較：

- ownership / responsibility
- dependency direction
- complexity
- migration impact
- testability
- extensibility
- regression risk

不要為了形式製造假選項。

遇到 uncertainty：

- repository fact：先 `explore`；
- repository 外的 platform / SDK / language / toolchain fact：交 `research`；
- paper reasoning 無法回答的 runtime / state / compatibility / UI feasibility：交 `prototype`；
- requirement / engineering trade-off：若需要 human judgement 且不是單一 targeted clarification，交 `grill-with-docs` 用 decision-tree frontier 收斂，design 不自行 improvising 長訪談；
- effort 大到完整 decision tree 尚不可見：先用 `wayfinder` 清除 architecture fog，再回到正常 design。

若 uncertainty 會改變 target、主要 contract、migration path 或 major estimate，在依賴它的工作前建立明確 gate。Implementation-only detail 不必阻塞 Design Doc。

## 8. Migration / estimates / verification

Design Doc 必須描述 implementation / migration **strategy 與 phases**，但不要把它展開成 ticket-level execution plan。Design acceptance 後，只有工作規模需要 fresh-context work packages / dependency graph 時，才交給 `spec` 產生 implementation spec。

每個設計都需要：

- bounded implementation / migration phases
- engineering estimate
- acceptance / regression strategy

只有 scope / risk 真的需要時才展開：

- feasibility fallback
- shadow / differential validation
- branch / integration coordination
- release / rollout / monitoring
- external resource readiness
- outcome metrics

若 confirmed goal 包含 extensibility / maintainability，extension exercise 不是 project governance，而是 design acceptance evidence：用一個代表性 command / source / policy 變更檢查 locality；詳細 discipline 由 `codebase-design` 提供。

不要把一般 design 擴張成 project / release governance 文件。

詳細 planning guidance 請讀 [delivery.md](delivery.md)。

## 9. Design Doc output

章節可依任務調整，不固定模板，但完成後 reviewer 應能回答：

- 為什麼做？scope / non-goals 是什麼？
- current system 怎麼運作？問題在哪裡？
- target external architecture 是什麼？
- internal collaborators / protocols / state owners 放在哪裡？
- significant abstraction 為什麼存在、誰 consume / implement？
- important runtime flow 怎麼走？
- refactor behavior invariant 如何保留？
- Current → Target responsibility 怎麼搬？
- migration 怎麼安全完成？
- phases / estimate / dependencies 是什麼？
- 每階段怎麼驗證？
- 哪些 unresolved decision 會 reopen design？

有一定規模的 design，最前面提供短 overview：問題、預期成果、Current → Target、遷移順序、總 effort、最大風險 / gate、待決事項。不要為了格式硬湊一頁。

## 10. Self-correction loop

交付前執行一次 design audit，發現 gap 就修訂後再檢查。

至少檢查：

- [ ] major responsibility 都有 owner；
- [ ] canonical / draft / workflow / temporary state 沒有不明雙 owner；
- [ ] significant protocol 有 purpose + consumer + implementer + placement；
- [ ] Current / Target / runtime / migration views 已覆蓋本次真正重要的問題；
- [ ] 沒有 responsibility table 正在替代需要的 relationship diagram；
- [ ] representative before / after behavior 可比較；
- [ ] migration bridge 若存在，有 scope / owner / retirement condition；
- [ ] phase 從 dependency / migration safety 推導，不偷偷新增 architecture decision；
- [ ] PLANNED VALIDATION 沒被寫成 completed evidence；
- [ ] 文件沒有為了 checklist 加入與 scope 無關的 rollout / governance / metrics。

Audit fail 時先修文件；不要只把問題列成 limitation 然後宣稱完成。

## 11. References

所有 supporting references 都直接從本檔連結，不再 nested：

- [architecture.md](architecture.md)：visual coverage、architecture / realization / runtime / migration diagrams。
- [interfaces.md](interfaces.md)：degrees of freedom、ownership、protocol / capability boundary、complexity guardrails。
- `codebase-design` skill：module depth、seam、locality、leverage、change-locality exercise 與 abstraction pressure。
- `research` skill：repository 外的 authoritative technical facts。
- `prototype` skill：以最小 throwaway artifact 解一個 paper reasoning 無法確認的問題。
- `grill-with-docs` skill：repository 中的 HITL decision-tree alignment + domain modeling；用於 target decisions 尚未收斂時。
- `domain-modeling` skill：domain terminology / ADR discipline；design 消費結果，不把 glossary 當 spec。
- `wayfinder` skill：超大型 effort 的 decision map；只在完整 design path 尚不可見時使用。
- [delivery.md](delivery.md)：migration phases、feasibility、estimate、verification 與 conditional delivery planning。

讀取策略：

- architecture / refactor：讀 `architecture.md`；
- protocol / ownership / abstraction：讀 `interfaces.md`；
- migration / estimate / verification：讀 `delivery.md`；
- 大多數 non-trivial design 會需要三份，但不要載入與任務無關的額外規則。

每份超過約 100 行的 reference 應在頂部保留 contents，方便定位。

## 12. Handoff

```text
explore
  ↓
design
  ↓
review
 ┌┴─────────────────────────────┐
 │                              │
ACCEPT                        REVISE
 │                              │
 ├── small / single-session → implement
 │
 ├── durable implementation contract → spec → spec-review
 │       ├── single-context → implement
 │       └── multi-context → work-breakdown
 │              ├── per item → implement
 │              └── whole graph → implement-spec
 │
 ├── accepted decisions need canonical-doc merge → doc-sync
 │
 └── presentation needed → report
                                │
                                └────────→ design
```

Design Doc 是 technical source of truth。若 human decisions 尚未收斂，先回 `grill-with-docs`；Review 負責 design acceptance；`spec` 將 accepted design 忠實轉成 implementation contract；需要多個 fresh-context work items 時再交 `work-breakdown`；`doc-sync` 只同步已決策內容；Report 只做 presentation extraction。Design 已收斂後，不要再用 `design` 做純文件整併。
