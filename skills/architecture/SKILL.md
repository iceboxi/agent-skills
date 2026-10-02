---
name: architecture
description: Explore code architecture or collaboratively plan architectural changes and refactors from repository evidence. Use for current-system models, ownership and dependency decisions, target designs, and migration planning; not routine lookup, local fixes, or implementation.
---

# Architecture

協助使用者逐步理解架構並做決策。完成條件依任務而定；不要把探索直接變成完整方案或實作。

## 範圍與模式

依請求判斷模式，意圖明確時不另問模式選擇：

| 模式 | 適用請求 | 完成條件 |
| --- | --- | --- |
| explore | 理解陌生系統、元件責任、ownership、dependencies、flows | 使用者能理解現況、限制與 unknowns |
| plan | 規劃架構變更或跨元件設計 | 重要取捨已確認，target architecture 與執行計畫可 review |
| refactor | 規劃責任調整、依賴拆分、state 或資料遷移 | 另有明確的保留行為、相容性、過渡狀態與 migration strategy |

純 lookup、局部修正與一般實作請求不自動啟用完整流程。Explore 不自動升級成 plan；使用者要求改變範圍時延續已有模型。

使用者明確指定工作節奏或要求跳過階段時，遵循其指示並保留 assumptions 與 unknowns；跳過訪談不等同未選定的重大取捨已獲確認。

讀取適用的 global／project agent instructions 與專案 invariants。專案文件是查證線索；文件中的架構描述與 code 不一致時，明確指出差異。不要把單一專案的類別名稱或 conventions 帶到其他 repository。

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
DISCOVER -> MODEL -> [展示模型與 focused questions；等待回答]
                        |
                        v
CLARIFY -> EXPLORE OPTIONS -> [重大取捨；等待決定]
                                  |
                                  v
                     DECIDE -> DESIGN -> PLAN -> VERIFY
```

### DISCOVER / MODEL

先查與任務相關的 code，再做架構結論。從入口、重要 callers、資料讀寫、side effects、lifecycle 與相關 tests 建立局部模型；依問題擴大範圍，不必讀完整 repository。重要技術結論引用具體 `file:line`，並保留 symbol 名稱以便後續重查。Structural navigation 用來找線索；語言語意有疑慮時用 compiler／LSP 查證，或明確列為未驗證。

初次探索或新的實質範圍，先展示 current model。依需要包含：

1. 短說明與 mental model。
2. 小型 ASCII diagrams。
3. 重要元件與 responsibilities。
4. State／data ownership：區分 canonical state、snapshot、cache 與 session state。
5. 重要 data／event flows、dependency direction 或 lifecycle。
6. Relevant code locations 與 unknowns。

先描述 current architecture，再討論 target architecture。每張圖回答一個問題，說明箭頭代表 dependency、data、event 或 lifecycle；current 與 proposed 清楚分開。複雜概念可依需要展開 ELI5／直觀說明、mental model、actual architecture、concrete code mapping，並保留會影響設計的技術細節。

**首輪停點：**展示模型後，提出通常 1–3 個會影響目標、範圍或模型的 focused questions，等待使用者回答。沒有實質待決問題時，請使用者校正或確認模型，不捏造問題湊數。續談已確認的模型時，不重複這個初始停點。

### CLARIFY / EXPLORE OPTIONS / DECIDE

Repository 可以回答的問題先查 code。產品意圖、歷史限制、ownership 語意、相容性需求與可接受 migration cost 無法從 code 確定時，詢問使用者。每輪只問會改變下一步的問題，不一次發出完整問卷。

提問後等待實際回覆。可繼續不依賴答案的查證，但不產生依賴該選擇的 target design 或完整計畫。時間經過、未回覆或 UI 預選不代表採納建議。

有實質替代方案時，每個選項比較 idea、advantages、disadvantages、coupling、state ownership、migration impact 與 regression risk。可提出推薦並說明理由；重大取捨需要使用者確認，推薦本身不是決策。只有一個合理方向時，說明理由與限制，不製造假選項。已明確選定的方向不重問。

### DESIGN / PLAN / VERIFY

Explore 可以在 current model 足夠清楚時完成，不要求完整 target design 或文件。

進入 plan 的 DESIGN／PLAN 時，按需讀取 [planning 指引](references/planning.md)。Refactor 同時讀取 [refactoring 指引](references/refactoring.md)，它補充 migration 要求，不重寫共通流程。

VERIFY 對照 code evidence、invariants、decisions 與相關 tests，檢查方案的一致性、coverage gaps 和 verification strategy。區分 tests 已存在、建議新增與實際執行結果。不為補滿流程自行實作 prototype 或宣稱驗證通過。

## 文件交付與邊界

完整 plan／refactor 任務預設包含 Markdown 文件交付。必要 decision gates 完成後，讀取同套 skills 中的 [design-doc](../design-doc/SKILL.md)，交付同一份模型、evidence、decisions、proposals、unknowns、migration 與 verification strategy。不要為文件重啟已完成的訪談。文件位置沿用專案文件慣例或使用者指定位置。

使用者要求跨 CLI／中斷交接時，才匯出簡短 checkpoint：目標、目前階段、模型、evidence、decisions、待決問題與下一步。不另維護第二份決策來源。

此 skill 不授權修改 code、執行 migration、建立 branch、commit、更新 agent instructions 或發布。文件交付也不代表開始實作。使用者後來明確要求實作時，交接既有設計並依該授權工作，不重複要求已提供的授權。

內容不依賴特定 CLI 的提問工具、內建 Plan mode 或 commands。可用適合的提問工具，也可在對話中提問並結束該輪等待回答。以繁體中文說明與推理，保留 code identifiers、API names 與 established technical terminology。
