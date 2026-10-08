---
name: review
description: On explicit user request, independently assess whether an existing technical design or implementation spec is defensible enough to become an accepted baseline. Verify material claims against authoritative requirements and repository evidence, report only acceptance-relevant findings, and return ACCEPT, ACCEPT WITH NON-BLOCKING NOTES, REVISE, or BLOCKED. Do not redesign or perform exploratory multi-role critique.
---

# Independent Technical Review

`review` 是使用者**手動呼叫**的選用技術審查，不是主流程的必經 acceptance gate。它回答：

> 這份既有 proposal 在目前 requirements 與可取得 evidence 下，是否足以成為 downstream implementation baseline？

它不是 `challenge`：challenge 追求更多盲點；review 追求低噪音、可證實、會影響 acceptance 的 findings。

## 1. Independence

優先使用 fresh reviewer agent / subagent。若目前 session 本身就是未參與設計的 fresh context，可直接 review。

Independent reviewer 的必要 context 只有：

- review subject；
- confirmed requirements / decisions / invariants；
- relevant repository / tests / project instructions；
- prior accepted baseline（review implementation spec 時）。

不要把作者未寫入 artifact 的 hidden reasoning、辯護過程或其他 challenger 結論當成 acceptance evidence。

若只能在原作者同一 reasoning context 執行，仍可做 review，但輸出要標示 `SAME-CONTEXT REVIEW`；不要宣稱 independent。

## 2. Pin the subject

先確定：

- artifact / version / commit / document revision；
- review scope；
- authoritative requirements / confirmed decisions；
- 哪些 claims 若錯會改變 ownership、interface、behavior、migration 或 acceptance。

已有清楚 subject 時直接開始，不做形式上的重新確認。

Implementation spec 使用 [spec-fidelity.md](spec-fidelity.md) branch；其餘 technical design 使用本流程。

## 3. Verify material claims

只查會影響 verdict 的 claims。Repository current facts 以 code/tests 為準。

依 scope驗證：

- ownership / canonical state；
- callers、dependencies、side effects；
- significant interface / seam claims；
- representative runtime / failure / lifecycle behavior；
- migration / compatibility assumptions；
- verification strategy 是否能觀察 promised behavior。

需要 module/interface judgement 時使用 upstream `codebase-design` vocabulary。不要把整個 repository 重新探索一遍。

## 4. Acceptance findings

Finding 必須包含：

- **Severity**：`BLOCKING | NON-BLOCKING | NOTE`
- **Claim**
- **Evidence**
- **Impact**
- **Required action**

只報真正影響 acceptance 或值得 downstream 明確追蹤的事項。

- 缺少 human decision → 不替 human 決定；回 `grilling` / `design`。
- 需要新 target architecture → 回 `design`。
- 只是探索性 concern、沒有 evidence → 不升格成 blocker；必要時標 NOTE 或交 `challenge`。
- naming / private helper /一般 implementation taste 不影響 architecture contract 時，不列 blocker。

Review 可以指出哪個 boundary / invariant 不成立，但不在 review 裡偷偷產生 replacement design。

## 5. Verdict

只用：

- **ACCEPT**：沒有 blocking finding，proposal 足以成為 baseline。
- **ACCEPT WITH NON-BLOCKING NOTES**：沒有 blocker，但 downstream 有需追蹤的明確風險。
- **REVISE**：已有 evidence 證明 proposal 與 confirmed goal / invariant / repository reality 衝突，或缺少必要 architecture decision。
- **BLOCKED**：缺必要 artifact / requirement / evidence，無法誠實判斷 acceptance。

Verdict 只代表 technical acceptance，不代表 implementation / tests / release 已完成。

輸出：

```text
Review mode: INDEPENDENT | SAME-CONTEXT
Verdict: ACCEPT | ACCEPT WITH NON-BLOCKING NOTES | REVISE | BLOCKED

Reason:
<short reason>

Blocking findings: <n>
Non-blocking findings: <n>
Notes: <n>
```

接著只列有 evidence 的 findings，最後列：

- **Acceptance basis**
- **Reopen conditions**
- **Next step**

## 6. Optional follow-up

由使用者決定是否依 verdict 回到 requirement / spec / planning authority 修正技術決策。若僅是獨立 Design Doc 的呈現或同步問題，使用 `design` maintenance mode。

Review 不自動觸發 `to-spec`、`to-tickets` 或 `challenge`；它不是 engineering implementation 的強制 gate。
