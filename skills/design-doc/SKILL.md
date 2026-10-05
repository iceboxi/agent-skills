---
name: design-doc
description: Create or update an independently reviewable Markdown Design Doc that synthesizes existing architecture or refactoring evidence, models, proposals, decisions, and rejected premises. Use when a Design Doc is requested or an offer to document architecture results is accepted; do not select this skill merely to persist another workflow's artifact.
---

# Design Document

將已有的架構理解與決策整理成可獨立 review 的 Markdown 文件。主要讀者是不熟悉 repository 的工程師，同時讓熟悉 code 的 reviewer 與其他 AI／CLI 能查證。

這是 downstream architecture synthesis／persistence skill。Architecture reasoning 可以先完成，不要求文件；只有明確要求 Design Doc／architecture document，或使用者已接受將 architecture 結果整理成 Design Doc 的建議時才啟用，不把有用的 planning 停點當成自動觸發。

**Selection boundary：** 不因其他 workflow 的輸出需要寫成 Markdown、保存到 `docs/`、格式化或持久化，就選用此 skill。Implementation plan、execution plan、review report 或其他 workflow artifact 仍屬產生它的 workflow；建立、整理、更新或保存這些 artifact，本身不構成 Design Doc 工作。只有使用者另外要求把既有 architecture evidence／decisions／boundaries／unresolved questions 綜整成可獨立 review 的 Design Doc 時，才使用本 skill。

## 輸入與邊界

接受使用者直接提供的材料，或 `architecture` 的已有成果：scope、current model、evidence、結果狀態、decisions、proposals、unknowns，以及已有的 migration／verification strategy。可以保存 explore、Resolved、Draft / Pending Decisions、Blocked 或 PREMISE REJECTED，不要求上游完成所有階段。資料充分時，不重跑已完成的訪談。

讀取適用的 agent instructions 與既有文件慣例。具體 codebase 的重要技術描述先對照相關 code；補查局部缺口，不為撰寫文件重新探索整個 repository。已提供的 code locations 可能過期，交付前重查重要 references 與 symbols。無法查證的內容標明來源、假設或限制。

此 skill 呈現已有成果，不自行選擇架構。若要求的定稿需要尚未確認的決策，提出 focused questions，或回到 [architecture](../architecture/SKILL.md) 的受影響階段。也可保留 Draft / Pending Decisions 與受阻工作，不把 proposals 寫成 decisions，不為補齊文件重啟選型。

只寫入已請求或已接受保存建議的文件，不重問已提供的文件授權；位置沿用使用者指定或專案慣例。不得藉此修改 code、agent instructions、CLI settings，或開始實作、migration、commit、發布。

沒有既有文件慣例時，選擇合適的 `docs/<topic>-design.md`，不要覆寫不相關文件。若目前環境限制寫檔，先在對話交付完整 Markdown，明確說明尚未存檔，不自行變更 CLI 權限或模式。

## 文件內容與閱讀主線

Design document 是 synthesis artifact，不按 investigation 順序傾倒證據。Reviewer 應先理解：

1. **Why：**為何值得改。
2. **What：**current → target 的核心差異。
3. **Why this direction：**主要理由與限制。
4. **Work：**預計工作與 implementation shape。
5. **Outcome：**完成後應有的具體結果。
6. **Pending：**影響實作的未決事項。

Architecture-change proposal 必須在前段包含 **Target Architecture Overview**，整合完成後主要 components、boundaries、dependencies 與 ownership；可同時呈現 confirmed 與 proposed elements，但狀態必須明確。PREMISE REJECTED 或明確的 current-state documentation 不要求 target overview。不要因 concrete API 尚未定案而省略已有足夠 evidence 支持的 conceptual target。

再以 progressive disclosure 提供 current evidence、protocols、flows、alternatives、migration、verification、history 與 risks。只保留能回答 scope 內架構問題的細節，不讓 supporting detail 搶過設計主線。

不強迫其他固定章節。已有 proposed technical boundaries 時，呈現重要 ownership、layers、interfaces／types 及其關係，並區分 conceptual target、PROPOSED API 與 CONFIRMED TARGET API；沒有上游設計時不自行補造。若仍有會決定 target responsibility、ownership、dependency 或 contract 的 design-blocking decisions，文件必須標為 **Draft / Pending Decisions**，不能當成 final target design；回到 `architecture` 推進 decision gate，除非使用者明確延後、必要 evidence 不可得，或決策合理依賴後續 validation。

文件以 structure、behavior 與 state 保存已有架構知識；下列規則只改變表達方式，不改變 `architecture` 的推理流程、decision gates 或完成契約。Confirmed decisions 與 explicitly unresolved knowledge 均可呈現，不為補齊圖或 protocol 說明自行做架構決策。

## 圖表格式與證據邊界

Markdown design documents 預設使用 Mermaid，以 fenced `mermaid` code blocks 嵌入。互動 CLI 的 ASCII 模型是輸入材料；轉成 Markdown sections 與 Mermaid 時，保留已建立的架構模型、關係與限制，不自行重新設計。Mermaid 不是上游 architecture reasoning 的要求。

圖與相鄰 Markdown 清楚區分：

- **CURRENT：**repository evidence 支持的既有架構與行為，提供 concrete code locations。
- **PROPOSED — NOT YET ACCEPTED：**尚未接受的候選設計，保留 assumptions 與 unresolved questions。
- **CONFIRMED TARGET：**使用者已確認的 target；說明是否已實作，不能讓它看似已在 repository 中運作。

不為讓 Mermaid 圖看似完整，補入沒有根據的 nodes、states、messages、dependencies 或 ownership relationships。未知關係可省略，或在相鄰 Markdown 明確說明 uncertainty；未決問題仍是未決問題。

## Structure、behavior 與 state

依 scope 選擇互補的視角，不要求每份文件都包含三者或所有圖型：

| 視角 | 需要呈現的架構問題 |
| --- | --- |
| Structure | 元件、dependency direction、ownership、protocol 與 responsibility boundaries。 |
| Behavior | 呼叫順序、跨元件互動、async flows、notifications／callbacks／delegates／events，以及會改變行為的 success／failure／recovery paths。 |
| State | 有意義的狀態、triggering events、transitions、guards，以及 terminal／error／recovery states。每個狀態需指出 owner。 |

Diagrams 保存推理中的關係與限制，不用來裝飾。每張圖回答一個問題，提供狀態標籤、必要說明及 evidence。困難概念可增加直觀說明，但不能省略會影響決策的技術細節。

### 選擇 diagram

| 架構問題 | Mermaid type |
| --- | --- |
| Component／dependency／ownership | `flowchart` |
| Data flow | `flowchart` |
| Call ordering／interactions | `sequenceDiagram` |
| Lifecycle／state transitions，有 meaningful states 時 | `stateDiagram-v2` |

- **`flowchart`：**呈現元件、dependency direction、ownership boundaries、protocol consumers／implementations，或 data flow。箭頭意義可能模糊時，在 Markdown 說明是 dependency direction、ownership 或 runtime data flow。不要混用 dependency、ownership 與 runtime message flow；同圖使用時必須明確區分。
- **`sequenceDiagram`：**順序或元件互動影響架構時優先使用。適合 repository／sync／async 操作、delegate／callback／notification、persistence transaction、authentication、lifecycle 與 failure／recovery。列出重要 participants、messages、await／callback，以及會實質改變行為的 failure branches；只畫理解架構所需的互動，不列每個 function call，也不把平行工作畫成固定先後。
- **`stateDiagram-v2`：**僅在 repository evidence 或 confirmed target design 建立有意義的 states／transitions 時使用。在相鄰 Markdown 指出 state machine owner，標示 triggering events、相關 guards、failure states 與 recovery transitions。Sequential process 不自動構成 state machine，不從暫時 control-flow steps 推定 persistent states。圖中的說明用名稱不得假裝成 repository 的 enum、欄位或新 state owner；尚未確認的狀態設計保留為 proposal／open question。

其他 Mermaid diagram types 只有在更適合表達該架構問題時使用，不為視覺變化而選用。

優先使用數張各回答一個問題的小圖，不用一張巨型圖涵蓋全系統，也不為增加密度要求所有 diagram types。當變更改變 behavior，必要時分別畫 current 與 target／proposal，不能混成一張讓新行為看似已存在。

## Protocol 與責任契約

將 scope 內定義重要架構邊界的 protocols 視為文件主要內容。每個 relevant protocol 有獨立 Markdown 小節，例如以 `###` 加上 protocol 名稱為標題。不要逐一列舉 repository 所有 protocols；先選會影響理解或 review 的介面。

依 evidence 與架構相關性，使用以下小節結構；可省略不相關的項目，重要缺口留在 Open questions：

| 小節 | 說明內容 |
| --- | --- |
| **Purpose** | 此 protocol 定義的架構邊界。 |
| **Owner / Layer** | Abstraction 所屬的 layer 與 owner。 |
| **Implemented by** | Repository evidence 支持的 concrete implementations。 |
| **Consumed by** | 依賴此 protocol 的元件。 |
| **Responsibilities** | Protocol 保證或協調的責任。 |
| **Non-responsibilities** | 明確位於邊界之外的重要行為。 |
| **Operations** | 重要 operations，以及有架構意義的 input／output semantics。 |
| **Lifecycle / Ordering** | 順序限制與相關 notifications／events／callbacks；連到相關 sequence diagram。 |
| **State implications** | State ownership 或經由此邊界引發的 transitions；連到相關 state diagram。 |
| **Error semantics** | 有架構意義的失敗行為。 |
| **Concurrency** | 相關的 actor、queue、thread、Sendable、synchronization 或 isolation requirements。 |
| **Current limitations** | Evidence 支持的已知限制。 |
| **Proposed changes** | 與 existing API 分開的候選變更。 |
| **Open questions** | 尚未確認的設計決策或缺少的 evidence。 |

可用簡短 Swift protocol declaration 輔助定位，但 declaration 不能取代語意說明。不複製 implementation details 來增加篇幅。區分 protocol requirement、extension default、具體實作能力與 caller 保證；不能從 method 名稱或 conformance 推定實作能力、錯誤契約或 isolation。

API 沿用上述證據與決策狀態，分別標為 **CURRENT API**、**PROPOSED API — NOT YET ACCEPTED**、**CONFIRMED TARGET API**。不把 proposed declaration 當成現有 code。只確認責任或行為不等於已接受具體 API declaration。

沒有足夠 evidence 或 accepted design 時，保留責任層級與 open question，不虛構 protocol 名稱、methods、states 或後續設計。Rejected premise 的文件也不需要 target API 或 migration 圖。

## 交叉引用與一致性

Protocol 說明連到相關 sequence／state flows 與 failure semantics；圖沿用其他段落的 component 與 protocol terminology。State diagram 指出 owner，sequence diagram 說明呼叫經過的介面，structure diagram 表達相同責任邊界。必要時用穩定的小節名稱或 anchors 交叉引用。

讀者應能從相互連結的表示回答：誰擁有責任、哪個 protocol 定義邊界、誰實作、誰使用、runtime 發生什麼、順序為何、哪些狀態改變，以及失敗後發生什麼。未知的答案保持可見，不為讓表示完整而補造架構。

所有 CURRENT diagrams 與 protocol 描述都需根據 code 查證。Proposal、confirmed target 與 current behavior 分開；確認 target 不代表它已在 repository 中運作。文件知識不足時可保留 gap，不重啟上游推理流程來補滿圖型。

## 決策狀態與寫作

Observed facts、interpretations、assumptions、proposed changes、confirmed decisions 與 unresolved questions 清楚區分。段落或表格已表明狀態時，不必每句加標籤。

Reasoning completion、規劃結果狀態、文件完成、方向已由使用者確認、外部 review 已通過是不同事項。沒有實際確認不能標成 accepted／approved；recommendation 不自動升格為 decision。若 review 改變前提，保留仍有效的內容，只修正受影響的模型與設計，必要時重開該 decision gate。

以繁體中文寫作。使用短句、一句一個主要意思、active voice、穩定術語與明確條件，減少模糊代詞。這是受 ASD-STE100 啟發的寫作習慣，不宣稱嚴格符合該標準。Code identifiers、API names 與 established technical terminology 保持原樣。

重要技術描述提供 repository-relative `file:line` 與 symbol，讓其他人與 CLI 能定位。外部能力或限制引用實際查證的 primary sources。Current facts 與 proposed behavior 分開，避免把未實作設計描述成既有能力。Tests 區分已有、建議與已執行；保留環境限制與結果來源。

## 文件驗證與交付

交付前確認 reviewer 無須讀原對話就能理解變更目的、current model、選擇理由與影響。對照 references、protocols、圖、ownership、contracts、migration、verification 與決策狀態，修正矛盾與無 evidence 的 claims。檢查 participants／messages、callback 與 failure ordering、state owners／guards／recovery 及 API 標籤是否與 prose 相符；不把 current、confirmed target 與未接受 proposal 混寫。尚未釐清的關鍵問題保持可見，並指出是否阻止後續實作。

確認 Mermaid code fences、diagram type 與圖中關係可讀且一致；有可用的 Mermaid parser／renderer 時，檢查語法或 rendering。語法檢查不能取代 repository evidence 與模型一致性查證。

沿用一份主文件作為此次交付，不預設另產生 AI 版、review 清單或多份重複報告；使用者指定多種 artifacts 時依其要求。完成後提供文件位置、狀態與最重要的待 review 問題。不要自動發送給 reviewer，也不要把文件交付當成實作授權。
