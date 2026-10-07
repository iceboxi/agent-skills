# Agent Environment

個人的跨裝置 agent engineering environment。Repository 名稱維持 \`agent-skills\`。共用規則與 skills 各自只有一份 source of truth，由 installer 建立本機 symlinks。

這套 workflow 借鑑 Matt Pocock skills 的核心結構，但保留我們自己的 architecture baseline：

- **Human alignment**：grilling / domain-modeling
- **Repository-grounded architecture**：explore → design → review
- **Implementation synthesis**：spec → spec-review
- **Execution decomposition**：work-breakdown
- **Implementation**：implement / implement-spec + tdd → code-review
- **Feedback loop**：retro
- **大型未知 effort**：wayfinder
- **Architecture health**：improve-codebase-architecture

## Router

不知道該用哪支時，先用 \`ask-skills\`。Router 只能 shortlist；推薦或跳過 candidate 前，必須實際讀 candidate 的 \`SKILL.md\`。

## Main flow

\`\`\`text
idea / change
    ↓
grill-with-docs              ← requirement / trade-off 尚未收斂時
    │
    ├── research             ← external fact
    ├── prototype            ← runnable uncertainty
    └── domain-modeling      ← glossary / durable ADR
    ↓
design ← codebase-design
    ↓
review
 ┌──┴──────────────────────────────────────────────────┐
 │                                                     │
REVISE                                              ACCEPT
 │                                                     │
 └──────────────→ design                                ├─ small → implement
                                                       │            ↑
                                                       │           tdd
                                                       │            ↓
                                                       │        code-review
                                                       │
                                                       ├─ durable contract
                                                       │      ↓
                                                       │     spec
                                                       │      ↓
                                                       │  spec-review
                                                       │      ├─ single-context → implement
                                                       │      └─ multi-context
                                                       │             ↓
                                                       │       work-breakdown
                                                       │          ├─ per item → implement
                                                       │          └─ whole graph → implement-spec
                                                       │                              ↓
                                                       │                         code-review
                                                       │
                                                       ├─ accepted decision merge → doc-sync
                                                       └─ presentation → report

after implementation / difficult session
    ↓
retro
    ↓
skill / instruction / tooling / guardrail improvements
\`\`\`

\`spec\` 只做 accepted decisions 的 synthesis；\`work-breakdown\` 才拆 tracer-bullet / expand-contract work graph。不要再把兩個 phase 合在一起。

## On-ramps

| Situation | Skill | Exit |
| --- | --- | --- |
| 不理解 current repository | \`explore\` | current-state evidence model |
| hard bug / flake / performance regression | \`diagnosing-bugs\` | exact red loop → fix → regression evidence |
| 不知道哪裡值得 architecture 投資 | \`improve-codebase-architecture\` | visual candidate report → selected candidate grilling |
| effort 大到 multi-session 且 route 不可見 | \`wayfinder\` | resolved decision map → design/spec |
| plan 不在 repository 或不想寫 domain docs | \`grill-me\` | shared understanding |
| knowledge 在另一個人腦中 | \`questionnaire\` | external human evidence |
| 必須由人操作 dashboard / credential / cutover | \`wizard\` | verified manual result |

## Shared primitives

這些可被其他 workflow skill reach：

| Skill | Responsibility |
| --- | --- |
| \`grilling\` | decision-tree frontier；facts 由 agent 查，decisions 由 human confirm |
| \`domain-modeling\` | GLOSSARY / domain scenarios / sparse durable ADR |
| \`codebase-design\` | deep module、interface、seam、adapter、depth、locality、leverage |
| \`research\` | repository 外 authoritative technical facts |
| \`prototype\` | throwaway artifact 解一個 design/runtime/UI question |
| \`tdd\` | new behavior red-green + legacy characterization |
| \`code-review\` | correctness、spec/design fidelity、locality、verification |
| \`writing-for-agents\` | skill / AGENTS / agent-facing docs 的 context-load 與 pruning discipline |
| \`change-summary\` | PR/MR body 的 smallest visual、before/after evidence、merge danger |

## Core artifacts and authority

| Skill | Can make new architecture decisions? | Main artifact |
| --- | ---: | --- |
| \`grill-with-docs\` | human-confirmed decisions only | conversation + glossary / sparse ADR |
| \`design\` | ✅ | Design Doc |
| \`review\` | ❌ | acceptance verdict |
| \`doc-sync\` | ❌ | bounded canonical-doc update |
| \`spec\` | ❌ | implementation contract |
| \`spec-review\` | ❌ | spec fidelity verdict |
| \`work-breakdown\` | ❌ | execution graph |
| \`implement\` / \`implement-spec\` | ❌ | code |
| \`report\` | ❌ | presentation |

## Phase boundaries

Context move 只在 phase boundary 決定。詳細規則見 \`skills/ask-skills/phase-boundaries.md\`。

優先順序：

1. 下一 phase 仍需要 primary reasoning 且 context 健康 → **continue**
2. 舊 context 完全無關 → fresh / clear
3. 跨 harness / directory / repo / colleague → \`handoff\`
4. bounded AFK side task → subagent
5. context relevant 但過大 → compact

不要把 handoff / compact 當成每階段固定 ceremony。

## Skill catalog

\`\`\`text
skills/
  ask-skills/
  grilling/
  grill-me/
  grill-with-docs/
  domain-modeling/
  explore/
  research/
  prototype/
  codebase-design/
  improve-codebase-architecture/
  wayfinder/
  design/
  review/
  doc-sync/
  spec/
  spec-review/
  work-breakdown/
  implement/
  implement-spec/
  tdd/
  diagnosing-bugs/
  code-review/
  change-summary/
  questionnaire/
  wizard/
  handoff/
  writing-for-agents/
  retro/
  report/
\`\`\`

每個 skill directory 至少有 \`SKILL.md\` 與 \`agents/openai.yaml\`；branch-specific references 與 templates 跟 skill 放在同一目錄。專案 ownership、build/test commands 與 project-specific constraints 留在各專案自己的 \`AGENTS.md\` / repository docs。

## Matt mapping / deliberate differences

目前已內化 Matt engineering flow 的主要能力，但名稱與 artifact 依本 workflow 調整：

- \`ask-matt\` → \`ask-skills\`
- \`grilling / grill-me / grill-with-docs / domain-modeling\` → 保留核心 frontier + HITL + glossary/ADR 模型
- \`to-spec\` → \`spec\`，只做 accepted decision synthesis
- \`to-tickets\` → \`work-breakdown\`，保留 tracer bullets / blocking / expand-contract，但不要求 issue tracker
- \`implement-spec\` → \`implement-spec\`，以 Codex native subagents/worktrees 執行 frontier
- \`pr\` → \`change-summary\`，同時適用 GitHub PR / GitLab MR
- \`to-questionnaire\` → \`questionnaire\`
- \`improve-codebase-architecture / diagnosing-bugs / research / prototype / tdd / code-review / retro / wayfinder / wizard / handoff / writing-for-agents\` → 保留核心 reasoning pattern，再移除特定 harness / tracker 假設

我們另外保留：

- \`explore\`：formal repository-current evidence phase
- \`design\` + \`review\`：正式 Design Doc architecture baseline + acceptance gate
- \`doc-sync\`：已收斂 decisions 的 bounded document integration
- \`spec-review\`：Design Doc → implementation contract 的 fidelity gate
- \`report\`：accepted Design Doc 的 presentation extraction

目前**刻意不加入**：

- Matt \`triage\`：它主要管理 incoming issue / external PR 的 tracker state machine。等專案真的需要 GitHub/GitLab request intake automation 再設計 tracker-neutral 版本。
- Matt \`setup-matt-pocock-skills\`：我們已有跨 Codex/Claude/Cursor installer；domain docs 採 lazy creation，且 core workflow 不依賴 issue tracker。
- \`teach\` / \`wait-what\` 等一般 productivity skills：不屬於目前 engineering workflow 的缺口。

這些是 deliberate exclusions，不代表永久禁止；若 \`retro\` 或實際工作暴露 recurring need，再加入。

## 新裝置安裝

需要 Git、Python 3.10+，以及可讀取此 private repository 的 GitHub SSH 設定。Installer 使用 Python standard library；symlinks 安裝適用 macOS 與 Linux。各 CLI 本身與帳號登入另行設定。

```sh
git clone git@github.com:iceboxi/agent-skills.git ~/Documents/agent-skills
cd ~/Documents/agent-skills
python3 install.py --dry-run
python3 install.py
```

也可以使用已登入的 GitHub CLI：

```sh
gh repo clone iceboxi/agent-skills ~/Documents/agent-skills
```

Installer 依目前裝置的 home 與 clone 位置建立連結。不要從其他裝置複製舊的絕對路徑 symlinks。保留整個 repository 與穩定的 clone 位置，供連結及 skills 的相對引用使用。

所有由 installer 管理的入口都必須使用 symlink。Skills 連結整個目錄；Codex／Claude 的全域指引連結單一檔案。Installer 不以複製作為安裝方式或失敗時的替代方案，並在安裝結束時檢查每個連結可解析且指向此 repository。檢查失敗會觸發本次安裝的回復。

透過任一已安裝入口修改 `SKILL.md`、supporting files 或全域指引，都會直接修改 repository 的工作目錄。Symlink 不會自動 commit／push；修改完成後仍須提交並同步到遠端。

| 安裝入口 | 指向 |
| --- | --- |
| `~/.agents/skills/<name>` | `<clone>/skills/<name>` |
| `~/.codex/skills/<name>` | `<clone>/skills/<name>`，保留既有 Codex 相容入口。 |
| `~/.claude/skills/<name>` | `<clone>/skills/<name>` |
| `~/.cursor/skills/<name>` | `<clone>/skills/<name>` |
| `~/.codex/AGENTS.md` | `<clone>/instructions/common.md` |
| `~/.claude/CLAUDE.md` | `<clone>/instructions/common.md` |

上述 Codex 入口使用預設 `CODEX_HOME`；若使用自訂 profile，需另外設定其入口。`--home <path>` 可對指定 home 安裝，或在 temporary directory 驗證安裝結果。

Codex 在 session 開始時載入全域與專案指引；更新全域規則後開啟新 session。若 `AGENTS.override.md` 存在，它會優先於同層 `AGENTS.md`。見 [Codex AGENTS.md 官方說明](https://learn.chatgpt.com/docs/agent-configuration/agents-md)。

Claude Code 從 `~/.claude/CLAUDE.md` 載入跨專案個人指引；更新後開啟新 session，可用 `/context` 確認載入的 memory files。這裡的安裝目標是 Claude Code CLI；Cowork desktop sessions 對工作目錄外的 symlinks 有額外限制。見 [Claude Code memory 官方說明](https://code.claude.com/docs/en/memory)。

### Cursor 全域規則

Skills 由 installer 安裝。全域規則使用 Cursor 官方文件中的 `Customize → Rules → User Rules` 入口：

```sh
cat instructions/common.md
```

將輸出的全文貼入一項專用的 User Rule，保留其他已有規則。更新 `common.md` 後，同步更新該 User Rule 的內容。Installer 不寫入 Cursor 的設定資料庫，也不將 `~/.cursor/AGENTS.md` 當成已確認的自動載入入口。見 [Cursor Rules 官方說明](https://cursor.com/docs/rules)。

## 更新與跨裝置同步

```sh
cd ~/Documents/agent-skills
git pull --ff-only
python3 install.py --dry-run
python3 install.py
```

既有 skills 與 Codex／Claude 全域指引會透過 symlinks 取得新內容。執行 installer 會把安裝狀態 reconcile 成目前 repository 的 desired state：新增缺少的 skill links，並自動移除仍直接指向此 repository `skills/<name>`、但該 source skill 已不存在的 stale managed symlinks。其他 repository 的 symlink、一般目錄或一般檔案都不會被刪除。Cursor 的 User Rule 依上節同步更新。

在任何裝置修改共用內容後，以一般 Git commit／push 同步；其他裝置再 pull。專案 `AGENTS.md` 由各專案自己的 repository 同步。

## 移轉既有安裝

預設遇到同名目錄、檔案或不同連結就停止；全部目的路徑通過檢查前不寫入。Installer 不提供強制覆寫，也不自動合併不同規則。

內容完全相同的 skills 目錄或全域指引檔案，可明確移轉：

```sh
python3 install.py --adopt-identical --dry-run
python3 install.py --adopt-identical
```

如果舊的全域指引是 `common.md` 已完整包含的一個文字區塊，可以使用：

```sh
python3 install.py --adopt-instructions --dry-run
python3 install.py --adopt-instructions
```

`--adopt-instructions` 只適用 Codex／Claude 的全域指引。它要求舊文件的完整非空文字按原順序出現在 `common.md` 中，並符合整行邊界；只忽略文件兩端空白。不會挑出幾條規則後丟棄其餘內容。如果兩種移轉都有需要，可以同時使用兩個 flags。

其他不同內容會保留並阻擋安裝。先比較規則，再決定哪些應納入共用來源。新內容無法符合上述檢查時，先手動備份並處理既有入口，再重跑安裝。

移轉會把原項目移至 `~/.local/share/agent-skills/backups/<timestamp>/`，再建立新連結。一般檔案的備份保存原始 bytes；既有 symlink 的備份保存原連結。檔案若在 preflight 後被修改，installer 會停止該次移轉。安裝失敗時會嘗試還原本次修改的項目。

內容不同、dangling symlink 或 skills 內另含 symlinks 的項目會停止移轉。成功移轉後保留備份，確認各 CLI 可以使用後，再自行整理。若變更 clone 位置，先保留原 clone，再以 `--adopt-identical` 移轉相同內容的既有連結。

## 驗證

```sh
python3 -m unittest discover -s tests -v
python3 install.py --dry-run
python3 install.py --verify
```

`--dry-run` 顯示需要安裝或移轉的項目；`--verify` 只檢查已安裝結果，不建立連結、不移轉既有項目，也不建立備份。缺少入口、一般副本、錯誤目標或失效 symlink 都會失敗，即使副本內容與 repository 完全相同。可在各裝置更新後執行此檢查。`--verify` 不可與 `--dry-run` 或移轉 flags 同時使用。

Tests 在 temporary directories 驗證首次安裝、重跑、來源更新、相對引用、全域指引衝突、相同或已包含指引的移轉、備份、preflight 後的編輯、安裝錯誤回復，以及唯讀 symlink 驗證。它們不修改真實 CLI 設定，也不代表多輪模型行為已實測。
