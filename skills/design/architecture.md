# Architecture & Diagram Guidance

## Contents

- Visual coverage contract
- View semantics
- Refactor defaults
- Diagram construction rules
- Anti-patterns
- Local subsystem views
- Architecture audit

## Visual coverage contract

Design 的目標不是「圖越少越好」，而是讓 reviewer 能直接看懂 ownership、placement、interaction 與 migration。

**Tables explain properties; diagrams explain placement and interaction.**

若問題本質是「元件在哪裡、誰連到誰、誰持有誰、runtime 怎麼走」，table / prose 不可取代必要的 architecture / sequence view。

對 non-trivial refactor，至少要讓文件以視覺方式回答下列適用問題：

1. **Current Structure**：造成問題的 current responsibilities / dependencies 在哪裡？
2. **Target External Architecture**：完成後主要 responsibility boundaries 與 dependency direction 是什麼？
3. **Target Internal Realization**：外部 owner 內的重要 collaborators / protocols / state owners 如何組合？
4. **Representative Runtime Before / After**：重要 behavior / ordering 如何由 current 轉到 target？
5. **Migration / Transitional Architecture**：若非一次切換，新舊 world 如何共存、何時退役 bridge？

不以固定圖數驗收；若一張圖能清楚回答兩個相容問題可以合併，但不能因「已有 table」就省略 placement / interaction 所需的圖。

## View semantics

| View | 主要回答 |
| --- | --- |
| Current Architecture | current responsibility、coupling、state / dependency placement |
| Target Architecture Overview | 長期 external ownership、major boundaries、dependency direction |
| Design Realization | protocols / concrete collaborators / state owners 在 target 內的位置 |
| Runtime / Sequence | call、callback、ordering、state read/write、side effects |
| Integration | target 與 BLE / DB / network / OS / legacy infrastructure 的接點 |
| Migration / Transitional | temporary facade / bridge / dual-path / retirement relationship |

Target Architecture Overview 是第一層，不是唯一一層。若 Overview 為了清楚而省略 internal collaborators，Design Realization 必須補足到 reviewer 能看懂重要 protocol / workflow / state owner 的位置。

## Refactor defaults

Behavior-preserving refactor 通常至少包含：

- scoped Current Architecture；
- Target Architecture Overview；
- Target Internal Realization（只要 target owner 內有多個 significant collaborators / protocols / workflow owners，就視為需要）；
- representative Current runtime flow；
- equivalent Target runtime flow；
- Current → Target responsibility mapping；
- 有 temporary bridge / coexistence 時的 Migration / Transitional view。

複雜 subsystem（例如 pattern transfer、sync、persistence、background task、multi-step ACK flow）若無法從主圖理解 ownership / interaction，加入局部 architecture 或 sequence view。

## Diagram construction rules

- 每張圖先寫出它要回答的問題，再選 node。
- 主圖從 responsibility / owner 出發，不從 type 清單出發。
- static dependency、runtime call、callback、data flow 不混用同一種箭頭；必要時用 legend 或拆圖。
- 多個 concrete types 同一 architecture role 時可合併，但 adjacent text/table 要列出 realization。
- pure helper / DTO / codec 不因存在就升成 peer architecture node；只有它影響 boundary / ownership / dependency 時才畫。
- legacy infrastructure 展開到設計成立所需的深度即可。
- 圖中的名稱與 code sketch / tables 使用同一 vocabulary。
- 圖太大時拆成 overview + local view，不以縮字或省略重要 relationship 解決。

## Anti-patterns

- 只有「Consumers → Domain → Outputs」三個 box，卻沒有補 internal realization。
- protocol 有 code sketch，但讀者找不到它位於哪個 responsibility boundary。
- 用 responsibility table 取代 owner / dependency placement 圖。
- 為了追求少圖，把 persistence / workflow / migration 的重要 wiring 全部埋在 prose。
- 為了追求完整，把所有 helper / task / singleton 全塞進一張 giant graph。
- diagram 看似有 cycle，實際只是把不同 abstraction level / runtime callbacks flatten 在一起。

## Local subsystem views

當下列任一成立時，優先增加局部圖：

- 有獨立 workflow state（retry / timeout / progress / rollback）；
- 有多 owner 交互且 ordering 重要；
- persistence / background task 的 read-time / write-time semantic 重要；
- protocol placement 用 table 仍難以理解；
- auto / manual flow 共用 mechanics 但 policy owner 不同；
- migration 中新舊 responsibility 暫時分離。

局部圖只回答該 subsystem；不要重畫整個系統。

## Architecture audit

交付前檢查：

- [ ] Current problem 是否能從圖或 flow 直接看懂？
- [ ] Target Overview 是否清楚顯示 external owner / boundaries？
- [ ] Significant internal collaborators / protocols 是否有 placement？
- [ ] Canonical / draft / workflow state owner 是否可視化或明確映射？
- [ ] Representative behavior 是否有 before / after flow？
- [ ] Transitional wiring 若存在，是否可看懂且有 retirement condition？
- [ ] 是否有 table 正在替代其實需要的 relationship diagram？
- [ ] 是否有圖只是重複文字而沒有增加 spatial / interaction information？

任一重要問題回答不了，先修 Design Doc，再交付；不要把 audit failure 留成文件中的 vague limitation。
