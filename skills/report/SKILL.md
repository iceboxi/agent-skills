---
name: report
description: Extract an approved Design Doc into a concise technical presentation focused on why, goals, current/target architecture, design realization, key protocols/code sketches, migration phases, engineering estimate, risks, and completion criteria. Use for HTML/slides/PPTX communication; never redesign architecture or invent missing technical decisions.
---

# Technical Report

將已完成、可作為 source of truth 的 Design Doc 轉成適合口頭報告或主管/工程溝通的 technical presentation。

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

1. **Approved / current Design Doc**：architecture、ownership、contracts、behavior、state、implementation phases、constraints。
2. **Accepted review result**：若有，提供 acceptance status 與 non-blocking risks。
3. Repository evidence 只在 source 明顯衝突或使用者要求 refresh / verify 時回查。

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
- estimate（若 Design Doc / accepted planning source 有可信數字）

Detailed file/task list 不進主 presentation，除非 audience 需要 implementation handoff。

若沒有 accepted estimate，明確標示 pending sizing；Report 不自行 invent。

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

完成代表 presentation extraction 完成，不代表 architecture 被重新 review 或 implementation 已完成。