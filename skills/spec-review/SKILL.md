---
name: spec-review
description: Independently review an implementation spec against its accepted Design Doc, repository reality, migration constraints, and verification seams. Use before implementation as a fidelity and executability gate; do not redesign the architecture or rewrite the spec.
---

# Spec Review

檢查 implementation spec 是否忠實、可執行、可驗證。這不是 design review，也不是 code review。

## Inputs

需要：

- review subject：implementation spec；
- accepted Design Doc / decisions；
- relevant design-review acceptance basis / reopen conditions；
- 必要的 repository evidence。

若缺少 baseline 到無法判斷 fidelity，回 `BLOCKED`。

## Review axes

### 1. Design fidelity

檢查 spec 是否：

- 偷偷新增 / 移除 owner、protocol、public capability、state copy；
- 改變 dependency direction；
- 把 implementation example 當成 mandatory architecture；
- 改變 accepted runtime / lifecycle / persistence semantics；
- 遺漏 design 的 migration gate / non-goal。

### 2. Executability

檢查 work packages 是否：

- bounded；
- dependency / blocker 明確；
- 可在 fresh context 執行；
- acceptance criterion 可觀察；
- high-risk uncertainty 在依賴工作前被 gate；
- wide refactor 沒被硬切成無法保持 coherent state 的假 vertical slices。

### 3. Verification seams

檢查：

- 每個重要 behavior 有合適 seam / characterization / regression；
- tests 驗證 behavior，不綁 private helper shape；
- device / integration gate 沒被 unit test 假裝取代；
- planned validation 沒被寫成 completed evidence。

### 4. Locality & blast radius

使用 `codebase-design` discipline 檢查：

- 普通 extension 是否集中在 responsibility owner；
- spec 是否預期大量 unrelated edits；
- shotgun surgery 是 legacy migration 暫時成本，還是 target design 本身沒有形成 locality；
- implementation work 是否順手加入 speculative cleanup。

## Findings

每個 finding：severity、claim、baseline evidence、repository evidence（relevant 時）、impact、required action。

Verdict：

- **ACCEPT**
- **ACCEPT WITH NON-BLOCKING NOTES**
- **REVISE**
- **BLOCKED**

需要新 architecture decision 時，required action 是 `REQUIRES DESIGN`；不要在 review 中提供 replacement design。只是 spec ordering / acceptance / wording 不完整時，回 `spec` 修正。

## Completion criterion

ACCEPT 類型表示：

- spec 沒有 design drift；
- implementation packages 足以執行；
- verification 能偵測主要 semantic drift；
- remaining uncertainty 有明確 stop / reopen condition。

Acceptance 不代表 code 已實作或 tests 已通過。
