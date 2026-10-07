---
name: diagnosing-bugs
description: Diagnose hard bugs, flakes, crashes, and performance regressions through a gated feedback loop: build a red-capable repro, minimise, rank falsifiable hypotheses, instrument, fix, and regression-test.
---

# Diagnosing Bugs

這支 skill 處理 hard bugs。核心不是「看 code 猜原因」，而是先建立一個對這個 bug 真的會變紅的 feedback loop。

## Phase 1 — Build a red-capable loop

先建立一個 agent 能反覆執行的 pass/fail signal，優先順序依專案調整：

- failing unit / integration / UI test
- CLI / script / captured fixture replay
- minimal harness
- differential old-vs-new run
- stress / repeated loop for flakes
- device / simulator automation
- 最後才是 structured HITL reproduction

Loop 必須：

- drive 到使用者描述的實際 symptom；
- 能在 bug 存在時 red、fix 後 green；
- 盡量 deterministic；
- 盡量 fast；
- agent-runnable，或明確說明 HITL gate。

沒有 red-capable loop，不進 hypothesis phase。若真的建立不了，列出已嘗試方法與還缺的 access / trace / device evidence。

所有 log / artifact 先 redact secrets。

## Phase 2 — Reproduce and minimise

用同一 loop 確認：

- reproduce 的就是原 bug，不是附近另一個 failure；
- flake 已提高到足以 debug 的 reproduction rate；
- symptom 有 observable evidence。

接著一次刪一個 input / config / caller / step，直到 remaining elements 都是 load-bearing。

## Phase 3 — Hypothesise

先產 3–5 個 ranked hypotheses，再測任何一個。

每個 hypothesis 必須 falsifiable：

"If X is the cause, then changing / observing Y should produce Z."

向使用者展示 ranked list；使用者有 domain knowledge 時可 re-rank，但 agent 不等待 user 才繼續可自動驗證的 probes。

## Phase 4 — Instrument

每個 probe 必須對應某個 hypothesis prediction。

偏好：

1. debugger / runtime inspection
2. targeted tagged logs
3. focused counters / timing / trace

一次改一個 variable。避免「log everything」。

Temporary debug instrumentation 必須可一次搜尋清理。

Performance regression 用 measurable baseline / threshold，不靠體感。

## Phase 5 — Fix and regress

只修 confirmed cause，不順手做 unrelated cleanup。

Fix 後：

1. 同一 red loop 必須 green；
2. 加 durable regression test / characterization at the highest stable seam possible；
3. 跑 relevant surrounding checks；
4. 移除 temporary instrumentation；
5. 若 root cause 暴露「沒有好 seam / locality 太差」，把 architecture finding交給 improve-codebase-architecture，而不是在 bug fix 中順手大重構。

## Phase 6 — Retro

Hard bug 修完後，建議用 retro 回看：

- 哪個 guardrail 本可更早抓到？
- 是否缺 deterministic check / test / observability？
- 是否 navigation / architecture seam 造成 diagnosis friction？

## Completion criterion

完成時必須能回答：

- 哪一個 command / loop 曾經 red？
- 最小 repro 是什麼？
- 哪個 hypothesis 被 evidence 支持？
- fix 為什麼解掉 exact symptom？
- 哪個 regression protection 現在會防止復發？
- 哪些 finding 屬於後續 architecture/environment work？
