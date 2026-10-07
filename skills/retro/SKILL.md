---
name: retro
description: Review an engineering or agent session for repeatable failure modes and propose improvements to skills, instructions, navigation, tooling, tests, and deterministic guardrails. Improve the environment, not the feature code.
---

# Retro

Retro 的對象不是這次 feature code，而是：

為什麼這次 agent / workflow 會走偏？下次如何讓環境更不容易重犯？

## Evidence

優先讀：

- current session / execution trace；
- 使用過的 skills / prompts；
- review findings；
- relevant AGENTS / instructions；
- build / lint / tests / CI；
- navigation / tooling friction。

不要只憑印象增加規則。

## Candidate categories

### Skill boundary

- 一支 skill 是否跨了兩個 phase？
- 是否取得超過任務需要的 authority？
- 應該拆 skill、改 handoff，還是只補 branch？

### Invocation

- agent 是否自動用了不該自動啟動的 orchestration skill？
- router / description 是否造成誤觸？
- human 是否已經難以知道該用哪支 skill？

### Context & writing

- main SKILL.md 是否塞進只有少數 branch 才需要的 reference？
- 是否有 duplicated rule / sediment / no-op instruction？
- 是否需要 progressive disclosure / shared reference？

### Navigation & information access

- agent 是否花大量時間找入口 / ownership？
- 是否缺 project navigation pointer、glossary、ADR、tool access？

### Deterministic guardrails

對 mechanical failure 優先：

- lint
- compiler / typecheck
- tests
- pre-commit
- CI
- custom checker

能 deterministic 擋住的錯，不優先再寫一條 prompt。

### Review standards

只有無法 deterministic encode 的 judgement call，才考慮放進 coding / review discipline。

### Tool economy

- 重複 expensive search / tool call；
- tool output 太大；
- 缺少更直接的 script / command / connector。

## Recommendation shape

每個 candidate 包含：

- Failure observed
- Evidence
- Root cause
- Recommended home:
  - automated check
  - project AGENTS / docs
  - shared skill
  - skill boundary / invocation
  - tooling
  - delete / simplify instruction
- Expected behavior change
- Risk / trade-off
- Priority

## Mutation policy

Retro 預設只提出改善，不直接修改 agent-skills、AGENTS、CI、hooks 或 production repository。

使用者明確要求套用某項改善後，再修改相應 source of truth。

## Completion criterion

只留下有 evidence、會改變未來 behavior 的改善候選；不要把「寫更多規則」本身當成果。優先把 recurring mechanical failure 變成 deterministic guardrail，把 phase confusion 變成 skill boundary / routing 修正。
