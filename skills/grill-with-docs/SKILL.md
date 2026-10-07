---
name: grill-with-docs
description: Sharpen a software plan or design through grilling while keeping project domain language and durable architectural decisions current in GLOSSARY.md and ADRs.
---

# Grill With Docs

這是 repository 中的 Human-in-the-loop planning 入口。

開始第一輪問題前，必須讀：

- [grilling](../grilling/SKILL.md)
- [domain-modeling](../domain-modeling/SKILL.md)

不要只看到 skill 名稱就自行 improvising interview。

## Behavior

- 用 grilling 的 frontier / round discipline 走 decision tree。
- 同時用 domain-modeling 持續 challenge terminology、查 code contradiction、更新 glossary / ADR。
- repository facts 自己查，不問使用者能由 code 回答的問題。
- 需要 external fact 時用 research；需要 runnable answer 時用 prototype。
- 大到一個 session 無法容納完整 decision tree 時，停止並建議 wayfinder。

## Paper trail

Session 中可能產生：

- GLOSSARY.md term
- sparse ADR
- conversation 中的其他 confirmed decisions

Glossary 不是 spec；ADR 也不是 Design Doc。多數 design decisions 仍只存在目前 conversation，所以 architecture 工作完成 grilling 後，應在同一 primary context 進 design，或需要跨 harness / directory 時先用 handoff。

## Completion criterion

- grilling frontier 空；
- domain terminology 足以支持後續 architecture reasoning；
- durable ADR decisions 已寫入；
- 其餘 confirmed decisions 仍可在目前 context 中追溯；
- 使用者確認 shared understanding。

本 skill 不自行產生 final Design Doc、不進入 implementation。
