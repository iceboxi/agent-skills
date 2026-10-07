---
name: prototype
description: Build the cheapest throwaway artifact that answers one unresolved design, behavior, integration, or UI question. Use when paper reasoning is not enough; capture the answer, not the prototype, as the durable decision.
---

# Prototype

Prototype 是為了回答一個問題而寫的 throwaway artifact，不是 production implementation，也不是完整 spike project。

## Start from the question

先把問題寫成一句可判定的句子，例如：

- 這個 state model 能否表達 required transitions？
- queued callback 在 token expiry 後是否仍會執行？
- Swift type 能否用 Objective-C 需要的 selector / nullability 暴露？
- UIKit interaction A / B 哪個符合使用情境？

如果問題無法清楚判定，不要先寫 prototype。

## Choose the smallest branch

### Logic / state prototype

適合 state machine、merge、retry、ordering、serialization、pure policy。

優先使用：

- existing unit-test target；
- standalone Swift / Objective-C snippet；
- tiny executable / script；
- 最小 deterministic harness。

### Integration / compatibility spike

適合：

- Swift ↔ Objective-C；
- framework / compiler feasibility；
- queue / lifecycle semantics；
- persistence / API shape；
- platform capability。

只建立回答問題需要的最小 wiring，不把 spike 變成 production architecture。

### UI prototype

適合 visual / interaction decision。

依專案現況選 isolated UIKit / SwiftUI demo、temporary screen、preview 或 lightweight harness。比較方案時至少讓差異可以直接切換或並列觀察。

## Rules

- One prototype, one question.
- 不主動加入 production abstraction、error architecture、persistence、polish。
- 除非問題本身是 persistence，不以正式資料來源為依賴。
- 將 relevant state / events / outputs 顯性化，讓結果可觀察。
- Prototype 可使用與 production 不同的簡化結構；不要因為 prototype 能跑就把它 promotion 成 target。
- 需要 device / hardware / account 才能回答時，明確區分 offline feasibility 與 device validation。

## Result

最後記錄：

- Question
- Setup
- Observation / measured result
- Decision supported
- Limitations
- What would falsify the decision

如果結果不足以做 decision，回 INCONCLUSIVE。

正式文件只保留 validated conclusion / evidence pointer；prototype 本體可留在 temporary / scratch location，除非專案明確需要保存。

## Completion criterion

完成不是「prototype 跑起來」，而是：

原本阻塞 design / implementation 的一個問題，現在有可重現 evidence 可以決定或明確判定仍未知。
