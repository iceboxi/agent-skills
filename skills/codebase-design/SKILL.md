---
name: codebase-design
description: Shared software-design discipline for module depth, seams, interface surface, locality, leverage, extension cost, and abstraction pressure. Use when designing or reviewing architecture, refactors, interfaces, or test seams; this is reference discipline, not an orchestration workflow.
---

# Codebase Design

這是 architecture / refactor / interface 工作共用的設計紀律。它不產生獨立 Design Doc，也不接管 workflow；`design`、`review`、`spec-review`、`code-review` 在需要判斷 module shape / seam / abstraction 時使用本 skill。

預設使用繁體中文；保留 repository terminology 與 code identifiers。

## Core vocabulary

- **Module**：對 caller 提供一個可理解 interface、內部封裝 implementation 的單位；尺度可以是 function、type、feature slice 或 subsystem。
- **Interface**：caller 正確使用 module 必須知道的全部 contract，不只 method signature，也包含 state、ordering、error、lifecycle、concurrency 與 capability surface。
- **Seam**：behavior 可以被替換、隔離或驗證的位置；先決定 seam 放哪裡，再決定 protocol / type shape。
- **Depth**：caller 需要理解的 interface 越小、背後承擔的 useful behavior 越多，module 越 deep。
- **Locality**：一個 logical change 應集中在負責該 policy / behavior 的少數位置，而不是散到 unrelated callers。
- **Leverage**：一個清楚 interface 能讓多個 callers / tests 重用同一份 behavior，而不複製 knowledge。
- **Adapter**：在 seam 上把外部 infrastructure / legacy implementation 接入 target contract 的 concrete role。

## Design pressure

設計或 review module 時問：

1. Caller 真正需要知道多少？
2. 刪掉這個 abstraction 後，complexity 是消失，還是散回多個 callers？
3. 一個 logical change 會集中在 owner，還是造成 shotgun surgery？
4. Common mechanism 是否隱藏 complexity，還是只增加 pass-through / middle-man layer？
5. Test 是否能經同一個 caller-facing seam 驗證 behavior，而不需要穿透 internals？
6. Abstraction 是否有 production responsibility；不要只為 mocking 製造 protocol。
7. Infrastructure seam 即使只有一個 production adapter，也可成立，但必須切斷真實 external / volatile dependency，而不是 hypothetical extensibility。

## Change-locality exercises

若 design 的 confirmed goal 包含「可擴充、易維護、容易新增 command / source / policy」，不能只用形容詞宣稱達成。選 1–3 個代表性變更做 extension exercise，例如：

- 新增一個普通 command；
- 改一個 command 的特殊處理；
- 新增 / 調整 merge source precedence；
- 替換一個 infrastructure adapter；
- 新增一個 consumer。

對每個 exercise 列出預期修改點與 **forbidden unrelated touchpoints**。若一般變更仍需修改 generic dispatch、legacy switch、unrelated persistence、transport routing 或多個 callers，視為 locality failure，回頭檢查 seam / ownership。

不要要求「永遠只改一個檔案」；目標是讓修改半徑符合 responsibility，而不是追求形式上的 file count。

## Interface alternatives

當 interface realization 仍有實質 uncertainty 時，可做 adversarial alternatives：

1. 固定已確認 architecture / ownership，不重開無關 decision。
2. 產生 2–3 個 genuinely different interface candidates。
3. 每個 candidate 都回查 actual callers、implementers、runtime semantics 與 migration。
4. 用 depth、locality、capability surface、behavior preservation、test seam、migration cost 比較。
5. 最後選一個；不要平均折衷。
6. Evidence 不足的項目標成 `NEEDS CHARACTERIZATION`，不要用 aesthetics 補答案。

## Failure smells

特別警覺：

- shotgun surgery：一個 logical change 散落多個 unrelated modules；
- shallow abstraction：interface 幾乎和 implementation 一樣複雜；
- speculative generality：為尚不存在需求加入 hooks / protocols / options；
- middle man：只轉送、不吸收 complexity；
- bypass pressure：real callers 頻繁繞過 abstraction；
- duplicated ownership：同一 canonical fact 被多個 owners 可寫；
- generic mechanism 吸收 feature-specific policy；
- tests 只能靠 private hooks / internal mocks 才能驗證主要 behavior。

## Completion criterion

本 discipline 被正確使用時，reviewer 能清楚回答：

- seam 為什麼在這裡；
- caller 需要知道什麼、被隱藏什麼；
- state / workflow / policy 各由誰 owner；
- 代表性未來變更的修改半徑；
- tests 從哪個 interface 驗證 behavior；
- 哪些 abstraction 是真實 responsibility，而不是設計裝飾。
