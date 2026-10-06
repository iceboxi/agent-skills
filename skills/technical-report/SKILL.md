---
name: technical-report
description: Transform approved technical designs, implementation plans, and optional repository evidence into a self-contained technical narrative and canonical content specification that can be rendered consistently to HTML, PPTX, DOCX, PDF, or Markdown. Use for manager, engineering, or mixed-audience architecture/refactor reports; not for architecture design, acceptance review, implementation planning, or layout/rendering itself.
---

# Technical Report

將已存在的 technical design、implementation plan 與可選 repository evidence，整理成 **self-contained technical narrative + canonical Content Specification**，再交給 downstream renderer 產生 HTML、PPTX、DOCX、PDF 或 Markdown。

本 skill 負責 communication synthesis，不重新做 architecture design，也不負責最終 layout/rendering。

預設使用繁體中文，遵循 shared `instructions/common.md` 的 terminology / language rules，保留 code identifiers、API names 與 authoritative source 已建立的 technical/domain vocabulary。

## Core priorities

遇到規則拉扯時，依下列順序判斷：

1. **Preserve technical truth**
   - 不改寫已確認的 architecture、ownership、scope、behavior contracts、status、ordering、dependency 或 diagram topology。
2. **Produce a useful standalone report**
   - 最終 artifact 應能獨立閱讀；理解主要結論不應依賴讀者另外打開 Design Doc、Implementation Plan 或 source code。
3. **Adapt to purpose and audience**
   - 調整 narrative、abstraction level、detail density 與 wording，但 adaptation 應自然反映在內容，不把 reasoning labels 洩漏到 artifact。
4. **Keep uncertainty proportional**
   - Evidence、confidence、risk、unknowns 與 reopen conditions 用來校正內容，不應壓過主 narrative、estimate 或已確認 conclusions。
5. **Separate content from rendering**
   - 同一份 canonical Content Specification 應能轉成不同 medium；renderer 改 presentation，不改 technical meaning。

總原則：

> **Adapt the communication, do not expose the adaptation.**

> **Uncertainty modifies useful content; it does not erase it.**

> **The artifact should stand on its own; evidence is support, not required reading.**

## Selection boundary

適用：

- 已有 Design Doc／architecture proposal／implementation plan，要整理成主管、工程或 mixed audience 的報告；
- architecture/refactor briefing、implementation communication、會後 reference 或 handoff；
- 要建立可供 HTML／PPTX／DOCX／PDF 等 renderer 使用的 Content Specification；
- 要整理 current → target、representative behavior、migration、estimate、testing 與 material risks。

不適用：

- ownership、target architecture、contracts 或 alternatives 尚待決定：回到 `architecture`；
- 要獨立驗證 proposal 是否成立：使用 `review`；
- 要建立 execution-level implementation plan：使用 planning workflow；
- 只要求保存 architecture 為 Design Doc：使用 `design-doc`；
- 單純處理 layout、theme、asset placement 或 rendering：交給 downstream artifact capability。

Repository evidence 可用來確認 technical claim、current behavior、complexity、risk 與 sizing，但不能藉此改寫 confirmed design。若 evidence 揭露足以推翻 design 的 contradiction，停止受影響內容並指出應回 architecture/review。

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

- Design：target、scope、ownership、behavior constraints、confirmed decisions。
- Implementation Plan：work decomposition、migration order、validation gates、execution shape。
- Repository evidence：current behavior、complexity、dependency、coverage、risk、sizing。
- Supporting material：只在不衝突時補充。
- Draft、proposal、planned tests、planned validation 不得描述成已完成。
- 舊版 estimate、verdict 或方案若已被新版 source 取代，不自動承接。

Terminology 以 authoritative source 與使用者明確指定為準。Audience-facing terminology replacement 應一致套用；source 舊稱只在避免誤解所必需時首次補充。不要自行建立第二套 domain vocabulary。

## Delivery contract

### Medium is not implied by Markdown output

聊天或 skill 的文字輸出格式不等於 artifact medium。**不得因目前介面方便輸出 Markdown，就默認使用者選了 Markdown。**

依使用者需求決定：

- 已明確指定 HTML／PPTX／DOCX／PDF／Markdown：建立 canonical Content Specification，交給對應 renderer。
- 明確要求「先看內容／先看大綱／先整理報告」：輸出 media-neutral Content Specification。
- 要求 finished report / artifact，但沒有指定 medium：詢問一次具體選項，例如「要 HTML、PowerPoint、Document，還是先看內容大綱？」；不要默認 Markdown。
- 使用者同時要求多種 medium：共用同一 canonical Content Specification 與 diagram specification，分別 render，不重新做 technical synthesis。

### Canonical content is the source of truth

```text
Design / Plan / Evidence
          ↓
technical-report
          ↓
Canonical Content Specification
          ├─ narrative
          ├─ diagrams
          ├─ estimate
          ├─ validation / behavior parity
          └─ material risks
          ↓
Renderer
   ├─ HTML
   ├─ PPTX
   ├─ DOCX
   ├─ PDF
   └─ Markdown
```

不同 medium 可以改版面、密度、分頁與互動方式，但 conclusions、architecture、estimate、diagram topology、representative behavior 不應分叉。

## Intent and audience inference

使用者以自然語句描述需求即可，不要求理解 Role／Audience／Medium taxonomy。

內部可推斷：

- **Purpose / role**：展示說明、會後 reference、implementation handoff 等。
- **Audience**：未指定時預設 manager-first, engineering-aware。
- **Medium**：由 Delivery contract 處理，不自行猜。

規則：

1. 「給主管 review／看／報告」通常是 audience / delivery context，不自動等同 technical review，也不產生 verdict。
2. Audience adaptation 是內部 reasoning；除非語意本身需要，不在正文反覆寫「主管需要知道」、「Manager takeaway」。
3. Explanation 應直接融入 narrative，不預設新增 `Mental Model`、`ELI5`、`Why this matters` 等人工標籤。
4. Medium 只改 presentation，不改 architecture semantics。

## Standalone report contract

正式 artifact 預設必須 **self-contained**：

- 讀者不點任何 source link，也能理解主要背景、scope、current → target、代表 behavior、migration、estimate 與 success criteria。
- 不用「詳見 Design Doc」「依 Implementation Plan」代替關鍵說明。
- 必要 technical context 應被 synthesis 進正文，而不是外包給原始文件。
- Source links、file:line、document section 只作 optional traceability，不是 comprehension dependency。
- 正式 audience-facing artifact 預設不顯示大量 file:line；放在 internal evidence notes、Presenter Pack 或 optional appendix。
- 若使用者要求 traceability / review evidence，可在不破壞 narrative 的前提下加入引用或 appendix。

判斷標準：

> **No external dependency for comprehension.**

Evidence 應回答「這個 claim 從哪裡來」，而不是「這個 claim 到底是什麼」。

## Build the canonical report model

先建立 media-neutral model：

- confirmed problem / goal
- scope / non-goals
- current structure / behavior
- target structure / responsibility
- key invariants
- representative before → after cases
- expected outcomes / direct benefits
- migration / work packages / dependencies
- estimate
- behavior parity / validation
- high-impact risks
- success criteria
- material unknowns / reopen conditions
- supporting evidence notes

不要把 investigation chronology 或 Design Doc 目錄直接當 narrative。

## Narrative synthesis

對 architecture/refactor report，優先建立一條連續故事：

```text
Current situation
      ↓
Why change + goal / scope
      ↓
Target structure
      ↓
What moves / what stays
      ↓
Representative before → after
      ↓
Migration + estimate
      ↓
How parity is proven
      ↓
Material risks
      ↓
Completion criteria
```

這只是常用 pattern，不是固定 template。重點是段落之間要有因果連續性，不要像互不相干的 slide cards。

### Current → target 必須具體

不要只說「decouple UI」或「single owner」。

應讓讀者能回答：

- 現在誰做什麼？
- 問題發生在哪一層？
- 完成後責任搬去哪裡？
- 哪些東西刻意不動？
- 對現有 caller / UI / persistence 有什麼影響？

### Representative before → after

對 behavior-preserving refactor，優先選 1–3 個足以代表主要差異的 case。

每個 case 可用：

```text
Current behavior
      ↓
What moves / what stays
      ↓
Target owner
      ↓
Behavior invariant
```

或表格：

| Representative case | Current | After refactor | Must stay the same |
| --- | --- | --- | --- |
| TN | ... | ... | ... |
| Sound | ... | ... | ... |

這比單獨列「validation concerns」更能建立可信度。

不要為完整而把全部 27 個 panel 展開；除非 audience 確實需要 implementation handoff。主報告通常用少數代表案例說明規則，再交代完整 coverage。

## Content Specification

Canonical Content Specification 應包含：

- ordered narrative units
- 每段的 key message
- supporting points
- exact diagram specification
- representative behavior cases
- estimate / work packages
- behavior parity / validation strategy
- material risks
- detail suppressions
- internal evidence notes
- optional Presenter Pack

若只輸出 Content Specification，可使用 media-neutral Markdown，但它是 **規格**，不是默認的 finished Markdown report。

Renderer 不應把 `Purpose`、`Audience`、`Key message`、`Why this matters` 等 planning metadata 機械顯示成 artifact labels。

## Visual strategy

Visual 的目的不是裝飾，而是讓 responsibility、workflow、ordering 或 before/after 更容易理解。

### Preserve source diagrams

若 authoritative source 已有直接支撐 narrative 的 architecture、ownership、sequence、dependency 或 state diagram：

- 保留 topology。
- 可以減少次要 annotation，但不能改 semantics、ownership、ordering 或 dependency。
- Current / Target 若都是理解變更必要資訊，分別呈現。
- 定義 ACK / commit / persistence ordering 的 sequence 不以 bullets 取代。
- 有正式 dependency 的 migration 不以 timeline/cards 取代 dependency diagram。

### Create explanation diagrams when useful

即使 source 沒有現成 diagram，若 responsibility split、representative workflow、state transition 或 before/after 用 prose 很難理解，可以建立新的 **explanation diagram**，但：

- 每個 node / edge / state 必須有 source support；
- 不為了圖好看補造 ownership 或 ordering；
- 圖只回答一個主要問題；
- 若是推導圖，Evidence notes 應記錄它由哪些 source facts 組成。

常見用途：

- current / target architecture
- responsibility split
- representative before → after
- ACK / retry / commit sequence
- state machine
- migration dependency

## Diagram source vs final asset

**Mermaid / diagram DSL 是 diagram specification，不等於 final artifact 必須 runtime render Mermaid。**

Canonical model：

```text
Diagram specification
    Mermaid / structured topology
            ↓
Deterministic render step
            ↓
SVG preferred / PNG when necessary
            ↓
Embed into final artifact
```

Renderer 規則：

- Final HTML／PPTX／DOCX／PDF 若重視穩定與 portability，優先使用預先 render 的 deterministic SVG；必要時使用 PNG。
- 不依賴 viewer runtime JavaScript、CDN 或 Mermaid version 才能看懂主要圖，除非 deployment environment 已知支援且使用者明確接受。
- HTML 若需要 editable / interactive Mermaid，可保留 Mermaid source，但應確認 runtime environment；不要把 runtime rendering 當成唯一可見版本。
- 多 medium 應共用同一 diagram specification；若可行，也共用同一 verified rendered asset。
- Slide / Reading View 必須共用相同 topology；只改 scale / layout，不重畫成不同圖。

## Behavior parity and validation

Behavior-preserving refactor 的 validation narrative 必須回答：

> **原本怎麼做？重構後哪個 owner 接手？什麼必須一樣？怎麼證明真的一樣？**

不要只列「可能壞什麼」或一串 testing concern。

### Baseline → invariant → evidence

代表 behavior 應用以下結構：

| Behavior | Existing baseline | Refactor invariant | Verification |
| --- | --- | --- | --- |
| TN ACK | 現行 trace | 保留 commit timing / value semantics | pre/post trace |
| Sound / LED | 現行 batch behavior | 保留 order / retry / rollback | workflow fixture |
| A4 save | memory/event before DB result | failure 不 rollback memory | sequence + failure test |

依 source 替換成真正的 representative cases。

Validation 可分：

- **Core equivalence**：merge、codec、serialization、bytes。
- **Workflow equivalence**：ACK、timeout、retry、commit、rollback。
- **Identity / lifecycle**：切車、logout、late callback、A→B→A。
- **Persistence / event**：snapshot identity、save failure、received/current、routing。
- **Runtime acceptance**：ObjC/Swift boundary、bootstrap、device/FW/environment。

Planned tests 不得寫成 existing coverage。

Testing / testability 若是 source 支持的 direct benefit，可以自然呈現；不要為了強調 behavior preservation 而貶低它。

## Migration and estimate

Migration 主報告通常壓縮成：

- phase goal
- key work
- dependency
- estimate
- material gate

Detailed batch list 只有 staffing / ownership 分派或 handoff 需要時才進主 artifact。

### Estimate is a planning output

當 scope 與 work decomposition 已足以 sizing，而且用途需要 timeline / planning，**必須提供目前最佳 actionable engineering estimate**。

- Estimate ≠ target ≠ commitment。
- 不直接沿用已被新版 design/plan 取代的舊 estimate；依目前 scope 重新 sizing。
- Pending validation 本身不是 withholding estimate 的理由。
- Evidence 不足時，擴大 range、降低 confidence，或簡短指出主要 uncertainty。
- 若 phases 可辨識，優先列 phase estimates + total range。
- Re-estimation checkpoint 用來更新目前 estimate，不是取代目前 estimate。
- 不自動把 engineering days 換算 calendar commitment。

Estimate section 應先讓讀者看到「現在估多少、主要工作在哪裡」，而不是先看到 disclaimer。

## Risks and uncertainty

Risk 的目的，是指出哪些事情值得提前管理，不是證明 estimate 不可靠。

主 artifact 只保留少數 high-impact risks：

- 會改 architecture safety、migration throughput 或主要 work package；
- 有實際 containment / validation 方法；
- 對 planning 或 decision 有實質影響。

避免：

- 把一般 implementation cautions 全列成 risk register；
- 多頁重複「可能上修／需重估／不是承諾」；
- 每個 pending validation 都轉成 schedule warning；
- 讓 risk section 比 current/target/estimate 更醒目。

只有 validation 真可能要求改 confirmed ownership、scope、behavior contract、whole-system persistence 等 architecture assumption 時，才列 reopen / re-estimation condition。一般 implementation variance 留在 estimate range 內。

## Detail suppression and Presenter Pack

主 artifact 預設壓低：

- rejected abstraction 的長篇辯論；
- exhaustive legacy command sequences；
- 全部 file:line references；
- implementation-only naming；
- 27 個 panel 的逐項卡片；
- exhaustive edge-case matrix；
- Q&A / presenter notes。

若 detail 對 correctness 重要，主報告用 principle、representative case 或 diagram 表達。

Presenter Pack 只有使用者要求或明確需要準備問答時才產生，可包含：

- detailed behavior matrix
- full panel / command inventory
- estimate assumptions / sizing evidence
- source references
- special cases / rejected alternatives
- deep-dive diagrams
- validation checklist

## Evidence discipline

重要 technical claim 必須可回 authoritative source 或 repository evidence，但 evidence 應在 synthesis 背後工作。

- 正式 artifact 不需要顯示全部 file:line。
- Source links 只能是 optional traceability，不應是理解正文的必要步驟。
- 無法查證的 project-specific claim 標為 assumption / unknown。
- Source code 可證明 complexity、dependency、current behavior 與 sizing evidence。
- Legacy identifier 本身不能升格成新 domain concept。
- Status 必須準確：planned、draft、validated、implemented、tested 不混用。

## Handoff to artifact generation

交給 renderer 時至少包含：

- purpose / role
- audience
- requested medium
- ordered narrative units
- key messages + supporting points
- exact diagram specifications
- preferred rendered diagram assets（若已建立）
- representative before → after cases
- migration / estimate
- behavior parity / validation
- material risks
- detail suppressions
- optional Presenter Pack

Renderer 負責：

- layout / typography / pagination / interaction
- deterministic diagram rendering / embedding
- medium-specific density adjustment

Renderer 不負責：

- 重新決定 architecture conclusions
- 重做 estimate
- 改 diagram topology
- 改 representative behavior semantics
- 把 Content Specification metadata 當成 artifact headings

## Completion check

交付前檢查：

1. **Standalone**：不開 source documents，讀者能否理解主要內容？
2. **Truth**：architecture、scope、status、behavior contracts 是否忠於 authoritative source？
3. **Narrative**：是否形成 current → target → representative behavior → migration 的連續故事，而不是互不相干的卡片？
4. **Medium**：若 finished artifact requested，medium 是否已明確？是否避免默認 Markdown？
5. **Portability**：canonical Content Specification 是否可以同步 render 到其他 medium，而不需要重新做 technical synthesis？
6. **Visuals**：主要 diagrams 是否保留或補足 explanation diagrams？Final artifact 是否避免不必要的 runtime rendering dependency？
7. **Behavior parity**：是否清楚呈現 baseline → invariant → verification，而不是只列 concerns？
8. **Estimate**：若 scope 足以 sizing，是否提供目前可用的 phase / total estimate？
9. **Risk**：uncertainty 是否比例適當，沒有壓過 main narrative？
10. **Detail**：source evidence 與 deep implementation detail 是否留在 supporting layer，而不是迫使讀者跳出 report？
11. **Success**：讀者是否能判斷重構完成時應看到什麼結果？

完成代表 canonical communication content 已足以交付或 render；不代表 architecture 已重新 review、implementation 已開始或 validation 已完成。
