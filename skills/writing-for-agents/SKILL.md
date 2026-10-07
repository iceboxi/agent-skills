---
name: writing-for-agents
description: Shared discipline for writing or refactoring skills, AGENTS.md/CLAUDE.md, and other agent-consumed documents. Use to control context load, pointers, progressive disclosure, completion criteria, duplication, no-ops, and instruction sediment.
---

# Writing For Agents

寫 agent 文件的目標不是「內容完整」，而是每次 invocation 都讓 agent 走對 process。

## Two loads

- Context load：每 turn 都被載入的文字成本，例如 AGENTS、skill description。
- Cognitive load：人要記住有哪些文件 / skill、何時使用的成本。

不要無條件最小化其中一個；把 judgement 留給 human，把重複查找與機械 routing 留給 system / router。

## Context pointers

Pointer 必須同時說：

- target 是什麼；
- 什麼 branch / condition 才應讀它。

Weak pointer 是 variance bug。先強化 trigger wording，再考慮把全文 inline。

## Information hierarchy

依 immediate need 排：

1. in-file steps
2. in-file reference
3. disclosed reference behind pointer

只有某些 branch 才需要的 reference 應 progressive disclose。不要只因檔案長就拆；依 branch / sequence 拆。

## Completion criteria

每個 phase / step 都要有可判定的 done condition。

模糊的「理解完成」「檢查一下」容易 premature completion。優先把完成條件寫成 observable / exhaustive condition。

## Single source of truth

同一個 meaning 只留一個 authoritative home。

- skill 行為在 skill；
- project facts 優先由 repo/config/environment 本身提供；
- AGENTS 多放 navigation pointer / truly persistent invariant；
- mechanical rule 優先 lint/test/CI，而不是 prose。

文件重述一個便宜 lookup，就是容易過期的 cache。

## Pruning

定期刪：

- duplicated rule
- stale branch
- environment 已能直接查的 cache
- no-op instruction
- sediment：因為「不敢刪」而一直累積的舊規則

Instruction 是否 no-op 要以實際 model behavior 判斷，不是以「看起來有道理」判斷。

## Invocation mechanics

詳細 skill-specific guidance 見 [skill-mechanics.md](skill-mechanics.md)。

## Completion criterion

文件完成時：

- main path 清楚；
- branch-specific detail 有 pointer；
- completion criteria 可判定；
- 沒有重複 source of truth；
- always-loaded text 每一行都值得 context cost。
