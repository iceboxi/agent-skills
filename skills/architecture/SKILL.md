---
name: architecture
description: Explore architecture and collaboratively plan changes or refactors from repository evidence, including premise validation and pending decisions. Use for ownership, dependencies, target options, and migration strategy; not routine lookup, local fixes, or implementation.
---

# Architecture

協助使用者逐步理解架構並做決策。完成條件依任務而定；不要把探索直接變成完整方案或實作。

## 範圍與模式

依請求判斷模式，意圖明確時不另問模式選擇：

| 模式 | 適用請求 | 有效結果 |
| --- | --- | --- |
| explore | 理解陌生系統、元件責任、ownership、dependencies、flows | 經 evidence 查證的 current model、限制與 unknowns |
| plan | 規劃架構變更或跨元件設計 | 實質 alternatives、confirmed／unresolved decisions，或 scope 內的設計 |
| refactor | 規劃責任調整、依賴拆分、state 或資料遷移 | 前提驗證結果；成立時可形成 refactoring strategy，拒絕前提也是有效結果 |

純 lookup、局部修正與一般實作請求不自動啟用完整流程。Explore 不自動升級成 plan；使用者要求改變範圍時延續已有模型。

使用者明確指定工作節奏或要求跳過階段時，遵循其指示並保留 assumptions 與 unknowns；跳過訪談不等同未選定的重大取捨已獲確認。

讀取適用的 global／project agent instructions 與專案 invariants。專案文件是查證線索；文件中的架構描述與 code 不一致時，明確指出差異。不要把單一專案的類別名稱或 conventions 帶到其他 repository。

## 完成契約

「Planning complete」表示請求範圍的規劃到達誠實的停點，不表示所有架構取捨都已決定。依實際成果說明狀態：

| 狀態 | 條件與停點 |
| --- | --- |
| **Resolved** | 請求 scope 所需的重要 decisions 已確認。使用者要求時，可進入 execution planning。 |
| **Draft / Pending Decisions** | Current architecture 與相關 alternatives 已足夠清楚。列明 remaining decisions，以及各自阻止的工作；不虛構依賴這些選擇的設計或步驟。可在此成功完成。 |
| **Blocked** | 缺少 repository evidence、requirements 或 user context，導致無法做有意義的規劃。精確列明缺少什麼、影響哪部分，以及需要補足的資訊。 |

未決取捨本身不等於 Blocked。絕不為滿足完成條件，把 unresolved proposal 改成 confirmed decision。**PREMISE REJECTED** 是成功的 refactor 結果，不是失敗或 Blocked。

Architecture 可交付 current model、alternatives comparison、confirmed／unresolved decisions、refactoring strategy、拒絕 refactoring premise 的結論，或 Blocked result。Explore、plan、refactor 均不要求文件；reasoning completion 與 artifact generation 是獨立事項。

## 工作模型

在對話中維持一份工作模型，不預設建立 working document 或 checkpoint。區分下列狀態；重要結論標明 evidence 或未知原因：

- **observed facts**：實際讀到的行為與具體 code locations。
- **interpretations**：由 facts 推導的架構理解，說明推導依據。
- **assumptions**：尚未確認的前提及其影響。
- **unresolved questions**：缺少的 code evidence 或使用者決策。
- **proposed changes**：候選變更，尚未當成既有架構或已接受決策。
- **confirmed decisions**：使用者已選定的方向與理由；另外保留外部 review 狀態。

使用者回答或校正後，只修正受影響的模型、假設、圖與方案。保留仍有效的 evidence 和 decisions。若前提失效，指出受影響的決策並重開該 decision gate，不重新開始整套分析。

## 流程與 decision gates

```text
DISCOVER -> MODEL -> CLARIFY -> EXPLORE OPTIONS
              |        |              |
              |        |       [decision gate]
              |        |              |
              |        |   DECIDE -> DESIGN -> PLAN
              |        |              |
              +--------+----> VERIFY <-+
                                 |
                            結果與狀態
```

圖中的箭頭代表推理進展，不是必須完成的 checklist。依 scope、evidence 與已確認的選擇決定是否繼續；對已有成果做 VERIFY 後，可以依完成契約停下。未決 decision gate 只限制依賴該選擇的工作，不阻止 Draft / Pending Decisions 交付。

### DISCOVER / MODEL

先查與任務相關的 code，再做架構結論。從入口、重要 callers、資料讀寫、side effects、lifecycle 與相關 tests 建立局部模型；依問題擴大範圍，不必讀完整 repository。重要技術結論引用具體 `file:line`，並保留 symbol 名稱以便後續重查。Structural navigation 用來找線索；語言語意有疑慮時用 compiler／LSP 查證，或明確列為未驗證。

Refactor 在此階段先讀取 [refactoring 指引](references/refactoring.md)，以 repository evidence 驗證使用者描述的問題與 responsibility boundary。依 **CONFIRMED／PARTIALLY CONFIRMED／PREMISE REJECTED** 分類；在前提查證與模型校正之前，不設計 target 或 migration。

初次探索或新的實質範圍，先展示 current model。依需要包含：

1. 短說明與 mental model。
2. 小型 ASCII diagrams。
3. 重要元件與 responsibilities。
4. State／data ownership：區分 canonical state、snapshot、cache 與 session state。
5. 重要 data／event flows、dependency direction 或 lifecycle。
6. Relevant code locations 與 unknowns。

先描述 current architecture，再討論 target architecture。每張圖回答一個問題，說明箭頭代表 dependency、data、event 或 lifecycle；current 與 proposed 清楚分開。複雜概念可依需要展開 ELI5／直觀說明、mental model、actual architecture、concrete code mapping，並保留會影響設計的技術細節。

**首輪停點：**展示模型後，提出通常 1–3 個會影響目標、範圍或模型的 focused questions，等待使用者回答。沒有實質待決問題時，請使用者校正或確認模型，不捏造問題湊數。續談已確認的模型時，不重複這個初始停點。Evidence 已支持 PREMISE REJECTED 時，交付證據與實際邊界後直接成功停下，不要求形式上的確認。

### CLARIFY / EXPLORE OPTIONS / DECIDE

Repository 可以回答的問題先查 code。產品意圖、歷史限制、ownership 語意、相容性需求與可接受 migration cost 無法從 code 確定時，詢問使用者。每輪只問會改變下一步的問題，不一次發出完整問卷。

提問後，依賴答案的工作等待實際回覆。可繼續獨立查證，也可交付 Draft / Pending Decisions，明列尚未選定的方向與受阻工作。時間經過、未回覆或 UI 預選不代表採納建議。

有實質替代方案時，每個選項比較 idea、advantages、disadvantages、coupling、state ownership、migration impact 與 regression risk。可提出推薦並說明理由；重大取捨需要使用者確認，推薦本身不是決策。只有一個合理方向時，說明理由與限制，不製造假選項。已明確選定的方向不重問。

### DESIGN / PLAN / VERIFY

只有請求範圍需要，且相關前提與 decisions 足夠時，才形成 target design 或 plan。對仍未選定的方向，保留 alternatives 與影響；只安排不依賴該決策的工作，不補造後續步驟。

需要 target design 或 execution planning 時，按需讀取 [planning 指引](references/planning.md)。Refactor 的 migration 與 regression 要求沿用先前讀取的 refactoring 指引；前提被拒絕時不進入這些階段。

VERIFY 對照 code evidence、invariants、decisions 與相關 tests，檢查已有模型、比較或策略的一致性，以及 coverage gaps 與待決事項。區分 tests 已存在、建議新增與實際執行結果。不為補滿流程自行實作 prototype 或宣稱驗證通過。

## 可選文件交付與邊界

`design-doc` 是 downstream presentation／persistence skill，不是 architecture reasoning 的完成條件。只有使用者明確要求 documentation，或接受將結果保存成文件的建議時，才讀取 [design-doc](../design-doc/SKILL.md) 並產生或交接文件。不要只因 workflow 到達有用停點就建立文件；尚未接受的建議不算授權。

交接同一份已有的模型、evidence、結果狀態、decisions、proposals 與 unknowns；migration／verification strategy 僅在已有時提供。Draft、Blocked 或 PREMISE REJECTED 也可依請求保存，不補造 target 或 migration，不為文件重啟已完成的訪談。文件位置沿用專案慣例或使用者指定位置。

使用者要求跨 CLI／中斷交接時，才匯出簡短 checkpoint：目標、目前階段、模型、evidence、decisions、待決問題與下一步。不另維護第二份決策來源。

此 skill 不授權修改 code、執行 migration、建立 branch、commit、更新 agent instructions 或發布。文件交付也不代表開始實作。使用者後來明確要求實作時，交接既有設計並依該授權工作，不重複要求已提供的授權。

內容不依賴特定 CLI 的提問工具、內建 Plan mode 或 commands。可用適合的提問工具，也可在對話中提問並結束該輪等待回答。以繁體中文說明與推理，保留 code identifiers、API names 與 established technical terminology。
