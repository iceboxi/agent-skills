---
name: report
description: Extract an approved Design Doc into a concise, rendered HTML/slides/PPTX artifact covering goals, current/target architecture, design realization, core protocols, migration phases, estimates, risks, and completion criteria. Deliver the presentation file and verify rendering; never redesign architecture or invent missing technical decisions.
---

# Technical Report

將已核准版本的 Design Doc 轉成適合口頭報告或主管/工程溝通的 HTML / slides / PPTX 成品，交付可開啟的檔案。

**Design Doc 是 technical source of truth；Report 是 presentation extraction。**

Report 不重新探索 repository、不重新設計 architecture、不建立第二套 technical narrative。若 Design Doc 缺少必要設計資訊，回 `design` 補足，而不是 Report 自己補 invent。

預設使用繁體中文並沿用 Design Doc / repository terminology。

## 1. Boundary

適用：

- HTML / slides / PPTX / presentation
- manager / engineering / mixed audience architecture briefing
- refactor / feature design presentation
- 需要在有限時間講清楚 Why、Goal、Architecture、Protocol、Phase、Estimate、Risk

不適用：

- architecture / protocol 還沒設計好：回 `design`
- acceptance review：使用 `review`
- 只理解 repository：使用 `explore`

## 2. Source authority

1. **Approved Design Doc**：architecture、ownership、contracts、behavior、state、implementation phases、engineering estimate、constraints。
2. **Accepted review result**：若有，提供 acceptance status 與 non-blocking risks。
3. Repository evidence 只在 source 明顯衝突或使用者要求 refresh / verify 時回查。

開始提取前，辨識 Design Doc 的版本或基準，以及使用者或專案既定流程接受該版本的核准依據。既有對話或文件已有明確核准時直接沿用，不重新要求確認；「已完成」、CURRENT 標記或作者自行宣稱 approved，不單獨構成核准依據。Review 的 ACCEPT 類型是 technical verdict，依既定流程判斷是否構成核准，不自行替使用者核准。

核准依據不明時，先整理 source 與待確認事項，再針對該版本詢問；已有明確核准則繼續交付。若核准後改動 technical decisions，或該版本仍有 unresolved blocking findings，回 `design` / `review` 處理；不得把其他版本的核准套用到目前內容。

若 Design Doc 缺少必要 technical content 或與 evidence 有實質衝突，指出受影響內容並交回 `design` 補正；Report 只調整呈現方式，不自行修正設計。

Report 不得：

- 新增 architecture conclusion
- 改 ownership
- 改 dependency direction
- 新增 protocol
- 重新設計 API
- 改 phase semantics
- 自行產生不存在的 estimate
- 把 pending validation 寫成已完成

## 3. Presentation focus

預設 narrative：

```text
Why
→ Goal / Outcome
→ Current Architecture
→ Target Architecture
→ What moves / what stays
→ Design Realization Map
→ Core Protocol / Interface
→ Representative Runtime Flow / Code Sketch
→ Migration Phases
→ Estimate
→ Risks / Validation
→ Completion / Next Step
```

這不是「一項 = 一張 slide」。內容需要多頁就拆多頁。

若 Design Doc 有 overview，優先提取作為開場，保留問題、預期成果、Current → Target、遷移順序與最大風險，再展開 technical anchors。按 audience 與 scope 保留核准的價值證明、重大 go/no-go、delivery milestones 與 rollout / monitoring 限制。開場優先使用 source 的 overview 圖，詳細圖放後續頁；圖仍遵守第 7 節 Diagram handling。

缺少所需的收益、feasibility gate 或 delivery decision 時，指出 source gap 並交回 `design`；Report 不自行計算 ROI、選 rollout 策略或替風險下新的結論。

## 4. Architecture → protocol continuity

這是 hard requirement。

Target Architecture 後如果要講 protocol / function / code sketch，先提供 Design Realization / Interface Relationship view，讓 audience 看得到：

- protocol 屬於哪個 component / boundary
- consumer
- implementer
- key call / event
- state / operation owner
- concrete type 如何對應 target architecture

禁止出現與 architecture 無法連回去的孤立 protocol slide。

## 5. Technical depth

不要把報告全部白話化。

至少保留能證明 design 可落地的 technical anchors，例如：

- defining boundary 的 core protocol
- 1–3 個 representative code sketches
- important sequence / runtime flow
- state ownership / lifecycle relationship
- implementation phase dependency

每段 code 必須服務 architecture explanation；不要變成 code walkthrough。

## 6. Current / Target comparison

Refactor presentation 優先保留：

- Current Architecture
- Target Architecture
- responsibility mapping
- representative before → after
- intentionally unchanged boundaries
- migration gates

新功能則保留 Existing Integration Context + Target Architecture。

## 7. Diagram handling

優先重用 Design Doc topology。

可重新排版、簡化 annotation、render 成 SVG / PNG，但不得改：

- ownership
- dependency
- ordering
- state transitions
- supported relationships

Final artifact 若重視穩定性，優先 pre-rendered SVG，不把主要圖依賴 runtime Mermaid / CDN。

## 8. Slide sizing

Slide size 是 hard constraint；topic boundary 不是 slide boundary。

例如 16:9：

- 1600×900 logical canvas，或
- PPTX widescreen 13.333 × 7.5 in

規則：

- 一張 slide 必須完整在 canvas 內
- 不允許 scroll / clipping / overflow
- 不為塞一頁把文字縮到不可讀
- 內容太多就拆頁
- 一個 topic 可跨多張
- 一張 slide 只需一個清楚 message

## 9. Phase / estimate

Migration presentation 聚焦：

- phase goal
- dependency
- architecture / validation gate
- major work package
- estimate（沿用已核准 Design Doc 的數字、單位、assumptions 與 uncertainty；其他 planning source 必須已被該版本引用並接受）
- 與 audience 相關的 go/no-go、可交付 milestones、rollout 與外部資源限制；保留 internal phase 與可 release checkpoint 的區別

Detailed file/task list 不進主 presentation，除非 audience 需要 implementation handoff。

若已核准的 source 明確保留 pending sizing，忠實標示該狀態；若 estimate 是必要內容卻未提供，回 `design` 補足。Report 不自行估算，也不把 provisional range 改寫成承諾。

## 10. Risks / validation

只保留對 planning / architecture / migration 真正重要的 risks。

優先呈現：

- behavior parity strategy
- identity / lifecycle risks
- ownership / dual-write risks
- migration stop / reopen conditions
- representative validation gates

不要把所有 edge case 都搬進 slides。

## 11. Handoff to renderer

Content handoff 至少包含：

- ordered slide messages
- selected Design Doc sections
- selected diagrams
- design realization diagram
- selected protocol / code sketches
- migration phases
- estimate status
- material risks / validation
- completion criteria
- fixed slide size / medium

Renderer 只負責 layout、typography、pagination、visual rendering，不重新決定 technical content。

Report 負責將 extraction 與 rendering 完成至可交付成品；只有 handoff specification、slide outline 或內容摘要，不代表任務完成。除非使用者明確只要求 outline / renderer handoff，否則依指定格式產出 HTML 或 slides / PPTX 檔案；未指定格式時依已有需求選擇並說明。

## 12. Completion check

交付前確認：

1. 忠於 Design Doc。
2. Why / Goal / Current / Target 清楚。
3. Current → Target 差異清楚。
4. Target Architecture → protocol / type / function 有 continuity。
5. 有足夠 code / interface / runtime detail 支撐 technical credibility。
6. 沒有把 presentation 變成完整 Design Doc dump。
7. 每張 slide 無 overflow / scroll。
8. Phase / estimate / risks / completion criteria 可被 audience 理解。
9. Diagram semantics 與 source 一致。
10. Audience 不打開 Design Doc 也能理解主線。
    若 source 有價值證明、重大 gates 與 delivery milestones，已依 audience 提取，未把未知資源或 provisional estimate 呈現為承諾。
11. 在交付說明或成品 metadata 標示 source Design Doc 的版本或基準與核准依據，讓 technical content 可追溯。
12. 以對應 browser / presentation renderer 實際開啟成品，檢查每頁文字、code、圖表是否可讀、無 clipping / overflow、資源載入正常；交付檔案位置與驗證結果。無法完成 rendering verification 時明確列出原因與未驗證範圍，不宣稱已通過或完整交付。

完成代表 presentation extraction、rendering 與成品驗證已完成，不代表 architecture 被重新 review 或 implementation 已完成。
