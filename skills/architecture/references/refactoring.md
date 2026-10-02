# Refactoring Planning

在 refactor 模式形成 target architecture 與 migration strategy 時讀取本指引。它補充 planning 指引；共通訪談、選項比較與 decision gates 仍由 `architecture/SKILL.md` 定義。

## 先確認保留範圍

從 callers、資料格式、讀寫流程、side effects 與 tests 查明現有 contracts。依任務檢查 identity、ordering、notifications、async／concurrency、error handling、lifecycle、persistence 與外部 consumers；只展開與變更相關的項目。

區分 observed behavior 與應保留的 invariant。若既有行為看似有問題，不能自行判定可以改變。需要使用者確認哪些行為必須保留、哪些可改變，以及相容性與 migration cost 的界線。允許的行為變更在計畫中獨立標示。

## 設計 migration

建立 current -> transitional -> target 的最小路徑。不要在 codebase 沒有這種需求時預設 dual writes、adapter、feature flag 或資料格式升級。

必要時用 ASCII 圖解釋每個過渡階段的 dependency direction、state owner 與 read／write paths。逐項交代：

- **Ownership：**每階段的 canonical owner、可寫入者，以及衍生 snapshot／cache；新舊路徑共存時避免兩個互相競爭的 owner。
- **Compatibility：**需要支援的舊資料、API、consumer 或版本，以及明確可接受的限制。
- **Identity／data：**資料或 identity 如何對映，何時轉換，如何處理重試、中斷與失敗；無資料遷移時明確說明。
- **順序：**先建立哪些邊界，再遷移哪些 callers，何時切換主要路徑。
- **Rollback／recovery：**各階段能退回到哪裡。若真有不可逆步驟，先呈現影響與恢復限制，取得對該取捨的決定。
- **Cleanup：**依可驗證的條件移除舊路徑、過渡機制與不再使用的資料；不只寫「之後清理」。

Migration strategy 必須在實作前形成。若證據顯示有多個合理遷移方向，回到共通選項比較與 decision gate；不在步驟安排中默默決定。

## Regression strategy

以外部可觀察行為與重要 invariants 設計 verification matrix：

| 階段／風險 | 應保留或改變的行為 | 現有 evidence／tests | 必要新增驗證 | 成功或恢復條件 |
| --- | --- | --- | --- | --- |

優先沿用既有 tests、fixtures 與可注入依賴。缺少保護網時，指出需要 characterization tests 的行為。過渡與 target 狀態都需要相應驗證；依實際風險涵蓋相容性、保存失敗、中斷、並行操作與 identity 等案例，不套用無關 checklist。

對目前無法自動驗證的項目，列明手動方法、預期結果與限制。不要把 proposed tests、閱讀過的 tests 或文件中的歷史結果描述成此次已通過。
