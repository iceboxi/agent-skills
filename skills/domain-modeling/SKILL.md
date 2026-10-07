---
name: domain-modeling
description: Sharpen project-specific domain language, stress-test terms with concrete scenarios, and record durable terminology and hard-to-reverse decisions in GLOSSARY.md and ADRs. Use when terminology or domain boundaries are actively being decided.
---

# Domain Modeling

這是 active domain discipline，不是單純讀 glossary。

## Language

遇到 project-specific fuzzy / overloaded term：

1. 先查既有 GLOSSARY.md / GLOSSARY-MAP.md。
2. 若使用者用法與既有定義衝突，立刻指出。
3. 用 concrete edge scenarios 壓測概念邊界。
4. 選一個 canonical term，必要時列出應避免的 synonyms。
5. resolution 一形成就更新 glossary，不要等 session 結束才批次整理。

Glossary 只記 domain vocabulary，不放 implementation detail、spec、scratch notes 或一般 programming concept。

若 repo 沒有 glossary，第一次真的有 term 需要記錄時才 lazy-create：

- single context：root GLOSSARY.md
- multi-context：若已有 GLOSSARY-MAP.md，跟隨 map 指到對應 context

## Cross-check code

當人描述 domain behavior / relationship 時，查 repository 是否一致。

若 code 與說法衝突，先 surface contradiction：

- code 是 current behavior；
- 使用者說法可能是 target / requirement；
- 不自行選一邊。

## ADR

只在三個條件全部成立時建議 ADR：

1. hard to reverse；
2. future reader 看 code 會覺得 surprising without context；
3. 曾有 real trade-off / alternative。

預設位置沿用 repo convention；沒有 convention 時用 docs/adr/NNNN-slug.md。

ADR 可以很短：context + decision + why。不要把所有 implementation choice 都變成 ADR。

## Completion criterion

- resolved term 有唯一 canonical meaning；
- glossary 沒混入 implementation prose；
- code / domain contradiction 已被指出；
- ADR 只記真正 durable trade-off；
- 未決 terminology 保持 unresolved，不用 agent 自創詞掩蓋。
