---
name: design-doc
description: Create or update a review-ready Markdown architecture or refactoring document when documentation is requested or an offer to document results is accepted. Present existing evidence, models, proposals, decisions, and rejected premises; do not select architecture or implement changes.
---

# Design Document

將已有的架構理解與決策整理成可獨立 review 的 Markdown 文件。主要讀者是不熟悉 repository 的工程師，同時讓熟悉 code 的 reviewer 與其他 AI／CLI 能查證。

這是 downstream presentation／persistence skill。Architecture reasoning 可以先完成，不要求文件；只有明確的文件請求或使用者已接受的保存建議才啟用，不把有用的 planning 停點當成自動觸發。

## 輸入與邊界

接受使用者直接提供的材料，或 `architecture` 的已有成果：scope、current model、evidence、結果狀態、decisions、proposals、unknowns，以及已有的 migration／verification strategy。可以保存 explore、Resolved、Draft / Pending Decisions、Blocked 或 PREMISE REJECTED，不要求上游完成所有階段。資料充分時，不重跑已完成的訪談。

讀取適用的 agent instructions 與既有文件慣例。具體 codebase 的重要技術描述先對照相關 code；補查局部缺口，不為撰寫文件重新探索整個 repository。已提供的 code locations 可能過期，交付前重查重要 references 與 symbols。無法查證的內容標明來源、假設或限制。

此 skill 呈現已有成果，不自行選擇架構。若要求的定稿需要尚未確認的決策，提出 focused questions，或回到 [architecture](../architecture/SKILL.md) 的受影響階段。也可保留 Draft / Pending Decisions 與受阻工作，不把 proposals 寫成 decisions，不為補齊文件重啟選型。

只寫入已請求或已接受保存建議的文件，不重問已提供的文件授權；位置沿用使用者指定或專案慣例。不得藉此修改 code、agent instructions、CLI settings，或開始實作、migration、commit、發布。

沒有既有文件慣例時，選擇合適的 `docs/<topic>-design.md`，不要覆寫不相關文件。若目前環境限制寫檔，先在對話交付完整 Markdown，明確說明尚未存檔，不自行變更 CLI 權限或模式。

## 文件內容

先建立不熟悉 repository 的 reviewer 所需的理解，再呈現取捨與計畫。依規模選擇有用的內容，不強迫每份文件都有相同章節：

只呈現已有材料。Target architecture 或 migration strategy 尚未形成時，可省略對應章節並說明原因。PREMISE REJECTED 的文件保留證據、實際責任邊界與較窄的未決問題，不虛構變更來補滿章節。

1. **目的與範圍：**具體問題、預期結果、scope／out-of-scope、文件狀態。
2. **Current architecture：**短說明、mental model、元件責任、ownership、重要 flows 與 code mapping。
3. **Proposed architecture：**target 與 current 的差異、責任與依賴變化、state／data ownership、contracts、lifecycle／failure handling。
4. **Decisions／alternatives：**已確認的選擇及理由、有實質意義的其他方案與未採用理由。沿用既有比較，不製造假選項。
5. **Migration／plan：**已有的階段、前置條件、相容性、過渡狀態、failure／recovery 與 cleanup。尚未能規劃的部分保留待決原因。
6. **Verification：**相關現有 tests、必要新增驗證、實際檢查結果與限制。
7. **Risks／open questions：**尚未解決的問題、其影響與需要 reviewer 判斷的具體事項。

文件以 structure、behavior 與 state 保存已有架構知識；下列規則只改變表達方式，不改變 `architecture` 的推理流程、decision gates 或完成契約。Confirmed decisions 與 explicitly unresolved knowledge 均可呈現，不為補齊圖或 protocol 說明自行做架構決策。

## Structure、behavior 與 state

依 scope 選擇互補的視角，不要求每份文件都包含三者或所有圖型：

| 視角 | 需要呈現的架構問題 |
| --- | --- |
| Structure | 元件、dependency direction、ownership、protocol 與 responsibility boundaries。 |
| Behavior | 呼叫順序、跨元件互動、async flows、notifications／callbacks／delegates／events，以及會改變行為的 success／failure／recovery paths。 |
| State | 有意義的狀態、triggering events、transitions、guards，以及 terminal／error／recovery states。每個狀態需指出 owner。 |

Diagrams 保存推理中的關係與限制，不用來裝飾。優先使用小型 ASCII diagrams；依使用者偏好與文件環境可選其他表示。每張圖回答一個問題，提供狀態標籤、必要說明及 evidence。困難概念可增加直觀說明，但不能省略會影響決策的技術細節。

### 選擇 diagram

- **Component／dependency diagram：**解釋元件關係、dependency direction、ownership boundaries，以及 protocol consumers／implementations。標明箭頭是 dependency、call、data 或 event，不把它們混用。
- **Sequence diagram：**順序會影響行為時使用。適合 repository／sync／async 操作、delegate／callback／notification、persistence transaction、authentication、lifecycle 與 failure／recovery。列出重要 participants、messages、await／callback 與必要的 failure branches；不要把平行工作畫成固定先後，或只畫成功而省略會改變責任的失敗處理。
- **State transition diagram：**只有實作或已同意設計確實存在有意義的 states／transitions 時使用。標明 owner、events、guards、failure 與 recovery。Sequential process 不自動構成 state machine；code 沒有建立的狀態，須清楚標成 proposal 或省略。圖中的說明用名稱不得假裝成 repository 的 enum、欄位或新 state owner。

優先使用數張各回答一個問題的小圖，不用一張巨型圖涵蓋全系統，也不為增加密度要求所有 diagram types。當變更改變 behavior，必要時分別畫 current 與 target／proposal，不能混成一張讓新行為看似已存在。

## Protocol 與責任契約

將 scope 內定義重要架構邊界的 protocols 視為文件主要內容。不要逐一列舉 repository 所有 protocols；先選會影響理解或 review 的介面。

Evidence 可建立時，對每個 relevant protocol 說明：

- Purpose、layer／owner、implementations 與 consumers。
- Responsibilities 與 explicit non-responsibilities、important operations，以及有架構意義的 input／output semantics。
- State ownership implications、lifecycle／ordering requirements、error semantics，以及相關 notifications／events／callbacks。
- 有關的 concurrency／isolation requirements、current limitations、proposed changes 與 open questions。

可用簡短 Swift protocol declaration 輔助定位，但 declaration 不能取代語意說明。區分 protocol requirement、extension default、具體實作能力與 caller 保證；不能從 method 名稱或 conformance 推定實作能力、錯誤契約或 isolation。

API 與 diagrams 的狀態一致，使用清楚的標籤：

- **CURRENT API／CURRENT：**實際 repository code 與行為，附 concrete code evidence。
- **PROPOSED API — NOT YET ACCEPTED／PROPOSED — NOT YET ACCEPTED：**未接受的宣告或行為；列明假設、替代方案與 unresolved questions。
- **CONFIRMED TARGET API／CONFIRMED TARGET：**使用者已確認的 target；另外說明是否已實作。只確認責任或行為不等於已接受具體 API declaration。

沒有足夠 evidence 或 accepted design 時，保留責任層級與 open question，不虛構 protocol 名稱、methods、states 或後續設計。Rejected premise 的文件也不需要 target API 或 migration 圖。

## 交叉引用與一致性

Protocol 說明連到相關 sequence／state flows；圖沿用其他段落的 component 與 protocol terminology。State diagram 指出 owner，sequence diagram 說明呼叫經過的介面，structure diagram 表達相同責任邊界。必要時用穩定的小節名稱或 anchors 交叉引用。

讀者應能從相互連結的表示回答：誰擁有責任、透過哪個 protocol 暴露、誰呼叫、順序為何、哪些狀態改變、失敗後發生什麼。未知的答案保持可見，不為讓表示完整而補造架構。

所有 CURRENT diagrams 與 protocol 描述都需根據 code 查證。Proposal、confirmed target 與 current behavior 分開；確認 target 不代表它已在 repository 中運作。文件知識不足時可保留 gap，不重啟上游推理流程來補滿圖型。

## 決策狀態與寫作

Observed facts、interpretations、assumptions、proposed changes、confirmed decisions 與 unresolved questions 清楚區分。段落或表格已表明狀態時，不必每句加標籤。

Reasoning completion、規劃結果狀態、文件完成、方向已由使用者確認、外部 review 已通過是不同事項。沒有實際確認不能標成 accepted／approved；recommendation 不自動升格為 decision。若 review 改變前提，保留仍有效的內容，只修正受影響的模型與設計，必要時重開該 decision gate。

以繁體中文寫作。使用短句、一句一個主要意思、active voice、穩定術語與明確條件，減少模糊代詞。這是受 ASD-STE100 啟發的寫作習慣，不宣稱嚴格符合該標準。Code identifiers、API names 與 established technical terminology 保持原樣。

重要技術描述提供 repository-relative `file:line` 與 symbol，讓其他人與 CLI 能定位。外部能力或限制引用實際查證的 primary sources。Current facts 與 proposed behavior 分開，避免把未實作設計描述成既有能力。Tests 區分已有、建議與已執行；保留環境限制與結果來源。

## 文件驗證與交付

交付前確認 reviewer 無須讀原對話就能理解變更目的、current model、選擇理由與影響。對照 references、protocols、圖、ownership、contracts、migration、verification 與決策狀態，修正矛盾與無 evidence 的 claims。檢查 participants／messages、callback 與 failure ordering、state owners／guards／recovery 及 API 標籤是否與 prose 相符；不把 current、confirmed target 與未接受 proposal 混寫。尚未釐清的關鍵問題保持可見，並指出是否阻止後續實作。

沿用一份主文件作為此次交付，不預設另產生 AI 版、review 清單或多份重複報告；使用者指定多種 artifacts 時依其要求。完成後提供文件位置、狀態與最重要的待 review 問題。不要自動發送給 reviewer，也不要把文件交付當成實作授權。
