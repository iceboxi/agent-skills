# Architecture Planning

在使用者要求完整架構／refactor 規劃，且 current model 已完成首輪澄清後，按需讀取本指引。互動、evidence 分類與 decision gates 沿用 `architecture/SKILL.md`。

## Target architecture

由已確認的目標、constraints 與 decisions 推導 target architecture。使用者尚未選定的實質取捨維持 proposed 狀態，先回到對應的 decision gate。

依變更需要說明：

- Current problem、預期結果、scope 與 out-of-scope。
- 元件責任、dependency direction、interfaces／contracts。
- State／data ownership，以及寫入權限、snapshot 或 cache 的角色。
- 重要 data／event flows、lifecycle、failure handling。
- Current 與 target 的差異；以小型 ASCII diagrams 呈現。

Target 是 proposal，不把預期行為描述成目前已存在的 code。每項重要變更對應現有 files／symbols 或明確標示的新元件。需要查平台能力或外部技術限制時，以合適的 primary sources 補足 evidence，區分驗證結果與 inference。

## 執行計畫

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

## VERIFY 與文件交接

交付前對照：

- 設計是否符合已確認的目標、invariants 與選擇理由？
- 每個重要 flow、ownership 或相容性變更是否有對應計畫與 verification？
- 計畫中的 code locations、依賴與相關 tests 是否仍符合目前讀到的 code？
- 哪些 risks／unknowns 仍存在？是否阻止完整規劃，或可明確留待 review？

實際執行的檢查記錄結果與限制；未執行的檢查只列為 strategy。資料足夠後把現有成果交給 `design-doc`。若使用者明確要求先交付 draft，保留未決事項與它們阻止的後續步驟，不補造決策。
