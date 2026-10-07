---
name: doc-sync
description: Synchronize accepted decisions, review resolutions, or bounded findings into an existing Design Doc or technical document without creating new design. Use after decisions are already settled and the canonical document needs a faithful, consistency-preserving update.
---

# Doc Sync

把 **已確認的決策** 精準同步回既有 technical document。這是 document integration，不是 design iteration。

## Authority

由高到低：

1. 使用者明確 confirmed decisions；
2. accepted review findings / resolutions；
3. 已完成的 bounded decision memo / characterization result；
4. 既有 canonical document；
5. repository 只在 reference 明顯過期或來源互相衝突時做最小查證。

Doc Sync **沒有 design authority**。若需要選新的 ownership、API、protocol、runtime semantics、migration strategy 或 implementation policy，輸出 `REQUIRES DESIGN`，不要自行補完。

## Process

1. **Pin sources**：列出 canonical document 版本 / path，以及本次要同步的 accepted inputs。
2. **Build patch map**：把每個 accepted decision 對應到受影響 sections、diagram、interface sketch、runtime flow、table、acceptance criteria。
3. **Apply bounded edits**：只修改 decision 直接影響的內容與為了避免矛盾必須同步的 dependent wording。
4. **Propagate consistency**：更新 cross-reference、diagram label、terminology、status label；刪除已被 supersede 的舊 proposal。
5. **Anti-drift diff**：檢查新增的 type / method / ownership / behavior / dependency 是否都能追溯到 accepted input。
6. **Stop on design need**：追溯不到或 sources 互相矛盾時，保留原文並標示 `REQUIRES DESIGN`。

## Boundaries

不要：

- 重新探索 repository 來改善設計；
- 執行新的 tests / probes 來創造 decision；
- 因文件「看起來不完整」而新增 helper / API / abstraction；
- 把 implementation example 升格成 required contract；
- 重排 architecture / phases / estimate，除非 accepted input 明確要求。

可以做：

- wording cleanup；
- 刪除 superseded proposal；
- 把已接受 semantics 同步到所有相關 runtime / lifecycle views；
- 把 exact helper shape 降級為 example realization；
- 修正因同一 accepted decision 造成的圖文不一致。

## Completion criterion

完成時必須回報：

- Updated sections
- Decisions applied
- Derived consistency edits
- `REQUIRES DESIGN` items（若有）
- Confirmation：沒有新增未被 input 授權的 design decision

不需要再次執行 design self-audit；只做 source traceability 與 document consistency check。
