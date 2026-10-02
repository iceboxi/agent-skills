# Refactoring Planning

Refactor 在 DISCOVER／MODEL 時先讀取本指引，驗證前提後才考慮 target architecture 與 migration。共通訪談、選項比較、decision gates 與完成契約沿用 `architecture/SKILL.md`。

## 先驗證 refactoring premise

把使用者描述的問題拆成可查證的 claims。從實際 implementation、callers、state 讀寫與 side effects，確認問題是否存在，以及責任目前由誰負責。不要從 class 名稱或 refactoring template 推定責任放錯位置。重要結論提供 `file:line` 與 symbols。

| 分類 | Repository evidence 與下一步 |
| --- | --- |
| **CONFIRMED** | Evidence 支持 refactoring premise。繼續 refactoring analysis；成立不表示某個 target 已獲確認。 |
| **PARTIALLY CONFIRMED** | 部分 claims 正確，但實際 problem 或 responsibility 與描述不同。先校正 current model，再針對成立的部分分析。修正若改變目標或 scope，先詢問使用者，不自行換題。 |
| **PREMISE REJECTED** | Evidence 與 premise 矛盾。展示相關證據，說明實際 responsibility boundary，交付拒絕結論並成功停止。 |

Evidence 不足時，不勉強判定 CONFIRMED 或 PREMISE REJECTED。列明欠缺的 repository evidence、requirements 或 user context；若因此無法做有意義的規劃，依完成契約交付 Blocked。

PREMISE REJECTED 時，不虛構 target architecture、不建立 migration phases，也不提議移動已位於預期 boundary 的 code。若存在較窄的 unresolved question，明列該問題與範圍，然後停止；不要把它改寫成新的 refactor 任務。拒絕前提不是失敗或 Blocked。Refactoring template 不能凌駕相反的 repository evidence。

## 先確認保留範圍

只對 premise 成立的部分繼續下列分析。尚未選定的 target choices 回到對應 decision gate，或交付帶 unresolved decisions 的結果。

從 callers、資料格式、讀寫流程、side effects 與 tests 查明現有 contracts。依任務檢查 identity、ordering、notifications、async／concurrency、error handling、lifecycle、persistence 與外部 consumers；只展開與變更相關的項目。

區分 observed behavior 與應保留的 invariant。若既有行為看似有問題，不能自行判定可以改變。需要使用者確認哪些行為必須保留、哪些可改變，以及相容性與 migration cost 的界線。允許的行為變更在計畫中獨立標示。

## 設計 migration

Premise 已查證且相關 target decisions 足夠時，建立 current -> transitional -> target 的最小路徑。可先交付獨立部分的 strategy；未決選擇所阻止的階段保持未規劃，明列原因，不填入虛構步驟。不要在 codebase 沒有這種需求時預設 dual writes、adapter、feature flag 或資料格式升級。

必要時用 ASCII 圖解釋每個過渡階段的 dependency direction、state owner 與 read／write paths。逐項交代：

- **Ownership：**每階段的 canonical owner、可寫入者，以及衍生 snapshot／cache；新舊路徑共存時避免兩個互相競爭的 owner。
- **Compatibility：**需要支援的舊資料、API、consumer 或版本，以及明確可接受的限制。
- **Identity／data：**資料或 identity 如何對映，何時轉換，如何處理重試、中斷與失敗；無資料遷移時明確說明。
- **順序：**先建立哪些邊界，再遷移哪些 callers，何時切換主要路徑。
- **Rollback／recovery：**各階段能退回到哪裡。若真有不可逆步驟，先呈現影響與恢復限制，取得對該取捨的決定。
- **Cleanup：**依可驗證的條件移除舊路徑、過渡機制與不再使用的資料；不只寫「之後清理」。

需要 migration 的實作開始前，必須先形成 migration strategy；refactor session 本身不必達到此階段才算完成。若有多個合理遷移方向，回到共通選項比較與 decision gate，或交付 pending decisions；不在步驟安排中默默決定。

## Regression strategy

以外部可觀察行為與重要 invariants 設計 verification matrix：

| 階段／風險 | 應保留或改變的行為 | 現有 evidence／tests | 必要新增驗證 | 成功或恢復條件 |
| --- | --- | --- | --- | --- |

優先沿用既有 tests、fixtures 與可注入依賴。缺少保護網時，指出需要 characterization tests 的行為。過渡與 target 狀態都需要相應驗證；依實際風險涵蓋相容性、保存失敗、中斷、並行操作與 identity 等案例，不套用無關 checklist。

對目前無法自動驗證的項目，列明手動方法、預期結果與限制。不要把 proposed tests、閱讀過的 tests 或文件中的歷史結果描述成此次已通過。
