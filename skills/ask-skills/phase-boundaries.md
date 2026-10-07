# Phase Boundaries

Context move 只在 phase boundary 決定。Mid-phase 若還沒完成，就 continue 或把 bounded side task 丟 subagent；不要為了「整理」隨便 compact。

按順序問，第一個成立的就用。

## 1. Can we continue?

若下一 phase 需要目前 conversation 的 reasoning 作 **primary source**，而 context 還在有效範圍，優先 continue。

Continue 沒有資訊損失，也是最便宜的選項。

典型：

- grill-with-docs → design
- design revision loop
- small accepted design → implementation（context 還健康時）

## 2. Is the old context irrelevant?

若下一 phase完全不需要前面的 reasoning，fresh / clear。

例如一個完全獨立的 accepted work item，所有必要資訊都已在 spec/work item 中。

## 3. Does context need portability?

只有在 context 要搬到：

- 另一個 harness
- 另一個 directory / repo
- colleague
- mid-phase fork

才用 handoff。

Handoff 的價值是 portability，不是整理筆記。

## 4. Can a bounded task run AFK?

能精確定義 input/output、無需持續 steering → subagent。

例如：

- external research
- bounded repository exploration
- independent review axis
- safe parallel work item

## 5. Otherwise compact

同 harness、同 directory、context 還 relevant，但 room 不夠 → compact。

Compact 是 fallback，不是第一選項；它把 primary source 變成 secondary summary，會損失 nuance。

## Primary vs secondary

- Continue：full primary source，資訊最多、noise也最多。
- Handoff / compact：secondary source，portable/乾淨但 lossy。
- Artifact pointer：只要 canonical decisions 已存在 Design Doc/spec/ADR，可用 pointer 減少重複。

所以 phase artifact 的存在，不代表應該立刻丟掉 conversation；先判斷下一 phase 是否仍需要「why」。
