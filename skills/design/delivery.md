# Phases, Estimates & Verification Documentation

## Contents

- Boundary and self-contained output
- Phase synthesis
- Migration and feasibility
- Engineering estimates
- Verification and acceptance
- Final audit

## Boundary and self-contained output

從已確認的 spec、工作規劃、決策、estimate、test strategy 提取 **工程報告需要的內容**，不重新拆解工作、不調整依賴、不創造 engineering / release gate。

Design Doc 必須獨立閱讀：Phase 直接說明目標、內容、交付成果、工時與驗證，不出現 issue / ticket ID、標題、狀態、tracker URL、ticket-to-phase mapping，也不要求讀者開啟 tracker 才能理解。

## Phase synthesis

將詳細工作拆分**彙總為少量可向工程與主管說明的 implementation phases**；數量依已規劃的工作與架構邊界決定，不按 ticket 數一對一對照。

每個 phase 說明：

- Goal / deliverable
- Major responsibilities / interfaces / flows affected
- Preconditions / real dependencies
- Relevant behavior preserved / introduced
- Verification / completion signal
- Migration gate / stop / rollback condition（有來源時）
- Effort range（已有可追溯數字時）

對原本可並行工作，不要因報告順序造成假的 hard dependency。若切換必須先完成 characterization / compatibility，保留這個重要 gate。

## Migration and feasibility

只記錄來源支持的 transition strategy：legacy / new coexistence、state transfer、expand-contract、bridge retirement、stop criteria 等。若行為保留是目標，交代 Current behavior invariant 與如何觀察。

Feasibility unknown 若會改變 target、主要 contract、migration 或重大 estimate，明確標 `UNRESOLVED` 或已規劃的 validation gate；不要自行決定 fallback。

不為一般小型功能製造 rollout、ROI、project governance 等多餘章節。

## Engineering estimates

- 優先使用已確認的估算、單位、範圍與前提；已存在的 work estimates 可以正確彙總，但不能自行加 buffer 或假精確數字。
- 分開描述 engineering effort（人時 / 人日）與 calendar duration。
- 估算必須涵蓋來源已納入的實作、整合、review、回歸測試及 device / runtime verification。
- 未提供可追溯數字時明確列出缺口與影響，不因 Design Doc 需要工時就創造一組數字。
- 已知的高風險、外部依賴、re-estimation conditions 在文件中具體交代，不作「一切可能延後」的空泛提醒。

## Verification and acceptance

區分：

- Existing tests / fixtures
- Characterization baseline
- Planned unit / integration tests
- Manual / device / hardware verification
- Prototype / spike evidence（verified / planned）

描述 behavior-preserving refactor 時，將已確認的 observable baseline、target invariant、verification method、stop condition 寫完整。不把 planned test 寫成 pass，也不把 unit test 當成 BLE、Watch、background lifecycle 或 entitlement 的 device evidence。

## Final audit

- [ ] Phase 可獨立理解，沒有呈現任何 tracker management 資訊。
- [ ] 依賴 / gate 與來源一致，沒有自行重排成新的工程決策。
- [ ] Estimate 可追溯、有單位、沒有虛構的精確數字。
- [ ] Verification 標明 existing / planned 和 unit / integration / device 層次。
