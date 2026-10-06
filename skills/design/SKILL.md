---
name: design
description: Design a concrete, implementable software solution for a new feature or refactor from repository evidence and requirements. Actively resolve uncertain decisions through exploration and questions. Produce a Markdown Design Doc with target architecture, responsibilities, protocols/interfaces, runtime flows, migration, implementation phases, engineering estimates, and verification. Use before implementation; do not merely reformat an already-decided design.
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
Target responsibility model
    ↓
Minimal architectural spine
    ↓
Architecture views
    ↓
Protocols / interfaces / runtime flows
    ↓
Migration / implementation phases / engineering estimate
    ↓
Verification
    ↓
Design Doc
```

預設使用繁體中文，保留 code identifiers、API names 與 repository terminology。

## 1. Core Design Contract

Design 必須：

1. 理解需求、scope、non-goals 與 compatibility constraints。
2. 讀取 relevant repository code；若缺 current model，先完成必要的 explore 工作。
3. 找出 responsibilities、dependencies、state ownership、extension points 與主要 runtime flows。
4. 先建立 target responsibility model，再抽出最小 architectural spine；不要從所有候選 types 直接組 architecture diagram。
5. 依 scope 選擇必要的 Target Architecture、Design Realization、Runtime Flow、Integration、Migration views；不同 view 的語意不可混用，每個 view 只回答一個主要問題。
6. 只有在確實解決 boundary / testability / extensibility 問題時才引入 abstraction / protocol / pattern。
7. 提供 concrete protocols / interfaces / type sketches。
8. 說明每個重要 abstraction 為什麼存在、解決什麼問題、誰 consume、誰 implement。
9. 讓每個 significant protocol / type 都可從 Design Doc 追查其角色、consumer、implementer 與所在責任邊界；不要求每個 abstraction 都成為 diagram node。
10. 對 refactor 提供 Current → Target 對照與 migration。
11. 從 architecture dependency 與 migration safety 推導 implementation phases。
12. 提供可驗證的 acceptance / regression strategy。
13. 主動透過 explore / 提問釐清影響設計的 uncertain decisions，不只列為 Pending。
14. 提供各 phase / work package 與整體的工時預估，說明 assumptions、dependencies 與不確定性。
15. 產出容易 review 的正式 Markdown Design Doc，依規模提供 overview 與詳細 evidence；Design Doc 是 design 的產物，不是另一個 downstream skill。

### Scale-dependent Planning

Core Design Contract 適用於每個設計，描述深度依 scope 調整；小型變更可用單一 bounded phase 與簡短 sizing。下列 planning 只在對應條件成立時展開，不是每份 Design Doc 的固定章節或提問清單：

| Planning | 適用條件 |
| --- | --- |
| Feasibility gates / fallback | 尚未驗證的關鍵假設若失敗，會改變 target、主要 contract、compatibility、migration 或主要 estimate；小型任務也適用。 |
| Progressive / shadow validation | 高風險的 behavior preservation 或 owner 切換，需要切換前的比較 evidence；依成本選方法，不強制 shadow mode。 |
| Branch / integration strategy | 較長、跨多人或共用修改點需要協調的變更。 |
| Release checkpoints / rollout / monitoring | 跨 release、分批切換或正式環境觀測與回復限制會影響交付安全。 |
| External resource readiness | 設計或驗證實際依賴 device、account、data 或其他外部資源。 |
| Extension exercise / outcome metrics | Confirmed goals 包含需代表性 exercise 驗收的可讀性、擴充能力或 UI separation，或要求可量測改善、ROI 等成果證明。 |

依 evidence 與 confirmed goals 判斷適用性；後續章節與 completion checks 沿用這個規則。未觸發的項目直接省略，不要求逐項填 N/A 或為形式詢問。一般 acceptance / regression、工時預估與影響設計的 uncertainty 仍屬核心責任。

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
- engineering estimate
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
- engineering estimate
- regression strategy

若 premise 被 evidence 推翻，交付 PREMISE REJECTED，不虛構 refactor target。

## 5. Target architecture contract

Target design 必須回答：

- 完成後有哪些主要 responsibility boundaries / owners？
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

### Architecture view discipline

先找出 **minimal architectural spine**：只保留理解長期 responsibility ownership 與 dependency direction 所必需的節點。若拿掉某個 type 後，核心 responsibility model 完全不變，它通常不應出現在 Target Architecture Overview，而應下沉到 realization / integration / migration view。

**Architecture completeness ≠ diagram completeness.** Design 必須完整交代責任與 contract，但 diagram 只保留對該圖問題有辨識力的資訊。重要 abstraction 可以透過表格、mapping、code sketch、runtime flow 或正文被追查，不必全部變成 box / edge。

Target Architecture Overview 可以刻意省略 read / events / command / persistence 等 capability-level details，只要省略後不會扭曲 ownership、boundary 或 dependency direction，且後續 Design Realization / Runtime / Integration 有完整承接。

Target Architecture Overview 預設只呈現：

- 主要 consumers / entry boundary；
- 核心 application / domain owner；
- canonical state owner；
- 對理解 dependency direction 必要的主要 input / output boundaries；
- 長期 dependency direction。

不要把 pure helper、value type、codec、catalog、factory、legacy adapter、framework singleton、DB task、API class、temporary bridge 等全部提升成 peer architecture components。

不同 abstraction levels 必須有明確分層。必要時可以出現在同一張圖，但必須視覺分組，且該圖仍只能回答一個主要 architecture question；不得把 call graph 當成 architecture diagram。

Target Architecture Overview 優先使用 **responsibility layers / owner groups** 表達長期結構，不把每個 capability protocol 都畫成 peer node。像 read、events、commands、persistence 這類 capability，若只是 realization detail，應留到 Design Realization；只有它本身代表一個需要被 reviewer 理解的長期 architecture boundary 時才升到 Overview。不要為了少畫 concrete types，反而創造沒有實際 owner / type / boundary semantics 的抽象節點。

若多個 concrete types 扮演同一個 architecture role，在主圖合併成一個 responsibility node，並以 adjacent table / mapping 列出 concrete realizations。只有當 type 之間的差異本身影響 ownership、dependency 或重要 contract 時，才拆成多個 nodes。

至少概念上區分下列 views，依 scope 選擇需要的圖，不要求每案都各畫一張：

| View | 回答的問題 |
| --- | --- |
| **Target Architecture Overview** | 長期 responsibility boundaries 與 dependency direction 是什麼？ |
| **Design Realization** | architecture boundary 由哪些 protocols / concrete types 落實？ |
| **Runtime / Sequence Flow** | 一個 representative scenario 實際怎麼流動？ |
| **Integration View** | target 如何接既有 framework / DB / network / BLE / system infrastructure？ |
| **Migration / Transitional View** | current 如何安全走到 target？哪些 facade / bridge / adapter 只是過渡？ |

**Target Architecture 不等於 Design Realization，也不等於 runtime call graph。**

Migration-only facade、bridge、dual-read / shadow helper、temporary adapter 不得出現在 Target Architecture Overview；放入 Migration / Transitional View。終態仍需保留的 legacy adapter 可出現在 Integration View，但只有當它本身是長期 responsibility boundary 時才升到 Overview。

Integration View 應 **停在 target 與 existing infrastructure 的整合邊界**。對本次設計不修改的 legacy internals，優先收斂成例如 Existing BLE Infrastructure、Existing Persistence Infrastructure、Existing Lifecycle / Data Infrastructure 等邊界節點；其具體 manager、task、database、API class、payload wrapper、singleton chain 放在正文或 appendix。只有當某個 legacy internal 的 ownership、ordering、contract 或 replacement 本身就是本次 design decision 時，才展開其內部節點。不要把「需要保持不變」誤畫成「需要成為 target architecture 的一部分」。

### Ownership dimensions

不要把「同一 domain」誤解成「同一 owner」。設計時分別檢查：

- **State ownership**：誰持有 canonical state？
- **Workflow ownership**：誰負責 operation / sequence / retry / progress？
- **Policy ownership**：誰決定 business / feature-specific behavior？
- **Integration ownership**：誰接 legacy framework、DB、network、BLE、OS？
- **Presentation ownership**：誰管理 UI state / draft / rendering / interaction？

**Single canonical state owner does not imply ownership of every workflow that operates on that state.**

如果一個核心 service 開始同時吸收 unrelated workflows、UI sequencing、feature-specific policy、migration mechanics 與 infrastructure details，應重新檢查 boundary；不要只是靠 extensions / 多檔案把 god object 拆散。

### Complexity and implementation organization

方案的複雜度必須有具體依據：區分 canonical state owner、純 helper / value type、boundary、workflow 與 temporary bridge；說明新增元件的收益、接線與維護成本，以及現有 type 為何不足。不能單以 class / protocol 數量判定過度設計，也不能只宣稱「少數 concrete types」就省略成本說明。

核心元件涵蓋多組 policy / behavior 時，提出具體的檔案、extension 或方法分組、允許承擔的責任，以及何時需要重新檢查 responsibility boundary。邏輯上的單一 owner 不代表所有 implementation 都集中在一個檔案；拆檔也不自動解決 god object。警戒條件可包含無關 workflow 持續加入、每個新 feature 都需修改核心 policy、或 side effects 開始跨越既定 boundary；不設定通用行數或元件數上限。

終態仍保留的 legacy inheritance / adapter dependency，明列用途、可觸及的 API、限制與退役條件；不能因 live facade 已刪除，就把剩餘相容成本視為不存在。

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

### Capability-minimal boundaries

Consumer-facing protocol 只暴露該 consumer 類別真正需要的 capability。不要因為同一 service 內部支援某操作，就自動把它加入共用 client protocol。

逐一檢查 public / shared boundary 的 operations：

- 哪些 consumer 真的需要它？
- 它是一般 consumer capability，還是 owner-only mutation？
- 它是 runtime ingress / hydration / callback handling 嗎？
- 它是 persistence / upload / migration / administrative operation 嗎？
- 暴露後是否讓 UI / feature code 可以繞過 intended owner 或 invariant？

Owner-only mutation、ingress、persistence coordination、migration control 預設保持 internal / narrower capability surface；只有多個真實 consumers 都需要時才提升到 shared protocol。

避免建立「萬能 Client」：read、observe、command、canonical merge、persistence、upload、reset、migration control 不應只因屬於同一 domain 就全部暴露在一個 consumer-facing interface。

### Abstraction traceability without diagram inflation

每個 significant protocol / type 必須可被追查，但不要求出現在 diagram。至少讓 reviewer 能從以下任一形式找到它的角色與接線：

- Target / Current responsibility mapping；
- Design Realization diagram 或 table；
- protocol / type contract table；
- Runtime / Sequence Flow；
- Integration mapping；
- Migration / Transitional mapping；
- 具體正文或 code sketch，且能指出 consumer / implementer / owner。

Migration-only adapter / facade / bridge 只在 Migration mapping 中出現是合理的；existing infrastructure adapter 只在 Integration mapping 中出現也不算 orphan。

如果 reader 看完 abstraction 還不知道「為什麼存在、屬於哪個 responsibility、誰使用、誰實作／持有」，design 不完整。反之，已能透過 table / mapping 清楚追查時，不要為了形式再把它塞進 diagram。

## 7. Diagrams

Markdown Design Doc 預設使用 Mermaid。

先決定這張圖要回答哪個問題，再選節點。**不要從 type 清單出發畫圖。**

Target Architecture Overview 應先畫 minimal architectural spine；supporting collaborators、capability protocols、integration details 與 transitional components 分別放到對應 view。Overview 優先讓 reader 一眼看出 **layer / ownership / dependency direction**，不是列出所有合法 dependency。

Diagram 只畫對該問題有區辨力的 nodes / edges。多個 types 若共享同一 responsibility，先合併；具體成員、次要依賴與例外放 adjacent table / text。Design Realization 也不應退化成完整 wiring graph。

Static dependency、runtime call、callback / event delivery、data flow 不得在同一張圖用同一種箭頭混合表達。若必須同圖呈現，使用明確 legend / line style；若需要長篇文字才能解釋箭頭方向，應拆 view 或改用 sequence diagram。

Current Architecture 與 Integration View 都只展開到本次問題需要的深度。Current view 聚焦造成問題或限制 target 的 current responsibilities / dependencies，不必完整重畫整個 legacy system。

Integration View 只畫到必要的 existing-system boundary；**未修改且其 internal ownership / ordering / contract / replacement 不屬於本次 design decision 的 legacy tree 不展開**。若既有 internal 雖不修改，但其 ordering 或 contract 是設計成立的必要條件，可展開到足以表達該 decision 的程度。其餘由哪些舊 classes / tasks / APIs 落實，用文字、表格或 appendix 說明，不把它們全部搬進主圖。

Diagram 若需要一句以上文字解釋「看起來有 cycle，但其實不是」、「這個 dependency 只是 runtime call」或「這些 nodes 其實不是同一層」，優先重新檢查 view / dependency direction，而不是只補註解。若實際沒有 dependency cycle，但圖因 layers 被 flatten 而看起來有 cycle，重畫成 layer-oriented view；不要把視覺混亂當成架構複雜度本身。

依 scope 選擇**最少但足夠**的 diagrams；不是每個 conceptual view 都必須有圖。若 table / mapping / code sketch 更清楚，就用它取代 diagram。

### Refactor 常見需要
- 一張 scoped Current Architecture **或** current responsibility mapping，足以說明 problem / coupling；
- 一張 Target Architecture Overview，呈現 minimal architectural spine；
- 一個 representative before → after runtime flow，當 behavior / ordering 是設計關鍵時；
- Current → Target responsibility mapping；
- 只有在 concrete placement 難以從表格理解時才加 Design Realization diagram；
- 只有存在 temporary facade / bridge / adapter 且其遷移關係難以文字表達時才加 Migration / Transitional diagram。

### New feature 常見需要
- Existing Integration Context；
- Target Architecture Overview；
- Important Runtime / Sequence Flow（當 interaction / lifecycle / side effect 重要時）；
- Design Realization diagram 只在 protocol / concrete placement 真正需要視覺化時加入。

若 lifecycle / state transition 重要，再加入 state diagram。若同一資訊已由 table / sequence flow 清楚交代，不重複畫另一張 box diagram。

圖中的 component / protocol 名稱要與本文與 code sketch 一致，不另造第二套 vocabulary。

每張圖回答一個主要問題；不要把整個系統塞成一張巨型圖，也不要為了滿足 traceability 把所有 types 都畫進去。

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

### Uncertain decisions

遇到會影響 scope、architecture、ownership、contract、compatibility、migration 或工時的 uncertainty，主動縮小未知範圍：

- **Repository facts / current behavior**：先做有明確問題與範圍的 explore，查 relevant code、callers、tests、config 與 runtime path；不要請使用者猜 repository 可以查證的答案。Explore 只交付 current-state evidence，target decision 仍由 design 負責。
- **Requirement / product / engineering trade-off**：repository 無法決定時，儘早提問，說明待決定事項、可行選項、recommendation、理由，以及對 behavior、compatibility、migration 或工時的影響。使用者已有答案或已授權該 engineering trade-off 時沿用既有授權，不重新要求確認。
- **Technical feasibility**：先查既有 implementation / tests；仍不足時，依任務授權執行有範圍的 spike / prototype，或列出具體 validation plan、判定標準與 reopen condition。未執行的 validation 不得寫成已解決。

使用可用的提問工具；沒有時直接提出具體問題。等待答案時繼續不依賴該答案的查證與設計，不把未回覆當成同意，也不先落定受影響的 target。

重要 decision 保留問題、evidence / options、採用結果或 Pending 原因、影響範圍與解除條件。若問題尚無法解決，明確標示是否 design-blocking，以及下一個 explore、提問或 validation action。

### Risk-first feasibility gates

僅在上述關鍵假設尚未驗證時建立 gate；已有足夠 code / test evidence 支持可行性時，不為形式新增 spike 或 go/no-go。

依假設不成立的影響分類：若會改變 target、主要 contract、compatibility strategy、migration path 或主要 estimate，必須在投入依賴它的工作前安排 go/no-go；不能因需求已明確，就把技術上的關鍵假設降成 implementation detail。

每個重大 gate 說明要查證的假設、所需 evidence / spike、通過與停止標準、最早驗證時點，以及失敗時的 decision / fallback 與重估範圍。Fallback 必須足以評估受影響的接線、遷移與成本，不只寫「改用其他方案」。

核心方案可行性尚無足夠依據時維持 draft 並主動 explore / 提問。可延後的 validation 必須有明確的 stop / reopen condition；不要求所有 implementation 或 device regression 在設計前完成。

仍有 design-blocking Pending 時，只能交付清楚標示 blocker 的 draft，不得宣稱 Design Doc 已完成、可實作或已核准。不要用未確認的 assumption 填滿 target 來繞過提問。

Implementation-only details 不需要阻塞 Design Doc。

## 11. Implementation phases are part of design

Implementation / migration sections 與 phases 屬於 Design Doc，不要求另一份 standalone implementation plan。

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
- Engineering estimate / sizing assumptions

避免 big-bang；但也不要為了「incremental」製造 dual owner / dual writer。

若某個 phase 需要 temporary bridge，明確說明其 scope、owner、retirement condition。

### Progressive validation

對高風險的行為保留或 owner 切換，評估切換前可取得 evidence 的方法，例如 golden fixtures、differential tests、trace replay 或 read-only shadow compare；依 side effects、輸入可重現性與整合成本選擇，不強制每案加入 shadow mode。

單一 writer 的 invariant 不等於只允許一條計算路徑。若採 shadow compare，明列相同輸入、前置 state / identity / ordering、比較欄位、允許差異、差異記錄與停止條件；shadow 只操作隔離的複本或 derived result，不送 command、不寫入正式 storage、不通知正式 consumers，也不成為可寫的 live state owner。說明執行環境、額外負擔與移除條件；read-only compare、只啟用一條正式路徑的 feature flag、以及同時啟用雙 writer 必須分開判斷。

### Delivery planning

依第 1 節的適用條件，只展開與本次變更相關的 delivery planning：

- branch / integration 策略、共用大檔的修改協調與 merge conflict 處理責任。
- 可 build / 可 release 的 checkpoints、rollout 單位與順序；內部 phase 不自動等於可獨立 release。
- 相關 crash / 行為監控、基準、停止與回復條件；區分 code rollback、in-flight operation 停止，以及已發布版本的回復限制。
- 外部驗證資源的到位狀態、確認責任與所需時點；缺少時可繼續哪些工作、何時必須停止整合或切換。

沿用既有交付與監控能力。未知的資源或 release 決策主動查證 / 提問，不預設新建 infrastructure；planning 不授權實際 branch、release 或外部操作。

### Engineering estimate

Design Doc 必須包含可追溯至 phases / work packages 的工時預估：

- 各 phase / major work package 的 effort range 與整體總 effort，使用一致的人時或人日單位；使用人日時說明每日工時基準。
- 說明估算依據與 assumptions，例如修改範圍、既有可重用機制、技術熟悉度，以及所需 exploration / spike、implementation、review、regression、device validation 與 migration 工作。
- 列出主要 dependencies、可平行工作、等待外部資源的時間，以及會改變 estimate 的 risks / unknowns；避免重複計入共用工作。
- 區分 **effort** 與 **calendar duration**。若提供完成時程，另列人力配置、工作日與 dependency assumptions；不得把人日總和直接當完成日期。
- Estimate 是依目前 evidence 推估的 planning range，不是實測結果或承諾；標示不確定性與需要重新 sizing 的條件，不製造假精確數字。

高風險或一次跨多個 boundary 的 phase，將 major work packages 分開 sizing，讓 implementation、整合、可行性驗證與 regression 的成本可追查；只有 phase 總區間不足以支持 estimate。說明未知項目是否已涵蓋、若 gate 失敗哪些工作要重估；不套固定 buffer 百分比。

若 uncertainty 會實質改變估算，主動 explore / 提問。可依明示 assumptions 提供 provisional range；連合理區間都無法估計時，列出缺少的資訊與取得方式，交付 draft 並標示 sizing 尚未完成，不省略 estimate 就宣稱 Design Doc 完成。

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

### Outcome and extension acceptance

每個設計都將 confirmed goals 對應至 observable acceptance evidence。若 goals 包含可讀性、可擴充性或 UI separation 等能力，再以代表性的 extension / integration exercise 驗收：選定 scenario、baseline、預期修改範圍、驗證方法與完成標準，證明新的接點能支援所承諾的能力，而不只檢查 type 已建立或 legacy symbols 已刪除。

可依任務使用最小 command / 頁面接線、替代 consumer 或 test harness；先確認 scenario 的 scope 與外部支援，不強制新增 production 功能或變更 firmware。若能力本身影響核心方案可行性，提早以最小 slice 驗證，最終驗收仍需完整 evidence。

說明預期收益與投入為何合理，不要求每個設計都有 ROI 或量化指標。若 confirmed goals 要求可量測改善或 ROI，有資料才量化；缺少 baseline 時列出採集方法、指標與驗收方式，不虛構改善百分比。Planned exercise 不代表已完成的成果。

## 13. Design Doc output contract

### Layered reading

有一定規模的設計，最前面提供約一頁 overview：問題與預期成果、scope、最小 Current → Target / integration context（可用圖或短 mapping）、遷移順序、總 effort、最大風險 / go-no-go 與待決事項，讓 reviewer 先理解從哪到哪、怎麼走。簡單設計可用短摘要，不硬湊一頁或重複正文。

正文聚焦 design decisions、contracts 與驗證方式；詳細 caller 清冊、完整 code sketches、line references 與補充 traces 可放附錄，正文保留關鍵 `file:line` 或可追查的 evidence links。摘要、正文、圖與附錄必須使用一致的 component 名稱與 decision status，不因壓縮篇幅省略 blocker。

章節可依任務調整。Core Design Contract 的完成檢查必須能回答與本次設計相關的問題：

- 為什麼要做？
- scope / non-goals 是什麼？
- 現在怎麼運作？
- current limitation 是什麼？
- target architecture 的 minimal spine 是什麼？Overview 是否只保留理解 ownership / dependency direction 必要的資訊，沒有把 capability protocols、realization / integration / migration details 錯塞成 peer nodes？
- responsibility / state / workflow / policy / integration owner 怎麼分？
- 每個新 protocol 為什麼存在？其 capability surface 是否只包含 consumer 真正需要的操作？
- significant protocol / type 是否可透過 diagram、table、mapping、contract 或 runtime flow 被追查？是否避免為 traceability 強迫每個 abstraction 成為 diagram node？
- Current / Integration views 是否只展開到設計需要的深度，沒有把與本次 decision 無關的 legacy internals 畫成核心架構？
- important runtime flow 怎麼走？
- failure / lifecycle 怎麼處理？
- refactor 怎麼安全遷移？
- implementation 如何分階段？
- 各 phase / work package 與總工時是多少？估算依據、單位與 uncertainty 是什麼？
- 每階段怎麼驗證？
- 哪些 decision / limitation 仍 unresolved？
- 不確定決策做過哪些 explore / 提問 / validation？哪些仍會阻塞設計？
- 新增複雜度為何合理？核心元件涵蓋多組 policy / behavior 時，responsibility 警戒條件是什麼？
- 驗收如何證明 confirmed goals？預期收益與投入為何合理？
- 圖是否比正文更容易理解？若移除某些 nodes / edges 而不損失 architecture meaning，是否應改放 table / text？

Scale-dependent Planning 僅在第 1 節對應條件成立時補充檢查：

- 有重大未驗證假設時，何時 go/no-go？失敗後怎麼調整 target、migration 與 sizing？
- 有高風險行為保留或 owner 切換時，切換前如何取得 evidence？
- 有交付協調或 release 風險時，相關 integration / release / rollout / monitoring 怎麼安排？
- 依賴外部驗證資源時，到位狀態、責任與所需時點是什麼？
- 承諾需 exercise 驗收的能力或量化成果時，exercise / metrics 如何證明達標？

核心與已觸發的條件式問題若無法回答，Design Doc 尚未完成；未觸發的 planning 不構成缺漏。

將 Design Doc 寫成 Markdown 檔案並交付路徑，標示文件版本或基準與狀態，以及 acceptance basis：

- **Technical acceptance**：對該版本 Design Doc 的 `ACCEPT` / `ACCEPT WITH NON-BLOCKING NOTES` review，預設即建立 accepted baseline；既有使用者對整份版本的明確接受也可作為依據。
- **Business / process approval**：只有使用者或專案流程明定需要另一層 approval 時，才在相應交接前取得；不預設再問一次「是否 approve」。

預設 accepted Design Doc 即 `report` 所稱的 Approved Design Doc。作者自行宣稱完成、個別 CONFIRMED DECISION 或其他版本的 acceptance，不代表目前整份文件已接受；technical decisions 改動後，受影響範圍須重新 review / 接受。

## 14. Handoff

完成 Design Doc 後：

```text
design
   ↕
 review
   ↓ ACCEPT / ACCEPT WITH NON-BLOCKING NOTES
Accepted Design Doc
   ├──→ implementation
   └──→ report → presentation
```

`review` 是獨立 acceptance gate；若 verdict = REVISE，回到 design 修正受影響的 decision / section，而不是由 reviewer 重做 target。

`report` 只能從已接受版本的 Design Doc 提取 presentation，不重新設計 architecture。沿用該版本既有 acceptance，不加第二層 gate；只有明定的 business / process approval 尚未取得時，才補足該程序。

本 skill 不授權 production code implementation、migration、branch、commit 或 release；除非使用者另行明確要求。
