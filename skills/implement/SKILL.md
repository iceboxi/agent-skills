---
name: implement
description: Implement one accepted spec, phase, or ready work package without reopening settled architecture. Use after spec/design acceptance; work in small verifiable increments, preserve behavior, stop on design drift, and close with independent code review.
---

# Implement

依 accepted implementation spec / Design Doc 落地 code。Implementation 的權限是完成已決定的工作，不是重新設計。

## Preconditions

取得：

- accepted spec，或足以直接實作的小型 accepted Design Doc；
- source baseline / acceptance basis；
- 本次 ready work package / phase；
- project build / test instructions。

若工作尚未通過必要 spec/design acceptance，或存在 blocking decision，停止並指出缺口。

## Process

1. **Pin scope**：明確列本次 package、non-goals、依賴與完成條件。
2. **Minimal navigation**：只探索完成 package 所需 symbols / callers / tests；不要重新做整體 architecture exploration。
3. **Protect behavior**：使用 `tdd` discipline 選對 branch。
   - behavior-preserving refactor：先 characterize current behavior，再建立 regression seam；
   - 新 behavior：先建立會因缺少 behavior 而失敗的 test / verification，再做 minimum green；
   - ordering / lifecycle / persistence / cross-language contract 依 spec 保留；
   - unit test 不得冒充 device / hardware / OS-only validation。
4. **Implement in small increments**：每一步保持 diff 可理解，避免順手 cleanup 擴大 blast radius。
5. **Verify continuously**：跑最小 relevant test / typecheck / build；完成 package 後跑 spec 指定的 integration / regression gates。
6. **Drift check**：若需要新的 owner、protocol、public API、state semantics、dependency direction、migration policy：
   - 已接受 design 能涵蓋但 spec 漏寫 → `REQUIRES SPEC UPDATE`
   - 會改 accepted design → `REQUIRES DESIGN`
   不要自行合理化後繼續。
7. **Independent review**：完成後使用 `code-review` review 本次 fixed-point diff；修正 findings 後重新驗證。

## Implementation discipline

- 不為測試新增 production-only abstraction。
- 不因「順便更乾淨」重構 unrelated areas。
- 不把 current code 的 bug 修正混入 behavior-preserving change，除非 spec 明列。
- 不把 planned device / runtime validation 宣稱為已完成。
- 若 spec 的 touchpoint 與 repository 已明顯漂移，先查清是否只是導航更新；若責任 / contract 已變，停止。

## Completion report

回報：

- Implemented package / scope
- Changed responsibility / files
- Verification actually run + results
- Code-review result
- Deviations from spec（應為 none；若有，必須有已接受更新）
- Remaining gates / device validation
- Reopen items（若有）

除非使用者要求，不自動 commit / push / release。
