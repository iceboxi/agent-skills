---
name: technical-report
description: Extract an approved Design Doc into a concise technical presentation focused on why, goals, architecture, key protocols / implementation realization, migration phases, engineering estimate, and completion criteria. Use for slide/presentation communication; do not redesign architecture or replace the Design Doc.
---

# Technical Report

將已完成的 Design Doc 轉成適合口頭報告的 technical presentation。**Design Doc 是 technical source of truth；Report 是 presentation extraction。**

本 skill 不重新探索 repository、不重新做 architecture reasoning、不建立第二套 technical narrative。若 Design Doc 缺少支撐報告所需的設計資訊，回到 Design Doc 補足，而不是 Report 自己推導新的 technical conclusion。

預設使用繁體中文，沿用 Design Doc 與 repository 已建立的 terminology。

## 1. Boundary

適用：

- 將既有 Design Doc 轉成 HTML / PPTX / slides / presentation；
- 對主管、工程、mixed audience 說明 architecture / refactor；
- 需要在有限時間內講清楚 Why、Goal、Architecture、Implementation shape、Phase、Estimate。

不適用：

- architecture 尚未決定：回 `architecture`；
- 要寫完整 technical design：使用 `design-doc`；
- 要建立 implementation plan：使用 planning workflow；
- 要獨立 review design correctness：使用 review workflow。

### Source authority

1. **Design Doc**：architecture、ownership、protocols、behavior、state、implementation mechanics、constraints 的唯一主要來源。
2. **Implementation Plan**：只補 migration phases、execution gates、work breakdown、estimate。
3. Repository evidence 不由 Report 主動重新調查；只有使用者要求 verify / refresh，或 source 明顯衝突時才回查。

Report 不得產生 Design Doc 沒有的 architecture conclusion。

## 2. Presentation focus

Report 預設著重：

1. **Why**：現在的問題與為什麼值得改。
2. **Goal / Outcome**：完成後系統會變成什麼。
3. **Current Architecture**：只講到足以理解問題。
4. **Target Architecture**：ownership / dependency / boundary。
5. **Design Realization**：Target 如何落到 protocol / type / function / event。
6. **Representative Implementation**：1–3 個足以證明設計不是白話的 protocol / code sketch / sequence。
7. **Migration Phases**：phase goal、dependency、重要 gate。
8. **Engineering Estimate**：phase estimate、total range、主要工作量來源。
9. **Completion / Next Step**：做完的判斷標準與下一步。

Report 不需要預設展開：

- exhaustive source evidence / file:line
- 全部 protocols / methods
- 完整 state matrix
- 所有 edge cases
- exhaustive behavior parity matrix
- rejected alternatives
- 全部 open questions

但若拿掉某個 technical detail 後，audience 只能「相信結論」而無法理解設計為什麼成立，該 detail 應保留。

## 3. Extraction, not re-synthesis

從 Design Doc 選取、重排、視覺化內容：

```text
Design Doc
    ↓
select presentation-worthy technical material
    ↓
reorder for spoken explanation
    ↓
split into slides
    ↓
render
```

允許：

- 壓縮文字；
- 合併重複 explanation；
- 把 table / Mermaid 轉成 slide-friendly visual；
- 精選 protocol / code sketch；
- 將同一 topic 拆成多張 slides。

不允許：

- 改 architecture semantics；
- 新增 ownership / dependency；
- 重新設計 API；
- 重新推導 behavior；
- 為了簡潔刪掉使 architecture 無法理解的 technical anchor。

## 4. Narrative

常見 presentation progression：

```text
Why
→ Goal
→ Current Architecture
→ Target Architecture
→ What changes / what stays
→ Design realization map
→ Core protocol / boundary
→ Representative code / runtime flow
→ Migration
→ Estimate
→ Completion
```

這不是「一項 = 一張 slide」。同一 topic 需要 2–3 張才能清楚講完，就拆頁。

### Technical depth

Protocol / code sketch 是正式 presentation material，不預設隱藏。

適合保留：

- defining boundary 的 core protocol；
- target component 與 protocol / implementation 的關係；
- 能暴露 ordering / identity / state ownership 的 function sketch；
- 一個代表性 runtime sequence；
- 能說明「為何不能簡化成 generic policy」的 representative behavior。

不應把 presentation 變成 code walkthrough。每段 code 必須服務 architecture explanation。

## 5. Architecture → protocol continuity

如果 Report 從 Target Architecture 進入 protocol / function / code sketch，**必須先建立 continuity**。

推薦順序：

```text
Target Architecture
      ↓
Design Realization / Interface Relationship Diagram
      ↓
Core Protocol
      ↓
Key Function / Event Flow
      ↓
Representative Code Sketch
```

Design realization diagram 應讓 audience 直接看到：

- protocol / type 屬於哪個 component；
- implementer / consumer；
- key calls / events；
- state owner / operation owner；
- concrete interface 如何對應 Target Architecture。

不要讓 protocol declaration 成為一張與 architecture 無關的孤立 code slide。

## 6. Diagram handling

優先重用 Design Doc 的 diagram topology。

Report 可以：

- 選擇少數真正適合口頭報告的 diagrams；
- 重新排版 / 簡化次要 annotation；
- 將 Mermaid / diagram source deterministic render 成 SVG / PNG；
- 為 architecture → protocol continuity 產生 realization diagram，前提是完全由 Design Doc 已存在的 relationships 組成。

Report 不得改 ownership、ordering、dependency 或新增 unsupported relationship。

Final artifact 若重視穩定性，優先使用 pre-rendered SVG；不要讓主要 diagram 依賴 viewer runtime Mermaid / CDN。

## 7. Slide sizing and pagination

**Slide size 是 hard constraint；topic boundary 不是 slide boundary。**

Renderer 必須先確定固定 canvas，例如 16:9：

- 1600×900 logical canvas；或
- PPTX standard widescreen 13.333 × 7.5 in。

規則：

- 一張 slide 必須完整落在固定 canvas 內；
- 不允許內容靠垂直 scroll 才看得完；
- 不允許 clipping / overflow；
- 不為塞進一頁把文字縮到不可讀；
- 內容太多就拆成下一張；
- 一個主題可以跨多張；
- 一張 slide 只需有一個清楚 message，不要求一個 topic 只佔一張。

HTML presentation 應縮放整個 fixed slide canvas，而不是讓 section 高度隨內容增長。

## 8. Phase and estimate

Migration presentation 聚焦：

- phase goal
- dependency
- architecture / validation gate
- 主要 work package

Detailed file / task list 留在 Implementation Plan。

若已有可信 estimate：

- 顯示 phase breakdown；
- 顯示 total engineering range；
- 說明主要工作量來源；
- uncertainty 只保留會實際影響 planning 的項目。

Estimate ≠ commitment；但不要讓 disclaimer 壓過數字本身。

## 9. Self-contained enough for presentation

Presentation 不應要求 audience 同時開 Design Doc 才懂主線。

但 self-contained 不等於複製完整 Design Doc：

- Why / Goal / architecture / realization / phases / estimate 必須可獨立理解；
- deeper evidence、完整 edge cases、全部 code / protocol 留在 Design Doc；
- 可以在最後指出「完整 design / verification 見 Design Doc」，但不能用這句取代必要內容。

## 10. Handoff to renderer

Content handoff 至少包含：

- ordered slide messages
- selected Design Doc sections
- selected diagrams
- design realization diagram spec
- selected protocol / code sketches
- migration phases
- estimate
- completion criteria
- fixed slide size / medium

Renderer 負責 layout、typography、pagination、diagram asset rendering。

Renderer 不得重新決定 technical content。

## 11. Completion check

交付前確認：

1. 是否忠於 Design Doc，而不是重新發明一份 report architecture？
2. Why / Goal / Current / Target 是否講清楚？
3. Target Architecture 到 protocol / type / function 是否有 continuity？
4. 是否保留足夠 protocol / code sketch，避免只有白話結論？
5. 每張 slide 是否完整落在固定 canvas，沒有 overflow / scroll？
6. Topic 是否依內容需要自然跨多張，而不是硬塞一頁？
7. Diagram topology 是否忠於 Design Doc？
8. Phase / estimate 是否清楚、可用？
9. 細節是否足以支撐 technical credibility，但沒有變成完整 Design Doc dump？
10. Audience 是否能在不打開 Design Doc 的情況下理解主線與 planning？

完成代表已把 Design Doc 轉成可口頭講解的 technical presentation；不代表 Design Doc、architecture review 或 implementation 被重新完成。
