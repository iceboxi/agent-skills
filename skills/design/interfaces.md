# Interface, State & Runtime Documentation Guidance

## Contents

- Evidence and authority
- Ownership mapping
- Protocol contract and sketches
- Async / cancellation semantics
- Fidelity audit

## Evidence and authority

本 reference 指導 **記錄已確立的技術設計**，不是新增 abstraction 的設計教學。Source 可以是先前確認的 architecture decisions、implementation spec、已解析的 ADR / prototype evidence 與 repository current facts。

整理 protocol / function 時可以將相同決策畫成關係圖或轉為精簡 code sketch，但不能默默決定新的 public API、seam、concrete adapter、ownership 或 failure semantic。

若沒有足夠的 signature/detail，可列出已知 contract + `UNRESOLVED`；不要用編造的可編譯程式碼掩蓋缺漏。示意性 sketch 標 `ILLUSTRATIVE`，不具有超出來源的約束力。

## Ownership mapping

整理已知的：

- **State ownership**：canonical、draft、workflow、temporary state 的 owner。
- **Workflow ownership**：ordering、retry、progress、timeout 由誰控制。
- **Policy ownership**：feature / business decision 由誰做。
- **Integration ownership**：BLE / DB / network / OS / legacy adapter 在哪裡。
- **Presentation ownership**：render、interaction、UI-only state 在哪裡。

單一 domain 不代表上面都由同一個 class 負責；不可因為圖示簡化而誤導為雙 owner 或全能 object。

## Protocol contract and sketches

對每個 significant protocol / interface，從來源整理：

- Purpose / problem solved
- Consumer / caller
- Implementer / adapter
- Placement / owning module
- Responsibilities / non-responsibilities
- Key methods / data contract
- Error / concurrency / lifecycle contract（relevant 時）

在 Design Realization diagram 中顯示其位置，重要 call / callback 在 sequence view 中對應。Code sketches 優先表達已定案的 capability 與 method relationship；不要為了填滿畫面而增加 method 或 protocol。

`ILLUSTRATIVE` code sketch 可以略去 implementation noise，但若名稱、參數或回傳型別並非已確認，就用概念性 placeholder 或註明未定，不要將其偽裝成確定 API。

## Async / cancellation semantics

Refactor 描述 legacy async 行為時應從 repository evidence 區分：

- work 尚未排程；
- timer / delayed work 已排程但尚未觸發；
- callback 已觸發並 enqueue 後續 work；
- queued work 已開始執行；
- operation / scope 已 invalidated。

移除 observer、停止 timer、取消 queued work、invalidate 整個 operation 可能各有不同語意。只有在來源明確證實時才能寫成相同。

針對 finish / disconnect / scene exit 等事件，忠實呈現已確認的：哪些 work 停止、哪些可繼續、是否再排程、何時阻止 side effects。若 spec 沒有處理重要交錯情境，標示 gap，不由 Design Doc 自行發明 cancellation policy。

## Fidelity audit

- [ ] 重大 contract 有 purpose、consumer、implementer、placement。
- [ ] State owner、workflow owner、policy owner 不混淆。
- [ ] Code sketches、diagram 與 prose 用同一 vocabulary。
- [ ] 沒有將 illustrative type / helper 擴張成新的 architecture decision。
- [ ] Lifecycle / async edge cases 沒有把 assumption 偽裝成既有行為或已定案 contract。
