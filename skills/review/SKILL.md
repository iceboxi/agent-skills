---
name: review
description: Independently review a technical design or an implementation spec against its authoritative baseline. Use as an acceptance/fidelity gate; challenge the artifact, classify findings, and return ACCEPT, ACCEPT WITH NON-BLOCKING NOTES, REVISE, or BLOCKED. Do not redesign, implement, or perform routine code review.
---

# Technical Design Review

對既有 technical design、technical design proposal 或 Design Doc（含 implementation / migration sections）做獨立、evidence-based review。目標不是延續作者的 reasoning，而是判斷既有 proposal 是否有足夠依據可以接受並進入下一階段。

**把 proposal 視為尚未受信任，直到 repository evidence 支持它。不要替 proposal 辯護；主動嘗試證偽。**

此 skill 是 acceptance gate，不是第二個 `design` skill，也不是 PR／code review skill。Review 不應替作者完成缺失的 target design。

## 範圍與邊界

適用輸入：

- technical design proposal 或 target technical design；
- `design` 產生的文件；
- Design Doc 內的 implementation / migration **strategy**；
- 已接受 design 的 scope-drift / extension-quality review；
- 使用者要求「review／驗證／accept 這份設計」且重點是 technical boundaries、ownership、contracts、migration 或 regression strategy。

不適用：

- 尚未形成 proposal、需要從零探索 target 的工作：使用 `design`；
- 撰寫或重整 Design Doc：使用 `design`；
- implementation spec：仍使用本 `review` skill，但切到 [spec-fidelity.md](spec-fidelity.md)；execution graph / tickets 由 upstream `to-tickets` 的 human review gate 負責；
- PR diff、局部 code quality、style、bug review：使用 `code-review`；
- 實作、migration、branch、commit 或 production code 修改。

Review 不自行重新設計。發現 design-blocking 問題時，指出問題、evidence、影響與需要重開的 decision；若需要 alternatives 或新的 architecture decision，交回 `design`。可以描述「哪個 boundary 不成立」，但不要在 review 中偷偷建立替代 target。

讀取適用的 global／project instructions、review subject、其引用的 confirmed goals／scope／decisions，以及與主要 claims 相關的 repository code 和 tests。文件是 review subject，不是 current behavior 的權威來源；CURRENT claims 必須以 repository evidence 查證。

## Review 工作模型

維持以下分類，不把不同狀態混在一起：

- **confirmed constraints**：使用者已確認的 goals、scope、decisions、invariants。
- **proposal claims**：review subject 對 target、ownership、dependency、contract、migration 的主張。
- **observed evidence**：實際 repository code／tests 支持的 current facts。
- **findings**：proposal 與 constraints／evidence 間的 contradiction、gap、risk 或 unsupported claim。
- **implementation details**：不改變 target responsibility、ownership、dependency 或 contract 的後續細節。
- **unknowns**：目前 evidence 無法回答的事項，並標明是否 design-blocking。

Confirmed constraints 是 acceptance criteria。不能因 repository 現況、minimal change 或 reviewer preference 而縮小、弱化或重新解釋 confirmed goal。若 evidence 與 confirmed goal 衝突，這本身是 finding；不要自行改寫 goal。

## Review 流程

```text
IDENTIFY SUBJECT
      ↓
RECOVER CONFIRMED CONSTRAINTS
      ↓
VERIFY REPOSITORY EVIDENCE
      ↓
CHALLENGE PROPOSAL
      ↓
CLASSIFY FINDINGS
      ↓
CHECK ACCEPTANCE READINESS
      ↓
VERDICT
```

流程是 review discipline，不是固定篇章。範圍小時可簡化呈現，但不得跳過 evidence verification 或 verdict。

### 1. IDENTIFY SUBJECT

先確認 review 的 artifact／proposal、版本或基準，以及 review scope。已有清楚 subject 時直接開始，不要求形式上的重新確認。

對 Design Doc 區分 Core Design Contract 與 Scale-dependent Planning；後者只查核 scope、風險或 confirmed goals 已觸發的項目。未觸發相關 planning 的小型 feature，不因缺少 branch / rollout / monitoring / resource plan 或 ROI 而產生 finding；仍會改變 target 的重大未驗證假設不因規模小而免除。

若文件標示 CURRENT／PROPOSED／CONFIRMED TARGET／Pending，保留這些狀態。不要把 proposal 的自我標記當成 acceptance evidence。

### 2. RECOVER CONFIRMED CONSTRAINTS

從 review subject、已有 architecture成果與使用者明確指示提取 confirmed goals、scope、decisions 與 invariants。只把有實際確認依據的內容列為 confirmed；作者 recommendation、候選 API、文件中的 proposed wording 不自動升格。

若 acceptance criteria 本身不清楚到無法判斷 proposal 是否成功，這可能是 BLOCKED；先查已有上下文與 repository，不捏造 criteria。

### 3. VERIFY REPOSITORY EVIDENCE

針對會影響 verdict 的主要 claims 查 code，而不是只 review prose。至少覆蓋與 scope 相關的：

- current owners 與 canonical state；
- dependency direction 與主要 callers／consumers；
- relevant protocols／interfaces 與 concrete implementations；
- lifecycle、async ordering、side effects、failure／recovery semantics；
- representative simple 與 complex paths；
- migration seams、compatibility constraints 與 relevant tests。

重要技術 finding 使用 repository-relative `file:line` 與 symbol。只讀足以驗證 proposal 的範圍，不因 review 重新探索整個 repository。文件 reference 過期或與 code 不一致時，以實際 code 為 current evidence 並指出差異。

### 4. CHALLENGE PROPOSAL

主動嘗試找出 proposal 不成立的條件。依 scope 問：

- Proposal 是否真的達成每個 confirmed goal？
- Minimal-change reasoning 是否偷偷縮小 confirmed goal？
- Proposed owner 是否與既有 canonical owner 衝突或形成 duplicated state ownership？
- Dependency direction 是否產生新的 cycle、反向依賴或不必要 coupling？
- Common abstraction 是否只適合 simple case，卻把 complex case 推成大量 bypass／special hook？
- Common mechanism 是否吸收了應屬 site／feature-specific 的 policy 或 semantics？
- CURRENT facts、interpretations、PROPOSED design、CONFIRMED decisions 是否被混寫？
- Candidate API 是否被誤寫成 accepted contract？
- Design-blocking question 是否被藏在 Pending／implementation detail？
- Error、recovery、concurrency、lifetime 或 ordering 是否與 current behavior 衝突？
- Migration 是否能逐步驗證與 rollback，還是只能 big-bang 後比較？
- Regression strategy 是否真的能偵測 semantic differences，而不只是兩個 implementation 得到相同錯誤結果？
- Proposal 是否新增沒有 evidence 支持的 abstraction、protocol、state owner 或 workflow language？
- Review subject 是否聲稱 tests／prototype／compatibility 已通過，但沒有實際 execution evidence？
- 依文件規模，overview 是否忠於正文，讓 reviewer 能追查 Current → Target、遷移順序與重大風險？
- 需要理解 placement / ownership / interaction 的地方是否真的有 architecture / sequence view；是否用 responsibility table / prose 取代了必要的 relationship diagram，導致 significant protocol / collaborator 雖有描述但沒有位置感？
- 新增元件與 legacy compatibility 的成本是否有理由？單一 owner 是否吸收了無關 policy / workflow；拆檔是否只是掩蓋責任集中？
- 關鍵假設失敗是否會改 target / contract / migration / estimate，卻被列為 implementation gate？Go/no-go 是否早於依賴它的投入；fallback 是否可評估？
- 高風險 phase 的工作包、整合、可行性驗證與 regression 是否能支持工時區間，而不只是列出 phase 總數？
- Owner 切換前的 evidence 是否足夠？是否誤把 read-only compare 當 dual writer、讓 shadow 產生正式 side effects，或讓 feature flag 同時啟用兩條有 side effects 的路徑？
- 依 scope，integration / release / rollout / monitoring 與外部資源是否可執行；rollback 是否忽略 in-flight operation 或已發布版本的限制？
- 可讀性、擴充性或 UI separation 的成果是否有代表性驗收方法；ROI / 改善數字是否有 baseline 支持？
- 若 confirmed goal 是 extensibility / maintainability，是否有代表性 change-locality exercise；普通 command / source / policy 變更是否仍造成 unrelated shotgun surgery？
- Interface 是否 deep enough：caller-facing surface 是否小於它所隱藏的 behavior complexity，或只是 pass-through / middle-man abstraction？
- 若此版由 accepted decisions 回寫而來，新增的 type / method / helper / dependency 是否可追溯到既有 decision；追不到的 exact realization 是否被誤升格成 design contract？

不要為了顯得嚴格而製造 finding。沒有 evidence 支持的疑慮標為 unknown 或 review note，不當成已證實缺陷。

### 5. CLASSIFY FINDINGS

每個 finding 需包含：**severity、claim、evidence、impact、required action**。依下列分類：

| Severity | 意義 |
| --- | --- |
| **BLOCKING** | Proposal 違反 confirmed goal／invariant，ownership 或 contract 不成立，或缺少會改變 target 的必要 decision。不能接受為 implementation baseline。 |
| **NON-BLOCKING** | Target architecture 仍可接受；需要 prototype、implementation review、characterization 或局部 clarification，但不改變主要 ownership／dependency／contract。 |
| **NOTE** | 有價值的 observation、implementation caution 或 coverage gap，不影響 acceptance。 |

不要把 naming、generic shape、access level、private type 拆分等一般 implementation detail 升格為 blocker，除非它實際改變 architecture contract。

依 scope 與失敗影響判斷，不把所有文件都套成大型 migration。摘要、排版或拆檔建議通常是 non-blocking；若缺口阻止 confirmed goal 的驗收、核心可行性判斷或安全遷移，就按既有 severity / verdict 規則處理。列了 Pending、planned spike 或 fallback，本身不代表風險已降為 non-blocking。

若 finding 需要新 alternatives／ownership／contract decision，required action 是「回到 design 的相關 decision」，不是 reviewer 自己選方案。

### 6. CHECK ACCEPTANCE READINESS

在 verdict 前對照與 review scope 相關的核心及已觸發的條件式要求：

1. Confirmed goals／scope／decisions 都有被 target 滿足或明確指出 blocker。
2. 主要 ownership、dependency、technical boundary 有 repository evidence 支持。
3. Representative complex cases 沒有被 abstraction 無聲排除；需要後續 prototype 的部分已標為 non-blocking validation。
4. 沒有 design-blocking choice 被藏成 Pending。
5. Migration 與 regression strategy 足以在 observable behavior 改變時偵測並停下。
6. 文件沒有把未執行的 tests、prototype、compatibility 或 implementation 描述成已驗證。
7. Remaining items 確實是 implementation／verification detail，或已清楚標示會觸發 architecture reopen 的條件。
8. 若 review subject 是 Design Doc，確認有與 phases / work packages 對應的工時區間、總 effort、估算依據與 uncertainty；若提供 calendar duration，已區分人力與 dependency assumptions。缺漏時指出影響並交回 `design`，不由 reviewer 補估或重排 phases。
9. 已觸發的重大 go/no-go、fallback、delivery checkpoints、外部資源與停止 / 回復條件可執行，沒有把會改 target 的假設延後到大量實作後才驗證；未觸發的 planning 不列為缺漏。
10. 成果驗收能證明 confirmed goals；overview 與主要 claims 忠於詳細內容，planned evidence 沒有被寫成已完成。
11. 對 non-trivial refactor，Current structure、Target external boundary、Target internal realization、representative runtime before/after，以及存在 coexistence 時的 transitional wiring，都有足夠視覺覆蓋；table / prose 沒有取代 reviewer 必須看懂的 placement / interaction。

## Verdict

只使用下列四種 verdict：

### ACCEPT

沒有 blocking finding。Target design 足以作為 accepted baseline，並可進入 implementation。仍可列 NOTE，但不要因一般 implementation detail 降級 verdict。

### ACCEPT WITH NON-BLOCKING NOTES

沒有 blocking finding，但有值得在 prototype、implementation 或 verification 階段明確追蹤的 technical risks。每個 note 要說明驗證方式與「什麼 evidence 會要求重新開 design review」。

### REVISE

已有 evidence 證明 proposal 存在 design-blocking contradiction、gap 或 goal mismatch。列出 blocking findings，指出受影響的 sections／decisions，以及需回到 `design` 的哪個問題。不要在 review 中產生 replacement design。

### BLOCKED

缺少必要 artifact、repository evidence、requirements 或 confirmed decision，使 reviewer 無法誠實判斷 acceptance。精確列出缺少什麼、為何影響 verdict、取得後要驗證什麼。Unknown 不自動等於 BLOCKED；只有它阻止 acceptance 判斷時使用。

Verdict 是 review 結果，不代表 production code 已實作、tests 已通過或 release 已核准。

`ACCEPT` / `ACCEPT WITH NON-BLOCKING NOTES` 是 technical acceptance，預設即建立該版本與 review scope 的 accepted baseline，可供已授權的 implementation 使用，不要求使用者再接受一次 review 結果。只有使用者或專案明定另一層 business / process approval 時，才在相應交接前取得；technical acceptance 不取代這類明定程序，也不擴大執行授權。局部 section 的 ACCEPT 不代表未 review 的整份 Design Doc 已接受。

## 輸出格式

先給 verdict 與一段短理由，再列 findings。沒有 finding 時明確寫 `Blocking findings: 0`。建議格式：

```text
Verdict: ACCEPT | ACCEPT WITH NON-BLOCKING NOTES | REVISE | BLOCKED

Reason:
<為何此 verdict 成立>

Blocking findings: <n>
Non-blocking findings: <n>
Notes: <n>
```

接著依 severity 由高到低呈現 findings。每個 finding 包含 claim、evidence、impact、required action。最後列：

- **Acceptance basis**：哪些 confirmed constraints 與 evidence 支持 verdict；
- **Remaining implementation / verification details**：可延後事項；
- **Reopen conditions**：哪些後續 evidence 會使 design 必須重新 review；
- **Next step**：ACCEPT 類型可交接已授權的 implementation / report；明定的額外 approval 仍依流程處理；REVISE 回 design；BLOCKED 補 evidence／decision。

輸出不要求產生另一份 Markdown artifact。使用者要求保存 review 時才寫檔；不要預設建立「review report」。

## 與其他 skills 的交接

```text
design
  ↓
review (design mode)
  ├─ REVISE / BLOCKED → design
  └─ ACCEPT
       ├─ small → implement
       └─ durable contract → to-spec
             ├─ high-risk / multi-session → review (spec-fidelity mode)
             ├─ single-context → implement
             └─ multi-context → to-tickets → implement / implement-spec
```

同一支 `review` skill 有兩種 subject mode：

- **Design mode**：檢查 architecture proposal 是否可接受。
- **Spec-fidelity mode**：讀 [spec-fidelity.md](spec-fidelity.md)，檢查 `to-spec` 是否忠實保存 accepted baseline。

兩者共用同一組 independent review authority、finding severity 與 verdict，不維護第二支 review skill。Spec-fidelity 只在 high-risk、multi-session、multi-agent 或明確要求 durable handoff assurance 時使用；小型單一 context work不設第二道 mandatory gate。

Work graph 的 granularity、blocking edges 與 tracer-bullet sequencing 由 upstream `to-tickets` 自己的人類確認 gate 負責。

## Review discipline

以繁體中文說明與推理，保留 code identifiers、API names 與 established technical terminology。結論要短而明確，finding 要能被 repository evidence 查證。

不要把「我沒有找到問題」寫成「設計一定正確」。Acceptance 表示在目前 scope、constraints 與可取得 evidence 下，沒有 design-blocking finding。

此 skill 不授權修改 production code、Design Doc、agent instructions、branch、commit 或 release。Review 本身也不授權 implementation。
