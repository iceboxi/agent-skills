---
name: change-summary
description: Shape a pull request or merge request body around the smallest visual that explains the change, concrete before/after evidence, and merge danger including reversibility and blast radius.
---

# Change Summary

適用 GitHub PR、GitLab MR 或其他 code-review change body。它不建立 PR/MR，也不重新 review code；只負責讓 reviewer 快速理解 change。

## Summary

用**最小足夠 visual**表達核心 change：

- runtime / control flow → call tree / sequence
- responsibility move → shallow file/module tree
- small structural delta → diff sketch
- state transition → state/control pseudocode
- architecture interaction → Mermaid / equivalent diagram

只留 reviewer 理解 ownership、order、behavior 所需內容。

沿用 GLOSSARY domain language。

## Evidence

給 concrete before / after：

- screenshot
- failing → passing test
- old → new output
- benchmark / trace
- build / validation evidence

Planned validation 不可寫成 completed evidence。

## Merge danger

明確回答：

- **Door**：two-way / one-way
- **Blast radius**：影響範圍
- rollback / recovery 是否容易
- migration / data / compatibility 是否有不可逆部分

## Completion criterion

Reviewer 不需要先讀整個 diff，就能知道：

- 變了什麼；
- 為什麼；
- 有什麼 evidence；
- merge 失敗會影響哪裡、能否快速回復。
