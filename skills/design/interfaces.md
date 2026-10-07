# Interfaces & Ownership Guidance

## Contents

- Degrees of freedom
- Ownership dimensions
- Protocol / interface contract
- Capability-minimal boundaries
- Abstraction traceability
- Async / cancellation semantics
- Complexity guardrails

## Degrees of freedom

Software design 是高 freedom reasoning task。不要把 skill 寫成固定 architecture recipe。

### Low freedom：必須遵守

- CURRENT / PROPOSED / CONFIRMED / PLANNED VALIDATION 不混淆。
- canonical state 不得無意間形成雙 owner / 雙 writer。
- significant protocol 必須有 purpose、consumer、implementer、placement。
- refactor 必須保留或明確改變 behavior invariant。
- architecture / runtime / migration 語意不能混在同一個不明確 view。
- 未驗證事項不得寫成已完成。

### Medium freedom：提供 preferred shape

- interface sketch 深度；
- phase granularity；
- diagram decomposition；
- migration / validation strategy；
- error / lifecycle detail；
- file organization。

依 scope / risk 調整，不要求每份文件同形。

### High freedom：讓 repository evidence 決定

- architecture pattern 名稱；
- class / protocol 數量；
- concrete type vs protocol；
- naming；
- section ordering；
- file split；
- helper implementation style。

如果不同做法不會破壞 requirement / invariant，不要用 skill 強制單一路徑。

## Ownership dimensions

分別回答：

- **State ownership**：canonical state 在哪裡？
- **Workflow ownership**：sequence / retry / progress / timeout 誰持有？
- **Policy ownership**：feature / business decision 誰做？
- **Integration ownership**：BLE / DB / network / OS / legacy adapter 誰接？
- **Presentation ownership**：render / interaction / UI-only state 誰持有？

同一 domain 不代表上述責任都塞進同一 class。

## Protocol / interface contract

每個 significant protocol / interface 說明：

- Purpose / problem solved
- Consumer
- Implementer
- Responsibilities
- Non-responsibilities
- Key methods / data
- Error semantics（relevant 時）
- Concurrency / lifecycle（relevant 時）

提供足以 review 的 code sketch，但不要寫完整 implementation。

## Capability-minimal boundaries

Consumer-facing interface 只暴露真實 consumer 需要的能力。

特別檢查：

- owner-only mutation
- ingress / hydration
- persistence / upload
- migration control
- raw event stream
- reset / administrative APIs

這些預設保持 internal / narrower boundary。不要因同一 domain 支援它們，就做成「萬能 Client」。

## Abstraction traceability

significant abstraction 至少要能從下列一處追到：

- Design Realization diagram；
- responsibility / contract table；
- runtime flow；
- integration / migration mapping；
- code sketch + 明確 placement 說明。

但若 abstraction 影響「位置、owner、dependency、interaction」，只靠 table 不夠，應在對應 diagram 出現。

## Async / cancellation semantics

Behavior-preserving refactor 遇到 timer、retry、observer、DispatchQueue / TaskDispatcher、delayed callback 或其他 queued work 時，不要把它們統一成一個 generic `cancel` 語意。

必須依 repository evidence 區分至少這些 lifecycle stage：

- 尚未排程；
- timer / delayed work 已排程但尚未觸發；
- callback 已觸發、後續 retry / next-step 已 enqueue；
- queued work 已開始執行；
- operation 整體 invalidated。

**移除 observer、停止尚未觸發的 timer、阻止已 enqueue work、取消整個 operation 是不同 semantics，除非 current evidence 證明等價。**

若 finish / disconnect / scene exit / scope invalidation 會改變 asynchronous work，Design Doc 應明確說明：

1. 哪些尚未觸發的 work 被取消；
2. 哪些已 enqueue 的 work 仍會執行；
3. 執行後是否會再建立新的 timer / retry；
4. observation removal 是否只停止 delivery，還是也停止 workflow；
5. operation generation / scope invalidation 從哪個 stage 開始阻止 side effect。

對 ordering-sensitive legacy flow，加入 characterization fixture 覆蓋「callback 已 enqueue next-step，但 lifecycle event 在 next-step 執行前發生」的 interleaving；不能只測 steady-state success / timeout。

## Complexity guardrails

新增 abstraction 前問：

1. 現有 concrete type 為何不足？
2. 它切斷哪個 coupling / responsibility？
3. 誰會 consume？
4. 誰 implement / own？
5. 新增的 wiring / testing / maintenance cost 是什麼？
6. 若拿掉它，哪個 invariant 或 extension ability 會變差？

不要用 protocol 數量判定好壞；也不要用「只有一個 service」掩蓋 god object。
