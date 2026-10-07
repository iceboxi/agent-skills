---
name: wayfinder
description: Map and resolve a very large, foggy engineering effort whose full decision tree cannot fit in one design pass. Maintain a lightweight Markdown decision map, resolve one decision frontier at a time, and hand the clarified result into normal design/spec workflows. No issue tracker is required.
---

# Wayfinder

Wayfinder 處理的是：

目標大致知道，但從 current state 到 destination 的完整路徑還看不清楚。

典型例子：拆解巨型 DataRepository、跨多 subsystem migration、長期 Objective-C → Swift ownership migration。

它不是 implementation ticket generator，也不是大型 Design Doc。目標是逐步清除 fog of war，直到正常的 design / spec 能接手。

## Canonical artifact

使用一份 Markdown decision map。

若專案已有 planning / memo convention，沿用它；否則預設：

~~~
.scratch/wayfinder/<effort>/map.md
~~~

不要求 GitHub/GitLab issue、child ticket、label 或 blocking API。若團隊本來就在 issue tracker 工作，可以另外 mirror，但不是本 skill contract。

## Map shape

~~~
# <Effort>

## Destination
<走到什麼狀態才算 fog 已清到可以進正常 design/spec>

## Scope
<目前 effort 的邊界>

## Decisions resolved
- <decision>: <one-line result> → <link / note / evidence>

## Frontier
### <decision name>
Question:
Why now:
Depends on:
Resolution mode: explore | research | prototype | discussion

## Fog
- <知道未來需要處理，但現在還無法精確問的區域>

## Out of scope
- <刻意不處理的工作>

## Re-entry
<什麼條件達成後交給 design / spec>
~~~

Map 是 index，不要把每個 decision 的完整研究全文重複貼進來。Detail 放在獨立 note / prototype / source，map 只留 pointer + gist。

## Charting

1. Name the destination：先確認這次 effort 最終要交付什麼，例如「DataRepository 可被分域設計的 responsibility map」而不是模糊的「變乾淨」。
2. Draw current visible frontier：只建立現在能精確描述的 decisions。
3. Record fog：知道有問題但還不能精確問的，不要硬拆成假 work item。
4. Order dependencies：Frontier item 可寫 Depends on，但不需要 ticket graph。
5. Choose resolution mode：
   - repository fact → explore
   - external fact → research
   - runnable uncertainty → prototype
   - architecture trade-off → discussion / design bounded decision

## Working the map

一次聚焦一個 frontier decision，除非多個純 research 可以安全平行。

每次 resolution 後：

1. 把結果加入 Decisions resolved。
2. 更新受影響的 frontier。
3. Fog 中已能精確描述的項目才升成 frontier。
4. 被證明不屬於 destination 的項目移到 Out of scope。
5. 檢查是否已達 Re-entry condition。

Wayfinder 產生 decisions，不直接做 production implementation。

## DataRepository-style decomposition

對 monolith decomposition，優先逐步釐清：

- responsibility clusters
- canonical state / write ownership
- cross-domain dependencies
- side-effect boundaries
- high-risk lifecycle / async behavior
- externally visible compatibility contracts
- candidate extraction seams
- migration ordering / coexistence constraints

不要一開始就宣布最終 module list。先讓 evidence 與 resolved decisions 把可行 seam 顯現出來。

## Re-entry

當以下條件成立，就停止 Wayfinder：

- destination 已清楚；
- architecture-blocking decisions 已能列出或已 resolved；
- remaining work 能裝進一份 coherent Design Doc，或能直接形成 accepted implementation spec；
- fog 剩下的是 downstream detail，而不是未知 architecture。

此時 handoff：

~~~
wayfinder
  ↓
resolved decision map
  ↓
design
  ↓
review
~~~

若 wayfinding 結果其實只是 execution decomposition，而 architecture 已 accepted，可直接交 spec。

## Completion criterion

完成不是「列很多問題」，而是：

原本無法一次規劃的 effort，現在已有一份低解析但可追溯的 decision map，且已清到可以進正常 design / spec workflow。
