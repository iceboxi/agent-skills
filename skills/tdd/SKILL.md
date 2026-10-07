---
name: tdd
description: Behavior-first implementation discipline for new behavior and behavior-preserving refactors. Use inside implementation to establish observable seams, run red-green for new behavior, or characterize existing behavior before refactoring.
---

# TDD & Characterization

若 repository 有 relevant `GLOSSARY.md` / ADR，測試名稱與 seam terminology 應沿用 domain language並尊重 durable decisions；TDD 不修改 glossary/ADR。

這是 implement 內部可重用的 verification discipline，不是每次工作都必須獨立啟動的 workflow。

核心原則：

Tests verify observable behavior through agreed seams, not private implementation shape.

## Choose the branch

### New behavior

使用：

~~~
RED
 ↓
minimum GREEN
 ↓
next vertical behavior slice
~~~

- 先寫會因缺少 behavior 而失敗的 test / check。
- 只實作讓當前 behavior 成立的最小改動。
- 下一個 test 由上一輪學到的資訊決定。
- 不一次先寫全部 imagined tests。

### Behavior-preserving refactor

不要假裝有「新 behavior」來追求 red。

使用：

~~~
CHARACTERIZE CURRENT
        ↓
ESTABLISH REGRESSION SEAM
        ↓
REFACTOR IN SMALL STEPS
        ↓
KEEP GREEN
~~~

Characterization 的 expected result 必須來自 current behavior、known fixture、protocol/spec 或 independent oracle，不從 target implementation 反推。

## Seams

優先使用已存在、caller 真正使用的 seam。測試前先明確列出本次 agreed seams 與各自能抓到 / 抓不到的 behavior。若 seam 本身就是 design 問題，回 codebase-design / design，不要為了測試偷偷新增 production protocol。

區分：

- unit-testable behavior
- integration-testable behavior
- device / hardware / OS-only validation

Unit test 不得冒充 BLE、Watch、background lifecycle、entitlement、device timing 等真正需要 runtime environment 的驗證。

## Test quality

警覺：

- mock private collaborators 而不是測 observable behavior；
- tautological expected values；
- snapshot / fixture 與 implementation 使用同一算法生成；
- 為測試增加 production-only hook；
- assertions 只證明「沒有 crash」卻沒有驗 semantic result；
- refactor 改 private shape 就讓大量 tests 無理由破裂。

## Completion criterion

New behavior：至少一個 check 曾在缺少 behavior 時失敗，現在因正確 implementation 通過。

Behavior-preserving refactor：關鍵 current semantics 已被 characterization 捕捉，refactor 後同一 observable seam 保持通過；device-only gates 仍清楚標為 pending / completed。
