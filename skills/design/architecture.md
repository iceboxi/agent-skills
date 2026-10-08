# Architecture & Diagram Documentation Guidance

## Contents

- Boundary: explain, do not redesign
- Visual coverage
- View semantics
- Refactor and new feature
- Diagram construction
- Completeness audit

## Boundary: explain, do not redesign

本 reference 是 **documentation guidance**：用 diagrams 讓已確立的 architecture / state / workflow / migration 看得懂，不在畫圖過程引入新 owner、seam、protocol 或 runtime rule。

Source 來自確認過的需求、spec、implementation plan，以及必要的 repository code / tests。若來源矛盾或缺少 architecture-critical relationship，標為 `UNRESOLVED`，不能藉由補一條箭頭來替使用者決策。

Tables explain properties; diagrams explain placement and interaction. **圖不是越少越好**，但不能為了補圖數製造沒有根據的細節。

## Visual coverage

對 non-trivial refactor，讀者應能從圖回答：

1. Current responsibility、dependency、state ownership 與耦合問題在哪裡？
2. Target external owner / boundaries / dependency direction 是什麼？
3. 重要 internal collaborators / protocols / state owners 如何放在 target 內？
4. 代表性 behavior / callback ordering 的 Current → Target flow 是什麼？
5. 有 temporary bridge 時，新舊 world 如何共存、何時 retirement？

一張清楚的圖可以涵蓋數個相容問題，但不能用 table / prose 代替 placement / interaction。Overview 精簡時要用 local realization view 補足被隱藏的重要 protocol 或 state owner。

## View semantics

| View | 主要回答 |
| --- | --- |
| Current Architecture | 已存在的 owner / dependency / state / coupling |
| Target Architecture Overview | 已決定的 long-term external boundary 和 responsibility |
| Target Design Realization | target 內的 protocols、concrete collaborators、state owners |
| Runtime / Sequence | callers、callbacks、ordering、read/write、side effects |
| Integration | 已決定的 OS / network / BLE / DB / legacy seam |
| Migration / Transitional | coexistence、bridge、cutover、retirement conditions |

靜態 dependency、runtime call、callback、data flow 不要混用不明確的箭頭；必要時拆圖或加 legend。

## Refactor and new feature

Refactor 視來源充足程度通常提供：

- scoped Current Architecture；
- Target Architecture Overview；
- Target Design Realization（有重要 internal collaborator / protocol 時）；
- representative Current / Target runtime flows；
- Current → Target responsibility mapping；
- transitional view（存在 bridge / coexistence 時）。

New feature 沒有 before counterpart 時，展示現有 integration context / constraints，再展示 Target。不能虛構一條「舊版新功能」流程。

對 retry / timeout / auto-sync / persistence / background lifecycle / multi-step ACK 等複雜系統，當 overview 無法交代重要 state / workflow owner 或 ordering 時，加入 subsystem architecture / sequence view。

## Diagram construction

- 圖先定義要回答的問題，再選 nodes / edges；以責任與 owner，而非完整 class 清單，作為 overview 主軸。
- 使用 repository 已知 current names 與已確認 target names；current vs proposed 必須明確區分。
- Protocol / function relation 應與 code sketches 的名稱一致，讓讀者能找到 consumer、implementer、placement。
- 相同角色的 helpers 可合併；真正影響 dependency / state / lifetime 的 collaborator 不能在所有視圖中消失。
- 太大的圖拆成 overview + local view，不透過縮小文字或刪除重要關係假裝簡潔。
- Mermaid 圖交付前檢查 syntax、圖示標籤、edge 方向、legend；若未真的 render，不能聲稱 render verified。
- 如果缺少足以畫出確定箭頭的 source，改在相應節標示 unknown 與影響，不自創連線。

## Completeness audit

- [ ] Current / integration context 圖有 code evidence，Target 圖不冒充 current。
- [ ] 重大 ownership 與 protocol placement 能從圖看到，而不只出現在表格中。
- [ ] 重要 runtime before / after flow 與 migration transition（適用時）可理解。
- [ ] 每個具體 arrow 都是 source-backed，沒有為美觀加上想像的 dependency。
- [ ] 圖示增進可讀性，而非只重複文字。
