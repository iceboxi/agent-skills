---
name: handoff
description: Write a portable context handoff for another session, harness, directory, repository, or colleague without duplicating artifacts that already exist.
---

# Handoff

Handoff 只在 context 需要搬家時使用，例如：

- Codex ↔ Claude / 其他 harness；
- 換 repository / directory；
- 交給 colleague；
- mid-phase fork 一個 side task。

同 harness、同 directory、下一 phase 仍需要原 conversation 作 primary source 時，優先 continue；不要為了「整理一下」自動 handoff。

## Document

預設寫到 OS temp directory，不污染 project source tree。

包含：

- Purpose of next session
- Current phase / status
- Confirmed decisions
- Open decisions / blockers
- Relevant constraints / invariants
- Context pointers：Design Doc、spec、ADR、glossary、prototype、commit、diff、logs 等
- Suggested skills for next session
- Re-entry / completion condition

不要複製已存在 artifact 的全文；用 path / URL / commit pointer。

敏感資料一律 redact。

## Completion criterion

一個 fresh agent 不需要重問已 resolved decisions，就能從 handoff + pointers 繼續指定下一個 phase；同時 handoff 不成為第二份 source of truth。
