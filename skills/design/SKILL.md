---
name: design
description: Produce a self-contained, fixed-structure Markdown Design Doc from already-decided requirements, implementation spec, tickets, and repository evidence. Use after grill-with-docs, to-spec, and to-tickets when a human-readable technical design/report is needed. Document existing decisions and plans; do not redesign or change the implementation contract.
---

# Design Documentation

`design` 是 **post-spec / post-tickets documentation skill**，不是另一輪 architecture design、requirements interview、spec authoring 或 ticket planning。

輸入為已收斂的需求與技術決策、implementation spec、工作拆分，以及必要的 repository evidence。輸出為可獨立閱讀、適合工程審閱與主管報告的 **Markdown Design Doc**。使用繁體中文，保留 code identifiers 與台灣團隊自然使用的工程術語。

## Contents

- Role and boundaries
- Inputs and evidence
- Documentation workflow
- Fixed document structure
- Architecture and diagrams
- Interfaces and runtime semantics
- Phases, estimates and verification
- Handling gaps and changes
- Completion audit
- References and maintenance

## 1. Role and boundaries

- **Extract / organize / visualize**：只整理已建立的 requirement、architecture decisions、runtime contracts 與 implementation plan，從 repository evidence 解釋 current state。
- **Self-contained**：Design Doc 本身包含理解方案所需的背景、技術決策、圖、code sketch、工時與驗證策略，讀者不必開啟上游文件才看得懂。
- **No ticket exposure**：Design Doc 不列 ticket ID、ticket title、ticket status、tracker URL、ticket-to-phase mapping 或其他 issue-management detail。來源 tickets 可供 skill 閱讀，但不是文件章節或讀者的外部依賴。
- **No second design authority**：不得藉由補圖、補 protocol、估時或重新分組 phase，默默增加新 requirement、state owner、interface contract、runtime semantics、migration strategy、verification promise。
- **Implementation authority**：實作依照 spec、已確認的決策與實作工作拆分；Design Doc 是實作前的說明快照，不是不可修改的 API blueprint，也不構成預設 acceptance gate。
- **Optional artifact**：只有使用者需要這份 Design Doc 時才執行；沒有報告需求，可直接沿 upstream workflow 實作。
- `challenge` / `review` 都是使用者**手動明確呼叫**的選項，不能由 `design` 自動接續、也不構成產生文件或實作的前置條件。

## 2. Inputs and evidence

開始前收集足夠的來源：

1. `grill-with-docs` 已確認的 requirement / scope / domain decisions，相關 ADR、glossary。
2. `to-spec` 產生的 implementation spec：目標、已定義的 architecture / interface / runtime / test decisions。
3. `to-tickets` 的完整工作內容與依賴：用來理解實作順序、migration、驗證和階段範圍；**只供內部彙整，不在 Design Doc 暴露其追蹤結構**。
4. 對應 repository 的 relevant code / tests：支撐 current architecture、integration seam、legacy behavior，重要 codebase-specific claim 使用 `file:line` + symbol evidence。
5. 經確認的 estimates / assumptions / test strategy / prototype outcomes（若存在）。

這些來源是 **writing inputs**，而非報告內需要列出的閱讀前置條件。若 spec / work plan 未完成，指出欠缺哪種輸入；不要自行執行一次新的架構設計或創造 tickets 來填補。

Source priority：明確已確認的使用者決策與目前有效的 spec / ADR；接著是實作計畫與可驗證 repository facts。遇到矛盾時，先標示衝突並追查是否已被後續決策取代；不能自行挑選較喜歡的方案。

在文件中區分：

- **CURRENT**：以 code / tests 證實的現況。
- **DECIDED / PLANNED**：來源已確立的目標與預計做法，尚未實作。
- **ILLUSTRATIVE**：忠於已確立契約的示意語法或簡化視圖，不能默默增加新決策。
- **UNRESOLVED**：來源缺漏、衝突或尚未決定的關鍵事項。
- **VERIFIED vs PLANNED VALIDATION**：已執行驗證不得與預計驗證混用。

## 3. Documentation workflow

1. 讀取所有必要來源，建立 requirement → decisions → responsibilities / contracts → execution / validation 的內部工作摘要。
2. 查 relevant code、tests 以校對 current-state claim；不要把 proposed types 寫成已存在的 class / API。
3. 按固定章節整合為 **一份獨立的技術敘事**：先 Why / Current → Target，再說明 internal realization、runtime、migration、effort。
4. 將實作工作依工程上可理解的里程碑**歸納為 report phases**；保留已規劃的先後、依賴與 gate，不複製或顯示追蹤項目。
5. 依來源建立 architecture / placement / sequence / transitional diagrams；圖可以解釋既有決策，不可以靠圖新創決策。
6. 產出重要 protocol / interface 的具體 contract 與 code sketches（僅限已確認或能由來源忠實表達的 shape）。
7. 檢查每一個圖、contract、phase、estimate 是否都能回到來源找到根據；完成 self-audit 才交付。

## 4. Fixed Design Doc structure

使用以下順序與 heading；按規模調整各節長度，但不要把重要 technical detail 換成空泛摘要：

1. **Executive Summary**：Why、目標、預期成果、Current → Target 摘要、總 effort（若有根據）、主要風險。
2. **Requirements & Scope**：requirements、non-goals、compatibility constraints、已確認的重要取捨。
3. **Current Architecture / Integration Context**：重構說明現況架構、runtime、問題；新功能說明既有系統接點，不虛構不存在的 current counterpart。
4. **Target Architecture**：architecture overview、boundaries、dependency direction、responsibility / state owners。
5. **Design Realization & Interfaces**：內部 collaborators、protocol / function relationship views、具體 interface contracts、代表性 code sketches 與 placement。
6. **Runtime Behavior**：主要 sequence / state views，含適用的 async ordering、lifecycle、error / retry / cancellation semantics；重構時展示 before / after。
7. **Migration & Implementation Phases**：Current → Target mapping、transitional architecture / gates（適用時），以獨立的工程 phase 呈現目標、主要工作、交付與驗證。
8. **Estimates & Risks**：phase effort 與總計（只使用有根據的估算）、assumptions、high risks、re-estimation / stop conditions。
9. **Verification & Acceptance**：existing vs planned unit / integration / device verification、behavior invariants、observable acceptance criteria。

文件不能出現 ticket / issue IDs、追蹤標題、狀態與來源對照表；也不要寫「詳見 spec / tickets 才能理解」的內容。必要的決策、規格與步驟應直接完整寫在本文件。若關鍵資料尚未確立，應直接在相關章節具體標示未決，而不是推定其存在。

## 5. Architecture and diagrams

**Tables explain properties; diagrams explain placement and interaction.**

視任務需要提供 Current / Target external / Target internal realization / runtime before-after / migration views。Target overview 若省略重要 protocol、state owner 或 workflow，應以局部圖補足位置與關係；禁止用表格取代必要的 placement / interaction 圖。

使用 Mermaid 等可維護的 Markdown diagram，並檢查 node、edge、legend、code sketch 命名一致。對實際未 render 或驗證的圖，不宣稱已成功渲染。

詳細規則：[architecture.md](architecture.md)。

## 6. Interfaces and runtime semantics

從已確定的技術內容整理 significant protocol / interface：

- purpose、consumer、implementer、placement、responsibilities / non-responsibilities；
- key methods / data / state owner；
- 必要時補 error、concurrency、ordering、lifecycle、cancellation semantics；
- code sketch 可清楚標 `ILLUSTRATIVE`，但不得引入來源尚未同意的新 public capability。

如果沒有足夠資訊可提供具體 signature，只能展示已確立的最小 contract 並列出缺口；不要捏造看似正式的 Swift / Objective-C API。

詳細規則：[interfaces.md](interfaces.md)。

## 7. Phases, estimates and verification

把來源的執行順序整理成**報告適合的 phase**，不是逐項照抄 issue / ticket。每個 phase 交代 goal、主要變更、相依 / migration gate、可觀察成果、驗證及 effort。保留真正會改變工程風險的 transitional detail。

Estimate 以來源中有根據的數字、區間、assumptions 計算與呈現；缺估算時說明缺口，不憑空生成精確工時。區分人時 / 人日與 calendar duration。

詳細規則：[delivery.md](delivery.md)。

## 8. Handling gaps and changes

- **可直接整理**：同一決策的不同描述、示意圖、資訊重排、用既有 numbers 彙總 phase effort。
- **需標記而不能定案**：source 缺 protocol signature、state owner、exception handling、runtime ordering、migration safety gate、estimate 或出現互相衝突的答案。
- **需要新決策**：交還原本的 requirement / spec / implementation planning flow 釐清，再重新整理文件；`design` 不自作裁決。
- **實作階段發現差異**：允許依實際證據調整 implementation。必要時先更新實作契約或已確認決策，再視報告需求使用 maintenance mode 同步 Design Doc；無需為一般 helper / private API 變動反覆更新文件。

## 9. Completion audit

- [ ] 不讀取其他文件也能理解 Why、Current、Target、重要 interface、runtime、phase、工時與驗證。
- [ ] 沒有 ticket / issue metadata、ticket mapping 或依賴 tracker 才看懂的內容。
- [ ] Current facts 有 repository evidence，Target 與 planned validation 未被說成已完成。
- [ ] 所有重大 state / workflow ownership 與 protocol consumer / implementer / placement 都有清楚說明。
- [ ] 必要的 Current / Target / internal / runtime / migration views 能回答關係問題，沒有被表格替代。
- [ ] Code sketches 沒有自行新增未決 public API、owner、ordering 或 error semantic。
- [ ] Phase 與 effort 忠實濃縮既有工作規劃，沒有創造新依賴或虛構估時。
- [ ] Source conflicts / missing decisions 被具體標註，沒有被美化成已確認。
- [ ] 沒有默默啟動 challenge / review 或將本文件升格為實作唯一權威。

## 10. References and maintenance

- [architecture.md](architecture.md)：diagram coverage、placement、runtime / migration 圖及驗證。
- [interfaces.md](interfaces.md)：從來源整理 protocol、state ownership、lifecycle 與 code sketches。
- [delivery.md](delivery.md)：將工作計畫彙整為工程 phases、工時和驗證。
- [document-maintenance.md](document-maintenance.md)：來源決策或實作調整後，有限範圍同步既有 Design Doc。

讀取策略：architecture/refactor 讀 `architecture.md`；protocol/ownership 讀 `interfaces.md`；phases/estimate/verification 讀 `delivery.md`。非平凡技術設計文件通常三者都需要，重要指引皆列在各檔案前段。

上游 `grill-with-docs → to-spec → to-tickets → implement` 仍是工程主流程；`design` 僅是使用者要求時，在工作拆分後、實作前產生的獨立人類文件。`challenge` 與 `review` 保持手動選用。
