# Architecture Planning

需要描述 target architecture 或 execution planning，且已有足夠 current model 時，按需讀取本指引。互動、evidence 分類、decision gates 與完成契約沿用 `architecture/SKILL.md`；不要求所有取捨已定，也不要求文件。

## Target architecture

由已確認的目標、constraints 與 decisions 推導 target architecture。尚未選定的實質取捨以 alternatives／proposals 呈現，列明需要的選擇與各自影響；可以交付 Draft / Pending Decisions，不將候選方向寫成已選定的 target。

依變更需要說明：

- Current problem、預期結果、scope 與 out-of-scope。
- 元件責任、dependency direction、interfaces／contracts。
- State／data ownership，以及寫入權限、snapshot 或 cache 的角色。
- 重要 data／event flows、lifecycle、failure handling。
- Current 與 target 的差異；以小型 ASCII diagrams 呈現。

Target 是 proposal，不把預期行為描述成目前已存在的 code。每項重要變更對應現有 files／symbols 或明確標示的新元件。需要查平台能力或外部技術限制時，以合適的 primary sources 補足 evidence，區分驗證結果與 inference。

## 執行計畫

使用者要求 execution planning，且相關 decisions 足夠時才展開。未決選擇只阻止依賴它的步驟；可規劃獨立部分，並明列其餘工作的 blockers。不要為讓計畫看似完整而填入依賴未知答案的 tasks。

由 dependencies 與風險安排可獨立 review、驗證的階段，不依檔案清單機械性排序。每階段交代與判斷有關的資訊：

| 項目 | 要回答的問題 |
| --- | --- |
| 目的與前置條件 | 這一步解決什麼？依賴哪些決策或能力？ |
| 變更位置 | 影響哪些現有 files／symbols、contracts 或資料？ |
| 行為與 invariants | 什麼要保留？什麼是已確認可改變的行為？ |
| Verification | 哪些現有 tests、建議 regression cases 或手動驗證能判定成功？ |
| Failure／migration | 失敗如何處理？需要哪些過渡或恢復步驟？ |
| Decision point | 哪項新發現會需要使用者重新選擇方向？ |

計畫細節依變更規模調整。未知平台行為若可能推翻選型，先指出需要驗證的最小問題、預期觀察與選擇條件；不要假裝已完成 spike。未解決的關鍵決策不能被藏進 implementation task。

## VERIFY 與結果交付

交付前對照：

- 已形成的設計是否符合目標、invariants 與已確認的選擇？
- 已規劃的 flow、ownership 或相容性變更是否有對應 verification？尚未能規劃的部分是否有明確原因？
- 引用的 code locations、依賴與相關 tests 是否仍符合目前讀到的 code？
- Remaining decisions、risks 與 unknowns 是否清楚？各自阻止哪些後續工作？

記錄實際檢查結果與限制；未執行的檢查只列為 strategy。依主 skill 的完成契約交付 Resolved、Draft / Pending Decisions 或 Blocked；Draft 是有效停點，不要求使用者先特別請求 draft。是否保存文件，另依主 skill 的可選文件交付規則處理。
