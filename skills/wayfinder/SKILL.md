---
name: wayfinder
description: Map and resolve a multi-session, foggy engineering effort whose route to a named destination is not yet visible. Maintain a lightweight Markdown decision map; resolve one frontier decision at a time with grilling, research, prototype, or unblock tasks; hand clarified decisions into design/spec. No issue tracker is required.
---

# Wayfinder

Wayfinder 用在 **一個 session 裝不下，而且從 current state 到 destination 的路還看不清楚** 的 effort。

典型例子：DataRepository 拆解、跨 subsystem migration、長期 ObjC→Swift ownership migration。

它產生 decisions，不產生 implementation deliverables。

## 1. Name the destination

Chart map 前，先讀：

- [grilling](../grilling/SKILL.md)
- [domain-modeling](../domain-modeling/SKILL.md)

用 grilling 把 destination 說清楚。Destination 是這張 map 的 scope boundary。

如果 breadth-first grilling 後發現整條路其實一個 session 就看得清楚，**不要建 map**；回 grill-with-docs / design。

## 2. Canonical map

不綁 issue tracker。沿用 project convention；沒有時：

.scratch/wayfinder/<effort>/map.md

Map 是 index，不是 detail store：

~~~markdown
# <Effort>

## Destination
<清 fog 到哪裡就完成>

## Notes
<standing constraints / useful skill pointers>

## Decisions so far
- <decision name> → <one-line gist + pointer>

## Frontier
### <decision name>
Question:
Depends on:
Mode: grilling | research | prototype | task

## Not yet specified
- <知道未來有問題，但現在還不能精確問>

## Out of scope
- <超過 destination 的事項>

## Re-entry
<何時可交 design / spec>
~~~

Detail 放在 resolution note / prototype / research artifact；map 只放 gist + pointer。

## 3. Fog vs frontier

判斷標準：

- **Frontier item**：現在已能精確說出 question，即使還不能回答。
- **Not yet specified**：現在連 question 都還不能精確描述。

不要預先把 fog 切成假 work items。

## 4. Resolution modes

每個 frontier decision 選一種 mode。

### Grilling — default, HITL

能透過 discussion / judgement 解的 decision：

- 用 [grilling](../grilling/SKILL.md)
- 同時用 [domain-modeling](../domain-modeling/SKILL.md)

Human 必須真的回答；agent 不得自己問自己答。

### Research — AFK

外部 fact 阻塞 decision → research。

### Prototype — HITL

「要看到 / 跑到才知道」的 state、runtime、integration、UI question → prototype。

### Task — AFK or HITL

沒有 decision，但必須先完成一個 manual / provisioning / data-moving action才能做下一個 decision。

Task 只因為 **unblock decision** 才存在；不得把 production implementation 偷塞進 map。

Repository current fact 本身通常不是 decision ticket；用 explore 查完，將 fact帶回相應 frontier decision。

## 5. Work the frontier

一次 session 原則上只 resolve 一個非-research frontier decision。

Resolution 後：

1. 記錄 detail pointer + gist 到 Decisions so far。
2. 更新 dependent frontier。
3. Fog 中現在能精確問的才升成 frontier。
4. 超過 destination 的移到 Out of scope。
5. 重新檢查 Re-entry。

Research 可安全平行。

## DataRepository-style decomposition

優先釐清：

- domain / responsibility clusters
- canonical state / write ownership
- cross-domain dependencies
- side-effect boundaries
- lifecycle / async risks
- compatibility contracts
- candidate extraction seams
- migration / coexistence constraints

不要一開始宣布最終 module list。讓 evidence + resolved decisions逐步顯示 seam。

## Re-entry

停止 Wayfinder，當：

- destination 已明確；
- architecture-blocking decisions 已 resolved 或可完整列出；
- remaining work 能裝進一份 coherent Design Doc / spec；
- fog 剩的是 downstream detail。

通常：

wayfinder → design → review → spec

如果 architecture 已經 accepted、wayfinder 只釐清 execution uncertainty，也可以直接回 spec。

## Completion criterion

不是「列很多問題」，而是原本 multi-session、route-invisible 的 effort 已成為可追溯 decision map，且 route 已清到正常 design/spec 可以接手。
