---
name: technical-report
description: Transform approved technical designs, implementation plans, and optional repository evidence into audience-oriented technical communication outlines or content specifications. Use for manager, engineering, or mixed-audience architecture/refactor reports and presentations; not for architecture design, acceptance review, implementation planning, or artifact rendering itself.
---

# Technical Report

將已存在的 technical design、implementation plan 與可選 repository evidence，重新組織成可理解、可決策、可交付的 technical communication。這個 skill 負責 content synthesis，不重新做 architecture design，也不負責 artifact rendering。

預設使用繁體中文，遵循 shared `instructions/common.md` 的 terminology / language rules，保留 code identifiers、API names 與 authoritative source 已建立的 technical/domain vocabulary。

## Core priorities

遇到規則拉扯時，依下列順序判斷：

1. **Preserve technical truth**  
   不改寫已確認的 architecture、ownership、scope、behavior contracts、status、ordering、dependency 或 diagram topology。
2. **Produce useful communication**  
   Report 必須讓讀者得到足以理解、planning 或決策的資訊；guardrail 不應讓 artifact 只剩 caveats。
3. **Adapt to purpose and audience**  
   調整 narrative、abstraction level、detail density 與 wording，但 adaptation 應自然反映在內容，不應把內部 reasoning labels 洩漏到 artifact。
4. **Apply guardrails proportionally**  
   Evidence、confidence、risk、unknowns 與 reopen conditions 用來校正內容，不應喧賓奪主。

兩個總原則：

> **Adapt the communication, do not expose the adaptation.**

> **Uncertainty modifies useful content; it does not erase it.**

例如 audience 是主管，應改變資訊排序與 detail density，而不是反覆寫「主管需要知道」、「Manager takeaway」。需要更容易理解時，直接把 explanation 寫清楚，不預設增加 `Mental Model`、`Why this matters`、`ELI5` 等人工標籤。Estimate confidence 不足時，應擴大 range 或簡短標示主要變數，而不是因此不提供可用 estimate。

## Selection boundary

適用：

- 已有 Design Doc／architecture proposal／implementation plan，要整理成主管、工程或 mixed audience 的報告；
- architecture/refactor briefing、implementation communication、會後 reference 或 handoff；
- 要先建立 presentation／document／web artifact 的 Content Specification；
- 要整理 expected outcome、architecture story、migration、estimate、testing 與 high-impact risks。

不適用：

- ownership、target architecture、contracts 或 alternatives 尚待決定：回到 `architecture`；
- 要獨立驗證 proposal 是否成立：使用 `review`；
- 要建立 execution-level implementation plan：使用 planning workflow；
- 只要求保存 architecture 為 Design Doc：使用 `design-doc`；
- 單純建立 PPTX／DOCX／HTML layout/theme/rendering：交給 downstream artifact capability。

Repository evidence 可用來確認 technical claim、current behavior、complexity、risk 與 sizing，但不授權本 skill 偷改已確認 design。若 evidence 揭露足以推翻 design 的 contradiction，停止受影響內容並指出應回 architecture/review。

## Source authority

先辨識來源角色與狀態。除非使用者或專案另有 precedence：

```text
accepted / confirmed Design
        ↓
accepted Implementation Plan
        ↓
approved supporting material
        ↓
repository evidence
        ↓
explicit assumptions / unknowns
```

- Design 定義 target、scope、ownership、behavior constraints 與 confirmed decisions。
- Implementation Plan 定義 work decomposition、migration order、validation gates 與 execution shape。
- Repository evidence 支援 current behavior、complexity、dependency、coverage、risk 與 sizing。
- Supporting interface/reference 只能在不衝突時補充。
- Draft、proposal、planned tests、planned validation 不得描述成已完成。
- 舊版 estimate、verdict 或方案若已被新版 source 取代，不自動承接。

Terminology 以 authoritative source 與使用者明確指定為準。Audience-facing terminology replacement 應一致套用；source 舊稱只在避免誤解所必需時首次補充。不要自行建立第二套 domain vocabulary。

## Intent and audience inference

使用者以自然語句描述需求即可，不要求理解 Role／Audience／Medium taxonomy。

內部可推斷：

- **Purpose / role**：展示說明、會後 reference、implementation handoff 等。
- **Audience**：未指定時預設 manager-first, engineering-aware。
- **Medium**：HTML、PPTX、DOCX、PDF、Markdown / Outline 等。

規則：

1. 資訊足夠就直接執行，不重問 taxonomy。
2. 「給主管 review／看／報告」通常是 audience / delivery context，不自動等同 technical review，也不產生 verdict。
3. 只有 unresolved choice 會實質改變內容或 artifact 時才詢問，並問實際選項。
4. Medium 改變 presentation，不改變 architecture semantics。
5. HTML Slide View / Reading View 若同時存在，必須共用 conclusions、estimate 與 diagram topology；Reading 可展開 supporting detail，Slides 可 suppress。
6. Audience adaptation 是內部 reasoning。除非語意本身需要，不在正文反覆點名 audience。

## Report model

先建立 media-neutral report model，再組 narrative：

- confirmed problem / goal
- scope / non-goals
- current → target responsibility model
- key decisions / invariants
- expected outcomes / direct benefits
- migration / work packages / dependencies
- estimate
- testing / validation
- high-impact risks
- success criteria
- material unknowns / reopen conditions
- supporting evidence

不要把 investigation chronology 或 Design Doc 目錄直接當 narrative。

## Narrative synthesis

Report 應優先回答讀者真正需要的問題：

```text
Why are we changing this?
        ↓
What becomes better / clearer?
        ↓
What changes from current to target?
        ↓
How will we migrate?
        ↓
How much work is it?
        ↓
How do we prove it works?
        ↓
What could materially change the plan?
```

Architecture/refactor report 常見 progression：

```text
Executive framing
→ Why change + expected outcome
→ Current architecture
→ Target architecture / responsibility
→ Key invariants
→ Migration + estimate
→ Testing / validation
→ Material risks
→ Success criteria
```

這不是固定 template。依 purpose 合併、刪除或調整順序。

### Progressive disclosure

- 先講 responsibility / system shape，再講 protocol、API shape、special case。
- 不因 source 有很多 classes 就逐一列出。
- 每個 technical detail 都要支撐主線；否則移到 Presenter Pack 或省略。
- Explanation 應直接融入 lead、caption、callout 或正文，而不是預設建立獨立 Explanation Layer。
- Expected outcome 應早出現，不要等最後才第一次說明價值。
- 對特定 audience 有幫助的資訊直接呈現，不需要用「給某某看的重點」包裝。

## Content Specification

若輸出 outline / Content Specification，每個 section 視需要包含：

- **Purpose**：這段要解決什麼問題。
- **Key message**：讀者應記住的一句話。
- **Supporting points**：通常 2–5 個。
- **Visual specification**：圖比 prose 更適合時，描述 diagram / table / comparison。
- **Detail / suppressions**：主 artifact 不需要的細節。
- **Evidence notes**：需要回查時保留 source location。

這些欄位是 handoff metadata，不要求 renderer 把 `Purpose`、`Key message`、`Audience` 等 reasoning labels 原樣印在 artifact。

## Architecture and diagrams

Architecture、ownership、dependency、data/event flow、sequence、migration dependency 適合圖像化時，優先產生 diagram specification；Markdown/outline 可使用 Mermaid。

- component / ownership / dependency：`flowchart`
- call ordering / event interaction：`sequenceDiagram`
- meaningful lifecycle/state：`stateDiagram-v2`

每張圖只回答一個主要問題。Current 與 Target 明確分開。不要新增 source 不支持的 node、edge、state 或 ownership。

**Diagram topology 是 technical content，不是 decoration。**

若 authoritative source 已有直接支撐 narrative 的 architecture、ownership、sequence、dependency 或 state diagram：

- Content Specification 應保留其 topology。
- Audience adaptation 可減少次要 annotation，但不能改 semantics、ownership、ordering 或 dependency。
- Current / Target 若都是理解變更必要資訊，分別呈現。
- 定義 ACK / commit / persistence ordering 的 sequence 不以 bullet list 取代。
- 有正式 dependency 的 migration 不以 timeline/cards 取代 dependency diagram。
- Renderer 可改 typography、spacing、scale、theme；不可自行重畫成不同 topology。
- HTML dual view 必須共用同一 diagram source。

Decorative cards、metrics、timelines 可以輔助，但不能取代必要 technical diagrams。

## Behavior, testing and validation

Refactor report 必須清楚區分「搬 ownership」與「改 behavior」。若 source 要求 behavior preservation，不因 consistency、abstraction elegance 或 presentation simplicity 偷改既有 semantics。

Testing 是正式內容，但應聚焦「如何證明關鍵 contract 沒壞」：

- **Core**：merge、codec、rules、serialization。
- **Workflow**：state transition、ACK、timeout、retry、commit、invalidation。
- **Boundary / integration**：language boundary、event routing、snapshot、identity/lifecycle。
- **Regression / runtime**：fixtures、legacy traces、device/FW/environment。

不要把 planned tests 寫成 existing coverage。Coverage percentage 不是預設主角；優先說 critical behavior 如何被驗證。

Testing / testability 若是 source 支持的 direct benefit，可以自然呈現；不要為了強調 behavior preservation 而把「更容易測試」描述成負面或不重要的價值。

## Migration and estimate

Migration 主報告通常壓縮成：

- phase goal
- key work
- dependency
- estimate
- 重要 gate（只有必要時）

Detailed batch list 只有 staffing / ownership 分派需要時才進主 artifact。

### Estimate is a planning output

當目前 scope 與 work decomposition 已足以 sizing，而且 report 的 purpose 需要 timeline / planning，**必須提供目前最佳的 actionable engineering estimate**。

- Estimate ≠ target ≠ commitment。
- 不直接沿用已被新版 design/plan 取代的舊 estimate；應依目前 scope 重新 sizing。
- Pending validation 本身不是 withholding estimate 的理由。
- Evidence 不足時，擴大 range、降低 confidence，或簡短指出主要 uncertainty；不要用「之後再估」取代目前可用的 planning range。
- 若 phases 可辨識，優先列 phase estimates 與 total range，讓工作量來源可見。
- 不預設 Expected / Lower / Upper 三套數字；通常 phase breakdown + total range 足夠。
- 不自動把 engineering days 換成 calendar commitment。
- **Re-estimation checkpoint 用來更新目前 estimate，不是取代目前 estimate。**

Estimate 的主要工作量來源可以簡短指出。除非 uncertainty 足以讓目前 sizing 失去意義，不要讓 estimate section 變成 disclaimer section。

## Risks and uncertainty

Risk 的目的不是證明 estimate 不可靠，而是指出**哪些事情值得提前管理**。

主 artifact 只保留少數 high-impact risks：

- 會改 architecture safety、migration throughput 或主要 work package；
- 有實際 containment / validation 方法；
- 對 planning 或 decision 有實質影響。

避免：

- 把一般 implementation cautions 全列成 risk register；
- 在多頁重複「可能上修／需重估／不是承諾」；
- 為了完整性單獨建立一整頁 uncertainty，除非 risk 本身就是 decision topic；
- 把每個 pending validation 都轉成 schedule warning。

若某 validation 真的可能要求改 confirmed ownership、scope、behavior contract、whole-system persistence 或其他 architecture assumption，才列為 reopen / re-estimation condition。一般 implementation variance 留在 estimate range 內處理。

## Detail suppression and Presenter Pack

主 artifact 預設壓低：

- rejected generic abstraction 的長篇辯論；
- exhaustive legacy command sequences；
- 所有 file:line references；
- implementation-only naming；
- exhaustive edge-case matrix；
- management Q&A / presenter notes。

若 detail 對 correctness 重要，主報告用 principle、代表案例或必要 diagram 表達；完整內容可放 Presenter Pack。

Presenter Pack 只有使用者要求或明確需要準備問答時才產生，可包含 detailed behavior matrix、estimate assumptions、source evidence、special cases、deep-dive diagrams、validation checklist。

## Evidence discipline

重要 technical claim 必須可回到 authoritative source 或 repository evidence，但 evidence 應支撐 artifact，不應主導 artifact。

- 正式 artifact 不需要顯示所有 file:line。
- 無法查證的 project-specific claim 標為 assumption / unknown。
- Source code 可證明 complexity、dependency、current behavior 與 sizing evidence。
- Legacy identifier 本身不能升格成新的 domain concept。
- Status 必須準確：planned、draft、validated、implemented、tested 不混用。

## Handoff to artifact generation

Content Specification 交給 renderer 時至少包含：

- purpose / role
- audience
- requested medium
- ordered narrative units
- key messages + supporting points
- exact diagram specifications
- migration / estimate / testing / material risks
- detail suppressions
- optional Presenter Pack

Renderer 負責 presentation adaptation，不重新決定 technical conclusions。

若 HTML 有 Slide / Reading dual mode：

- 共用 technical content source、diagram topology、conclusions 與 estimate；
- Reading 可展開 supporting detail；
- Slides 可 suppress detail；
- renderer 發現 layout 不合時改 presentation，不改 semantics。

Hosting / publishing 不屬於本 skill。

## Completion check

交付前只檢查會影響品質的核心問題：

1. Technical truth 是否忠於 authoritative source，status 是否準確？
2. 讀者是否能快速理解 why、outcome、current → target 與 migration？
3. Audience adaptation 是否反映在 abstraction / ordering，而不是洩漏成「主管需要知道」等人工 labels？
4. Source 中支撐主 narrative 的 diagram topology 是否保留？
5. 若 scope 足以 sizing，是否提供目前可用的 phase / total estimate，而不是推給未來？
6. Risk / uncertainty 是否比例適當，沒有壓過 estimate 與主 narrative？
7. Testing 是否說明 critical contracts 如何驗證，而非只列 test 名稱？
8. Deep detail 是否被適當 suppress，而不是犧牲必要 technical evidence？
9. Success criteria 是否足以判斷 work 何時真正完成？

完成代表 communication content 已足以交給 audience 或 downstream renderer；不代表 architecture 已重新 review、implementation 已開始或 validation 已完成。
