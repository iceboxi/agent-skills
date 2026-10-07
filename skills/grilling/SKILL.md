---
name: grilling
description: Interview the user relentlessly about a plan, decision, or design until the reachable decision frontier is resolved. Use for human decisions that facts, code exploration, research, or prototypes cannot decide automatically.
---

# Grilling

Grilling 是 Human-in-the-loop decision primitive。目標不是「多問問題」，而是把 decision tree 一層一層走完，直到沒有被默默假設的 branch。

## Design tree

把每個 decision 視為 tree node。只有 prerequisites 已 settled 的 nodes 才進入目前的 frontier。

每一輪：

1. 重新計算 frontier。
2. 一次詢問目前 frontier 的所有問題；不要問依賴尚未 settled answer 的下一層問題。
3. 每題提供一個 recommendation，讓使用者可以用簡短回答接受或修正。
4. 使用者回答後更新 tree，再進下一輪。

問題格式不必僵化，但每題至少包含 decision、relevant alternatives / consequence、recommended answer、recommendation 理由。

## Facts are the agent's job

能從 repository、tool、官方文件、prototype 得到的 facts，不要反問使用者。

需要 fact 時：

- repository current fact → explore
- external platform / SDK / toolchain fact → research
- paper reasoning 無法判定的 runnable question → prototype

Fact 尚未取得時，只讓依賴該 fact 的 branch 等待；其他 frontier decision 繼續。

## Decisions are the human's job

Architecture trade-off、product behavior、scope、risk appetite、hard-to-reverse choice等需要 judgement 的 decision，要明確交給使用者。Agent 可以推薦，不替使用者把 recommendation 偷升格成 confirmed decision。

## Completion criterion

完成條件：

- 目前 scope 的 decision tree frontier 已空；
- unresolved fact / prototype blocker 已明確標示，而不是被假設；
- confirmed decision 與 recommendation 可區分；
- 使用者確認已達 shared understanding。

在 shared understanding 被確認前，不進入 implementation，也不把 recommendation 寫成 accepted target。
