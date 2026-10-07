---
name: wizard
description: Turn a genuinely human-only setup, credential, dashboard, provisioning, migration, or cutover procedure into a precise staged checklist or interactive script. Do not use for actions the agent can perform itself.
---

# Wizard

Wizard 用於 agent 無法替人完成、但又會阻塞工程 decision / setup 的 manual procedure。

例如：

- Apple Developer / App Store Connect manual step
- GitLab / GitHub secret or permission setup
- third-party dashboard provisioning
- one-off migration / cutover
- device-only configuration

如果 agent 有工具和權限可以直接做，就直接做，不要把工作丟回人。

## 1. Scope

先讀 repo / docs / config，列出：

- ordered stages
- 每階段產生/需要的 value
- value 從哪裡取得
- 要寫到哪裡
- secret / public
- irreversible step

對未知 dashboard UI / current vendor steps，先 research，不 invent。

## 2. Confirm the journey

給使用者 stage list，確認是否缺步驟、順序或權限。

## 3. Produce the guide

依環境選：

- concise staged Markdown checklist；或
- 使用者明確需要 repeatable automation 時，產 interactive script。

每個 stage：

- current goal
- exact place / URL / command
- what human does
- what value/result to capture
- validation
- irreversible action 前 explicit confirmation

Secret 不輸出到 log / chat；只描述安全 storage target。

## 4. Verify

能 static verify 的部分要驗：

- script syntax
- secret / variable names 對應 CI/config
- every captured value 有 destination
- every stage 有 completion check

不要假裝已完成需要 human click / device action 的 stage。

## Completion criterion

一個不熟悉上下文的人可以照 guide 完成 manual path，而且每個結果都能回到原本被阻塞的 decision / setup。
