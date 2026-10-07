---
name: explore
description: Inspect an unfamiliar or relevant part of a repository and build an evidence-based current-state model of responsibilities, dependencies, state ownership, runtime flows, constraints, tests, and unknowns. Use to understand how the system works before design or implementation; hand target design requests to design.
---

# Explore

建立可被後續 design、review 或 implementation 使用的 repository current-state model。

本 skill 是 **repository investigator**。核心工作是查證「現在怎麼運作」，不是替系統決定「之後應該長什麼樣」。

預設使用繁體中文說明與推理，保留 code identifiers、API names 與 repository terminology。

## 1. Responsibilities

Explore 應：

- 先讀 relevant code，再做 project-specific 結論；
- 找入口、callers、state reads/writes、side effects、lifecycle、persistence、external boundaries 與 tests；
- 區分 observed facts、interpretations、assumptions 與 unknowns；
- 建立 current architecture / responsibility / runtime flow；
- 對重要 technical claim 提供 repository-relative `file:line` evidence；
- 依問題擴大範圍，不需要讀完整 repository；
- 發現文件與 code 不一致時，以 code 為 current evidence 並指出差異。

Explore 不應：

- 提出 target architecture；需要設計時交給 `design`；
- 自動導入 Clean Architecture、MVVM、Repository、Coordinator、Factory 或其他 pattern；
- 為了「解耦」憑空新增 protocol；
- 產生 migration phases 或 implementation plan；
- 把 recommendation 寫成 current fact；
- 修改 production code。

## 2. Working model

維持下列分類：

- **Observed facts**：實際 code / tests / config 中可查證的行為。
- **Interpretations**：由 facts 推導的架構理解，附推導依據。
- **Assumptions**：尚未確認但目前暫時採用的前提。
- **Unknowns**：repository 或需求仍無法回答的事項。
- **Constraints**：既有 compatibility、platform、lifecycle、persistence、protocol 或 product 限制。

重要內容優先使用具體 symbol 與 `file:line`，不要只寫泛化描述。

## 3. What to inspect

依任務選擇相關項目：

- feature / screen / service entry points
- callers / consumers / implementations
- responsibility ownership
- canonical state、snapshot、cache、draft / session state
- write paths 與 side effects
- dependency direction
- data / event / command flow
- callback / async / concurrency ordering
- persistence / network / BLE / hardware boundaries
- failure / recovery / retry behavior
- identity / lifecycle
- existing protocols / interfaces / extension seams
- relevant inheritance：inherited state、instance / factory entry points、未覆寫方法的 side effects
- cross-language boundaries：實際 callers、同步 return、thread / callback contract 與匯入限制；語言可行性需要 compiler / tooling 查證時，不以搜尋結果代替
- tests / fixtures / characterization coverage
- existing build / test tooling 與可用的 device、account、data 等外部驗證資源
- project instructions / invariants

不要套固定 checklist；只展開與問題有關的部分。

區分已存在的保護網、可離線驗證的範圍，以及必須使用外部資源的範圍。資源可用性只能依已查證資訊或使用者確認描述；尚未確認就列為 unknown，不推定已到位。Explore 交付 constraints / evidence，不替 design 決定相容方案或 release 策略。

## 4. Refactor premise validation

使用者要求 refactor 時，先驗證 premise，不先接受「責任放錯」「耦合太高」等描述。

分類：

| Result | Meaning |
| --- | --- |
| **CONFIRMED** | Repository evidence 支持問題描述。 |
| **PARTIALLY CONFIRMED** | 部分成立，但實際 responsibility / flow 與描述不同。 |
| **PREMISE REJECTED** | Evidence 與 premise 矛盾；直接說明實際 boundary。 |
| **INSUFFICIENT EVIDENCE** | 現有 evidence 不足以誠實判斷。 |

PREMISE REJECTED 是有效結果。不要為了繼續 workflow 而虛構 target。

## 5. Output contract

Explore 的輸出不要求固定章節名稱，但應足以回答：

1. Scope：這次實際查了哪一塊？
2. Relevant components：主要 types / modules / files 是什麼？
3. Responsibility map：現在誰負責什麼？
4. Current architecture：dependency / ownership 怎麼連？
5. Runtime flow：代表性 request / event / command 怎麼走？
6. State ownership：哪些 state 是 canonical、temporary、derived？
7. External boundaries：network / DB / hardware / OS / framework 在哪裡？
8. Tests / validation points：目前有哪些保護網、tooling 與已確認／未確認的外部資源？
9. Constraints / special cases：哪些條件會限制後續設計？
10. Unknowns：哪些問題 repository 尚不能回答？

互動 CLI 預設使用小型 ASCII diagram；使用者要求文件或 Mermaid 時再改用對應格式。

範例：

```text
ViewController
    │ user action
    ▼
Manager
    │ command
    ▼
BLE Transport
    │ ACK
    ▼
Manager
    │ state update
    ▼
Repository
```

圖要能回到 concrete symbols，不要畫與 code 無關的理想化 layer。

## 6. Handoff

Explore 完成後：

- 若使用者只想理解系統，到此停止。
- 若使用者要新功能 / refactor 設計，且 scope 已能放進一份 coherent design，將 current-state model、evidence、constraints、unknowns 交給 `design`。
- 若 effort 大到 responsibility clusters / dependencies / decision frontier 尚無法一次看清，交給 `wayfinder` 建 decision map；不要硬產生 final target。
- 若已有 proposal 要驗證，交給 `review`。
- 不預設自動建立 Design Doc；`design` 的產物才是正式 design artifact。

Explore 不需要先取得所有 implementation detail。只要 current model 足以支撐下一個 decision，就可交接。
