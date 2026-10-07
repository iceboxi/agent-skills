---
name: challenge
description: Adversarially strengthen an existing technical design or Design Doc with multiple independent reviewer perspectives. Use after a draft exists and before acceptance review when the goal is to uncover blind spots, hidden assumptions, weak interfaces, runtime/migration risks, or unresolved human decisions. Produces a consolidated challenge set, not an acceptance verdict.
---

# Design Challenge

用多個彼此獨立的角度攻擊既有 Design Doc / technical proposal，目標是 **找盲點並強化設計**，不是判定 ACCEPT / REJECT。

這是一個高-recall critique pass：可以提出值得調查的 hypothesis，但必須和已證實 finding 分開。不要把 speculative concern 寫成 repository fact。

## 1. Inputs

至少需要：

- review subject：Design Doc / technical proposal；
- confirmed goals、scope、constraints、accepted decisions；
- relevant repository access，讓 factual challenge 可以自行查證。

文件作者的完整 reasoning history 不是必要輸入。Reviewer 應優先看 artifact、authoritative decisions 與 primary repository evidence。

## 2. Choose perspectives

依 scope 選 3–6 個真正不同的角色，不固定湊數。常用 perspectives：

- **Architecture / ownership**：state、workflow、policy owner，dependency direction，module depth / locality；
- **Interface / seam**：consumer surface、protocol placement、adapter necessity、cross-language contract；
- **Runtime / lifecycle**：ordering、retry、timeout、concurrency、callback lifetime、background / device behavior；
- **Migration / compatibility**：coexistence、cutover、rollback、state transfer、legacy contract；
- **Verification**：characterization、regression seam、independent oracle、device-only evidence；
- **Simplicity / extensibility**：speculative abstraction、middle-man layers、shotgun surgery、representative change locality。

只選和本次 design 有實際 failure mode 的 perspectives。

## 3. Independence

優先把每個 perspective 交給不同的 fresh agent / subagent，並行執行。

每個 challenger 只拿：

- Design Doc / proposal；
- confirmed requirements / decisions；
- repository 與 project instructions；
- 自己的 perspective brief。

不要把其他 challenger findings 先餵給它，也不要把作者未寫進 artifact 的辯護 reasoning 當 baseline。

如果 harness 無法建立獨立 agent，改做明確分隔的 sequential perspective passes，並在輸出標示 independence 降級；不要假裝是 multi-agent result。

## 4. Challenger contract

每個 challenger：

1. 先查 facts，再 challenge。
2. 需要 module/interface vocabulary 時使用 `codebase-design`。
3. repository 外 technical fact 用 `research`；paper reasoning 無法回答的 runtime/UI/integration question 指向 `prototype`。
4. 不替 human 做 product / engineering trade-off decision。
5. 不需要給 acceptance verdict。

每個 finding 用：

- **Perspective**
- **Challenge**
- **Type**：`EVIDENCE GAP | DESIGN GAP | HUMAN DECISION | VALIDATION GAP | HYPOTHESIS`
- **Evidence**：repository `file:line` / accepted requirement / doc section；hypothesis 可明確寫尚無 evidence
- **Impact**
- **Question / next investigation**

可以提出 alternative shape 來暴露 trade-off，但不要把它偷偷升格成 accepted replacement design。

## 5. Synthesis

所有 perspective 完成後才合併：

- 去除只是換句話說的重複 finding；
- 保留不同角色對同一處的不同 failure mode；
- 明確標出彼此衝突的 challenger assumptions；
- 將結果分成：
  - **Document correction**：不需要新 decision；
  - **Design gap**：需要回 `design`；
  - **Human decision gap**：需要 live `grilling` / `grill-me`；
  - **Validation gap**：需要 research / prototype / characterization。

Human decision gap 必須真的交給 human。不要讓 challenger agent 自己模擬使用者回答。

## 6. Output

先給 3–8 個最高價值 challenges，再給完整 consolidated set。不要用 severity / ACCEPT verdict；那是 `review` 的 authority。

最後列：

- **Decisions to grill**
- **Design revisions suggested**
- **Validation work suggested**
- **What survived challenge**：重要但未被任何 perspective 推翻的核心 decisions

Challenge 完成不代表 Design Doc 已 accepted。

## 7. Handoff

```text
design draft
    ↓
challenge
    ├─ human decision gaps → grilling / grill-me
    ├─ validation gaps → research / prototype / characterization
    └─ design/doc gaps → design / document-maintenance
                            ↓
                          review
```

如果 challenge 沒有找出需要改變 design 的問題，可以直接進 `review`；仍由 review 獨立決定 acceptance。
