---
name: technical-report
description: Transform approved technical designs, implementation plans, and optional repository evidence into audience-oriented technical communication outlines or content specifications. Use for manager, engineering, or mixed-audience architecture/refactor reports and presentations; not for architecture design, acceptance review, implementation planning, or artifact rendering itself.
---

# Technical Report

將已存在的 technical design、implementation plan 與可選 repository evidence，重新組織成適合指定 audience 與溝通目的的 technical report content specification。重點是「如何讓讀者理解並做決策」，不是重做 architecture reasoning，也不是照 Design Doc 章節順序摘要。

預設使用繁體中文說明，保留 code identifiers、API names 與來源中已建立的 technical/domain terminology。

## Selection boundary

適用：

- 已有 Design Doc／architecture proposal／implementation plan，要整理成主管、工程或 mixed audience 的報告；
- 要準備 architecture/refactor review、implementation review、technical briefing；
- 要先產生 presentation／document／web artifact 的內容大綱；
- 要從既有技術材料整理 estimate、risks、testing strategy、migration story 與 expected outcome。

不適用：

- 還需要決定 ownership、target architecture、contracts 或 alternatives：回到 `architecture`；
- 要獨立驗證 proposal 是否成立：使用 `review`；
- 要建立 execution-level implementation plan：使用對應 planning workflow；
- 只要求保存 architecture 為 Design Doc：使用 `design-doc`；
- 單純建立 PPTX／DOCX／HTML 的 layout、theme 或 rendering：交給 downstream artifact capability。

本 skill 可以查 repository evidence 以確認 report 中的重要 technical claim、補充 sizing/risk context，或定位 source reference；**repository evidence 不授權本 skill 改寫已確認的 design**。Evidence 若揭露會推翻 design 的 contradiction，停止受影響內容並指出應回到 architecture/review，而不是在 report 中偷偷修設計。

## Source authority

先辨識每份輸入的角色與狀態，不把所有文件當成同等權威。除非使用者或專案另有明確 precedence，預設：

```text
accepted / confirmed Design
        ↓
accepted Implementation Plan
        ↓
approved interface / supporting design material
        ↓
repository evidence
        ↓
explicitly labeled assumptions / unknowns
```

- Design 定義 target、scope、ownership、behavior constraints 與已確認 decisions。
- Implementation Plan 定義 work decomposition、migration order、validation gates 與已確認 execution shape。
- Repository evidence 用於 current behavior、complexity、dependency、coverage、risk 與 estimate grounding。
- Supporting interface/reference 只能在不與較高權威來源衝突時補充。
- 不把 proposal、draft、未執行 tests 或 planned validation 描述成已完成。
- 若使用者指定 precedence，以使用者指定為準並在工作模型中保留。

**Terminology：**沿用 authoritative Design 與使用者已確認的 domain vocabulary。Report 不自行正規化、翻譯或重新命名 domain concepts；若命名本身有問題，應在 Design/source-of-truth 階段修正，而不是由 report 層建立第二套 terminology。

## 先決資訊與輸出媒介

開始前確認下列資訊是否已由請求或上下文提供：

1. **Subject / purpose**：這次要讓 audience 理解、review 或決定什麼。
2. **Audience**：
   - `manager`：先說 outcome、scope、estimate、risk、decision impact。
   - `engineering`：可更早進入 ownership、interfaces、flows、validation。
   - `mixed`：manager framing 在前，再逐步 drill down technical detail。
3. **Delivery context**：若已知，包含時間限制、正式 review／status briefing 等。
4. **Output mode**：Presentation、Document、Web 或 Outline。

若 output mode 未指定，而且不同媒介會明顯改變內容結構，詢問使用者：

> 這次希望產出投影片、文件、網頁，還是先產生一份大綱？

若使用者要求「先大綱」，輸出 **media-neutral Content Specification**，供後續 artifact skill 使用。若媒介已明確，不要重問。

Artifact generation 與 communication planning 是兩個階段。使用者只要求 outline 時，不自行產生 PPTX／DOCX／HTML。

## 工作模型

先建立簡潔的 report model：

- **confirmed problem / goal**
- **scope / non-goals**
- **current mental model**
- **target mental model**
- **key decisions / invariants**
- **expected outcomes / direct benefits**
- **migration / work packages**
- **testing / validation**
- **estimate and confidence**
- **high-impact risks**
- **parallelization / dependencies**
- **unknowns / reopen conditions**
- **supporting evidence**

不要把 investigation chronology 當 narrative。來源文件即使有 20 個章節，也不代表 report 需要 20 個 sections。

## Narrative synthesis

依 audience 與 purpose 重新排序。Architecture/refactor review 的常用 mixed-audience progression 是：

```text
Executive framing
    ↓
Why change
    ↓
Expected outcome / benefits
    ↓
Current → target mental model
    ↓
Target architecture / boundaries
    ↓
Migration + estimate
    ↓
Testing / validation
    ↓
Key risks + parallelization
    ↓
Success criteria
```

這只是 narrative pattern，不是固定九頁 template。依 scope 合併、刪除或增加 sections。

### Progressive disclosure

先讓 audience 理解 whole-system responsibility，再介紹 protocols、API shapes、special cases。

- 不先用 protocol names 解釋問題。
- 不因 source 中存在很多 classes 就逐一列出。
- 不因 Design Doc 有完整 edge-case analysis 就全部搬進主報告。
- 每個 technical detail 必須回答主線中的一個問題；否則移到 Presenter Pack 或省略。

### Expected outcome 要早出現

Manager/mixed audience 在理解 problem 後，應盡早知道「完成後得到什麼」。常見價值包括 single ownership、reuse、testability、extension path、operational safety；只選 source 真正支持的項目。

Outcome 可在最後 Success Criteria 再 recap，但不要等到最後才第一次出現。

## Content Specification

Outline mode 不只列 section titles。每個 section／slide 應視需要提供：

- **Purpose**：這一段要解決 audience 的哪個問題。
- **Key message**：希望讀者記住的一句話。
- **Supporting points**：通常 2–5 個，足以讓 artifact 成為 speaker-ready／reader-ready。
- **Visual specification**：若圖表比 prose 更適合，描述應畫什麼。
- **Detail level / suppressions**：哪些細節不要進主 artifact。
- **Evidence notes**：需要 presenter/reviewer 回查時保留 source locations。

Presentation mode 應偏 speaker-ready，而不是只給極簡 keywords；Document/Web 可保留更多 prose。不要因媒介不同改變 architecture semantics。

## Visual specification

Architecture、dependency、ownership、data/event flow、migration dependency、testing layers 等適合圖像化時，優先產生 diagram specification；Markdown/outline 中預設可使用 Mermaid。

常用：

- component / ownership / dependency：`flowchart`
- call ordering / event interactions：`sequenceDiagram`
- meaningful lifecycle/state：`stateDiagram-v2`
- migration / parallel work：`flowchart`

每張圖只回答一個主要問題。Current 與 Target 明確分開；箭頭意義需可理解。不要為了圖完整而新增沒有來源支持的 node、edge、state 或 ownership。

**Diagram topology 屬於 technical content。** Downstream artifact renderer 可以改 typography、spacing、theme 與 visual styling，但不應自行增刪或重解釋 node/edge/hierarchy。若提供 Mermaid，應把它視為 diagram specification，而不是裝飾性草稿。Renderer 如何嵌入 Mermaid/SVG/PNG 屬 downstream concern，不是本 skill 的完成條件。

## Testing strategy 是正式內容

對 architecture/refactor report，testing 不應只藏在 implementation appendix。若變更目標包含 decoupling、ownership migration 或 behavior preservation，主報告應說明「什麼會被直接測試」。

依 source 支持程度區分：

- **Core unit tests**：例如 merge、codec、rules、serialization。
- **Workflow unit tests**：例如 state transition、ACK、timeout、retry、commit、invalidation。
- **Boundary / integration tests**：例如 language boundary、event routing、persistence snapshot、identity/lifecycle。
- **Regression / runtime validation**：fixtures、legacy behavior traces、device/FW/environment validation。

不要把 planned tests 寫成 existing coverage。若 refactor 讓原本綁在 UI/lifecycle 的 behavior 變得可直接 unit-test，這是 architecture benefit，可在 Expected Outcome 與 Testing Strategy 都呈現。

Coverage percentage 不是預設主角；優先說明 critical behavior 是否可被直接驗證。

## Estimate

當 implementation plan 已可辨識 work packages，而且 manager/mixed audience 需要 timeline 時，提供 **actionable engineering estimate range**；不要以「無法估算」作為預設答案。

### Estimate discipline

- **Estimate ≠ Target ≠ Commitment**。
- 不沿用已被新版 design/plan 取代的舊 estimate。
- 以目前 scope、work packages、source complexity、migration count、validation burden 與已知 risks 建立 range。
- Evidence 不足時擴大 range、降低 confidence，並說明主要 uncertainty；不要假裝精準。
- 不預設產生 Expected / Lower / Upper 三套數字；通常一個 range + confidence + drivers 足夠。
- 分清：
  - **schedule driver**：最主要的工作量來源；
  - **range-width driver**：最主要的不確定性來源。
- 不把 engineering days 自動換算 calendar commitment；除非使用者要求 staffing/calendar plan。

若 source evidence 顯示 work package 明顯比文件想像複雜，可調整 estimate，但要清楚說明是 sizing evidence，不是 architecture change。

## Risks 與 re-estimation

主報告只保留會影響 architecture safety、migration throughput、validation 或 estimate 的高風險項目。避免把一般 implementation cautions 全列成 risk register。

對每個主要 risk，盡量表達：

- risk / assumption
- why it matters
- affected phase / work package
- validation or containment

Estimate 與 risk 應靠近呈現，不要把相同 caveat 散落多個 sections。

若後續 validation 會改變已確認的 ownership、scope、lifecycle、persistence contract 或其他 architecture assumption，清楚寫成 **reopen / re-estimation condition**。語氣應是可操作的 planning condition，不是反覆免責。

## Migration 與 parallelization

主報告通常不需要逐 task 展開 implementation plan。將 phase 壓縮成：

- phase goal
- key work
- estimate（若有）
- acceptance / gate（只有重要時）

指出真正可平行的 work packages，以及它們依賴的 shared foundation。不要只說「可以多人做」；說明 dependency-heavy 區域與可分批區域。

Detailed batch lists 只有在 audience 需要 staffing/ownership 分派時才進主 artifact，否則留 Presenter Pack。

## Detail suppression

主報告預設壓低下列內容：

- 為何沒有採用某個 generic abstraction 的長篇辯論；
- 每個 legacy command 的完整 sequence；
- 所有 source file / line references；
- implementation-only naming；
- exhaustive edge-case matrix；
- management Q&A；
- presenter notes。

若這些內容對 design correctness 重要，主報告用一句 principle 或代表案例說明；完整內容移到 Presenter Pack。

例如不同 operations 有不同 ACK/retry/commit semantics 時，主報告可說：

> Share infrastructure and responsibility model, but do not force a single operation policy.

不需要逐 command 展開，除非該差異本身是此次 review decision。

## Presenter Pack

Presenter Pack 是可選的第二層輸出，不屬於正式 artifact，也不預設當 appendix。

可包含：

- likely questions + grounded answers
- detailed command / behavior matrix
- estimate assumptions / sizing evidence
- source references / file:line evidence
- special cases / rejected alternatives
- optional deep-dive Mermaid diagrams
- validation checklist

只有使用者要求、或明確需要準備問答時才產生。不要因為資訊有價值就全部塞回正式報告。

## Evidence discipline

重要 technical claim 必須能回到 authoritative source 或 repository evidence。若環境允許，保留可重查的 file:line、document section 或 citation；但正式 manager-facing artifact 不需要顯示所有 evidence。

Repository claim 在需要正式 evidence 時遵循專案既有規則（例如 file:line）。無法查證的內容標為 assumption / unknown，不用一般知識補成專案事實。

Source code 可以證明 complexity、dependency 與 behavior；**legacy class／method／variable naming 本身不能升格成新的 domain concept**。Domain terminology 仍以 authoritative Design 為準。

## Handoff to artifact generation

Content Specification 通過使用者 review 後，才交給 downstream artifact generation。交接至少包含：

- audience / purpose / delivery context
- ordered sections/slides
- key message + supporting points
- exact diagram specifications
- estimate / risks / testing content
- detail suppressions
- optional Presenter Pack（若有）

Presentation renderer 不應自行改變 technical topology；Document/Web renderer 不應重新選 architecture conclusions。若 renderer 發現 layout 不適合，應改 presentation，而不是改 semantics。

本 skill 本身不要求同時產生 PPTX、DOCX、HTML。使用者選一種就只產該種；也可以只停在 Outline。

## Completion check

交付前檢查：

1. 是否清楚知道 audience、purpose 與 output mode？
2. 是否遵守 source authority，沒有把 draft/proposal 寫成 confirmed implementation？
3. 是否重新組織 narrative，而非照 Design Doc 目錄摘要？
4. Manager/mixed audience 是否早期看到 outcome 與可用 estimate？
5. Current → Target ownership 是否能快速理解？
6. Diagram 是否保存 technical topology，沒有為美觀補造關係？
7. Testing 是否說清楚 critical behavior 如何驗證？
8. Estimate 是否與目前 plan/source 相符，且 risk/reopen conditions 集中呈現？
9. 是否只保留 high-value detail，將 deep dives / Q&A 留在 Presenter Pack？
10. Success criteria 是否能判斷這次 work 何時真正完成？

完成代表 communication plan/content specification 已足以交給 audience 或 downstream renderer，不代表 architecture 已重新 review、implementation 已開始、tests 已執行或 artifact 已生成。
