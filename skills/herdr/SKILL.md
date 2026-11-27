---
name: herdr
description: Control Herdr, a terminal multiplexer for coding agents. Use only when the user explicitly mentions Herdr or asks to use Herdr to inspect or control panes, tabs, workspaces, commands, or another agent. Do not use merely because a task could benefit from a background terminal, delegation, or parallel work. Requires HERDR_ENV=1.
---

# Herdr

完整指令由本機安裝的 herdr binary 提供，內容與這台機器的 herdr 版本一致。

1. 執行 `test "${HERDR_ENV:-}" = 1`。失敗代表不在 Herdr 管理的 pane 內：回報這點並停止。
2. 執行 `herdr --skill` 並讀完全部輸出。shell tool 截斷輸出時，分段補讀，例如 `herdr --skill | sed -n '100,220p'`。
3. 把印出的內容當成本 skill 的完整指令照做。

`herdr` 不在 PATH、`herdr --skill` 執行失敗或輸出為空時，回報這台機器沒有可用的 Herdr 並停止。
