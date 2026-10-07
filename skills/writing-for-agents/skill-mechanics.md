# Skill Mechanics

## Invocation

### Model-invoked

適合：

- agent 必須自行判斷何時 reach；
- 另一支 orchestration skill 必須依賴它；
- shared reference / reusable discipline。

代價是 description 永久佔 context，description 必須是精準 pointer，而不是宣傳文案。

### User-invoked

適合 phase-changing orchestration：

- grilling session
- design / review
- wayfinding
- implementation orchestration
- retro

人主動啟動；agent 不應自行換 phase。

在 Codex metadata 使用 policy.allow_implicit_invocation: false。

## Dependency rule

User-invoked orchestration 不應依賴另一支 user-invoked orchestration 自動觸發。

可共用的能力要：

- 抽成 model-invoked primitive；或
- 抽成 plain reference file。

例如：

- grill-with-docs → grilling + domain-modeling
- design/review → codebase-design
- retro → writing-for-agents

## Router

當 user-invoked skills 多到難記，用一支 user-invoked router 降 cognitive load。

Router：

1. 只做 routing，不執行工作；
2. summary 只供 shortlist；
3. 推薦 / 跳過某 skill 前，實際讀 candidate SKILL.md；
4. 推薦能解當前 phase 的最小 flow；
5. 說明最容易誤用的鄰近 skill。

## Splitting

拆 skill 的充分理由：

- invocation authority 不同；
- distinct reusable primitive 需要被其他 skill reach；
- sequence boundary 需要 fresh context；
- branch-only reference 正在淹沒 main path。

不要只因檔案行數增加就拆。
