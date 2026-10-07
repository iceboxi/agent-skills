---
name: spec
description: Turn an accepted Design Doc or already-settled technical decisions into an executable implementation spec. Use after design acceptance and before implementation when the work is large enough to need bounded work packages, dependencies, acceptance criteria, and verification. Never invent new architecture.
---

# Implementation Spec

把已接受的 target design 轉成可執行 implementation contract。Spec 解決「怎麼安全地做完」，不重新回答「系統應該設計成什麼」。

## Preconditions

優先取得：

- accepted Design Doc / technical baseline；
- design review verdict 與 reopen conditions；
- 本次 implementation scope。

若 baseline 尚有 design blocker，停止並回 `design` / `review`。若工作很小、單一 session 可直接完成，不必為流程形式硬產 spec。

## Process

1. **Pin baseline**：記錄 source Design Doc 版本 / commit / review basis。
2. **Choose scope**：整份 design、單一 phase 或一組 related changes。
3. **Recover invariants**：只帶入 implementation 必須保留的 ownership、contracts、runtime semantics、migration gates、non-goals。
4. **Create work graph**：拆成 bounded work packages，標示 dependencies / blockers。一般 feature 優先 vertical slices；wide refactor / owner migration 可用 expand-contract 或 migration phases，不強迫垂直切片。
5. **Define seams**：每個 package 說明從哪個 observable seam 驗證；優先既有 seam，不為測試增加 production abstraction。
6. **Define acceptance**：列 behavior、migration、compatibility、characterization / regression criteria 與必要 commands / device gates。
7. **Map touchpoints**：指出主要 symbols / responsibility groups / likely files，目的是導航與 blast-radius awareness，不把 file list 當 architecture。
8. **Set stop conditions**：若 implementation 需要新的 owner、public capability、protocol、ordering semantics 或 scope expansion，標 `REQUIRES DESIGN`，不要在 spec 內決定。

## Work-package shape

每個 package 至少包含：

- Goal / behavior delivered
- Inherited design decisions
- Expected touchpoints / owners
- Dependencies
- Acceptance criteria
- Verification / characterization
- Migration / rollback or stop condition（relevant 時）
- Explicit non-goals

Package 要能在 fresh implementation context 中執行，不依賴作者腦中的隱含 reasoning。

## Locality check

對 extensibility / maintainability goal，利用 `codebase-design` 的 change-locality discipline檢查 work graph。若一個普通 change 預期要碰大量 unrelated modules，先確認這是 legacy migration blast radius，還是 target seam 本身仍然不對。

## Output

Spec 不複製整份 Design Doc。保留 source pointer，正文聚焦：

1. Baseline / scope
2. Inherited invariants
3. Work graph
4. Work packages
5. Integration / regression verification
6. Reopen / stop conditions

## Completion criterion

一份可接受的 spec 應讓 implementer：

- 不需要重新做 architecture decision；
- 能知道先做什麼、什麼被 block；
- 能知道每個 slice 怎麼證明完成；
- 遇到超出 accepted design 的需求時知道停止而不是自行擴張。
