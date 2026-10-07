# Migration, Estimation & Verification Guidance

## Contents

- Applicability
- Implementation phases
- Feasibility gates
- Progressive validation
- Delivery planning
- Engineering estimate
- Verification & acceptance

## Applicability

這份 reference 只在 migration / planning / validation 需要時讀取。不要為了 checklist 把每個小設計擴張成 project / release governance 文件。

核心每案都需要：

- implementation / migration phases（可只有一個 bounded phase）
- engineering estimate
- acceptance / regression strategy

下列僅在 evidence / scope 觸發時展開：

- feasibility gate / fallback
- shadow / differential validation
- branch / integration coordination
- release / rollout / monitoring
- external resource readiness
- measurable outcome / extension exercise

未觸發就省略，不填 N/A。

## Implementation phases

Phase 從 architecture dependency、migration safety、validation gates 推導，不按檔案數或任意 P1/P2 切。

每個 phase 說明：

- Goal / preconditions
- Components / contracts changed
- Behavior preserved / introduced
- Verification
- Compatibility / bridge
- Stop / rollback condition
- Dependency
- Effort range

避免 big-bang，也避免為了 incremental 人為製造 dual owner / dual writer。

temporary bridge 必須有 owner、scope、retirement condition，並在 Migration / Transitional view 可追查。

## Feasibility gates

只有尚未驗證且會改變 target / contract / migration / major estimate 的假設才需要 gate。

Gate 說明：

- assumption
- required evidence / spike
- pass / stop criteria
- earliest validation point
- fallback / reopen decision
- estimate impact

已有足夠 repository / test evidence 時，不為形式新增 spike。

## Progressive validation

高風險 behavior preservation / owner switch 可考慮：

- golden fixtures
- differential tests
- trace replay
- read-only shadow compare

shadow path 不得 send command、寫正式 storage、通知正式 consumer 或成為第二 writer。

## Delivery planning

只有長期、多人、跨 release 或 production rollout 真的影響設計安全時才展開：

- branch / integration coordination
- build / release checkpoints
- rollout / monitoring
- external device / account / data readiness
- rollback limitations

不要在一般單一 refactor 中預設新增這些章節。

## Engineering estimate

Estimate 必須可追到 phases / work packages：

- effort range + total
- unit（人時 / 人日；人日說明基準）
- assumptions / reusable mechanisms
- exploration / implementation / review / regression / device validation
- dependencies / parallelism
- unknowns / re-sizing conditions

effort 與 calendar duration 分開。不要製造假精確數字，也不要套固定 buffer 百分比。

## Verification & acceptance

區分：

- existing tests / fixtures
- characterization tests
- new unit / integration tests
- manual / device validation
- planned spike

Behavior-preserving refactor 至少回答：

existing baseline → target invariant → verification method → failure / stop condition

Confirmed goals 若包含 extensibility / UI separation / maintainability，可選代表性的 extension / integration exercise；只有 scope 真正要求量化 outcomes 時才加入 metrics / ROI。

未執行的 validation 一律保持 PLANNED VALIDATION，不得宣稱已通過。
