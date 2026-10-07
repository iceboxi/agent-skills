---
name: questionnaire
description: Turn a decision blocked by knowledge in someone else's head into a focused Markdown questionnaire. Interview the user about the recipient and the needed outcome, then target questions at the missing knowledge.
---

# Questionnaire

用在：

> 阻塞 decision 的資訊不在 code、官方文件、prototype 或目前使用者手上，而在另一個人腦中。

不要假裝 research 可以查到 human-only knowledge。

## 1. Grill the send, not the subject

只問目前使用者一定能回答的兩件事：

1. **Who**：要給誰？角色、專業、和你的關係。
2. **What you need back**：拿到回答後，你必須能做出哪些具體 decision / action？

不要讓使用者替 recipient 回答 subject 本身。

## 2. Write the questionnaire

產生 Markdown，預設 current working directory 或使用者指定位置。

包含：

- Purpose
- From / To
- Context
- How answers will be used
- Questions grouped by theme
- 每題只問一個 concept
- 重要問題優先
- 容易被誤答時補一行 why this matters
- Answer stub
- Anything else?

鼓勵 recipient 回「不知道 / 不確定」，不要逼猜。

## 3. Re-entry

拿回答案後，將它當 evidence：

- requirement / trade-off → grill-with-docs / design
- external fact → research verify（若可驗）
- wayfinder frontier decision → 更新 map

Questionnaire 本身不是 accepted decision。

## Completion criterion

每個「目前使用者必須從對方取得的資訊」都有對應問題，而且 recipient 不需要知道前一整段 conversation 也能回答。
