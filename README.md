# Agent Environment

個人的跨裝置 agent engineering environment。這個 repository 以 Matt Pocock skills 作為 pinned upstream base，只保留真正不同的 local documentation / optional critique abilities 與少量 global overlay。

- Matt Pocock skills = generic engineering workflow base
- local skills = 獨立 Design Doc artifact / 選用 critique
- `instructions/common.md` = 輕量 workflow / Apple-platform overlay
- `skills-manifest.json` = 決定哪些 upstream skills 會被安裝
- Git submodule gitlink = upstream 版本唯一 pin

Matt upstream 採 MIT License；upstream 原始內容保持在 submodule，不直接修改。

## Layering

~~~text
Matt upstream
├─ ask-matt
├─ grilling / grill-with-docs / domain-modeling
├─ research / diagnosing-bugs / codebase-design
├─ prototype / tdd / wayfinder
├─ to-spec / to-tickets
├─ implement / implement-spec / code-review
├─ triage / pr / wizard
├─ handoff / teach / wait-what / to-questionnaire
└─ retro / writing-for-agents / ...

Our local skills
├─ design       # optional standalone post-spec/post-tickets Design Doc
├─ challenge    # manual adversarial critique
└─ review       # manual independent assessment

Lightweight overlay
└─ instructions/common.md
   ├─ optional standalone Design Doc after spec / work planning
   ├─ native Apple-platform prototype rule
   ├─ behavior-preserving characterization
   └─ device/runtime validation boundary
~~~

原則：**沒有新的 authority / artifact，就不要 fork upstream skill。** 平台差異、handoff 差異與 verification nuance 優先寫成短 overlay；只有 upstream 無法表達的正式流程才保留 local skill。

## Main engineering flow

不知道該用哪支 skill 時，直接使用 upstream router：

~~~text
$ask-matt
~~~

工程主流程恢復 Matt upstream 的預設分工：

~~~text
grill-with-docs / decisions
        ↓
      to-spec
        ↓
     to-tickets
        ├──────────────→ implement / implement-spec → code-review
        │
        └── 需要獨立 Design Doc 時（使用者指定）
                         ↓
                       design
                standalone Markdown
                         ↓
                implement / implement-spec → code-review
~~~

小型 single-context 工作可照 upstream 跳過不必要的 ticket 拆分。`design` 從已確立的需求、spec、工作規劃與相關 repository evidence，**只做 extraction / organization / visualization**，將 Current / Target architecture、protocol/function、state ownership、runtime、migration phases、工時與驗證整理成自足的固定格式 Design Doc；不重新做 architecture decisions。

**Design Doc 不露出 ticket ID、標題、狀態、tracker URL 或 ticket-to-phase mapping。** 詳細工作項目可彙整成工程 phase，但文件必須能獨立閱讀，不能要求讀者回到 tracker 或 spec 才看得懂。Implementation 仍依 spec 和確認過的工作規劃；實作發現新證據可適度調整，必要時才同步文件。

`challenge` 和 `review` 僅在使用者主動呼叫時執行；不自動串接，也不是 implementation 必經的 acceptance gate。

Repository current-state inspection 不再是獨立 skill；各 workflow 直接依需要讀 code/tests。Accepted Design Doc 的 bounded maintenance 也不是獨立 skill，而是 `design` 的 document-maintenance mode。

`prototype`、`tdd`、`wayfinder` 直接使用 upstream 版本；Apple/legacy/architecture-specific 差異由 `instructions/common.md` 補充，不維護 local fork。

Side paths:

- hard bug / flake / perf regression → diagnosing-bugs
- architecture health survey → improve-codebase-architecture
- huge route-invisible effort → wayfinder
- external technical fact → research
- runnable design / runtime / UI uncertainty → prototype
- test-first behavior work → tdd
- stateful learning → teach
- explanation did not land → wait-what
- GitHub/GitLab issue or external PR/MR intake → triage
- PR/MR reviewer summary → pr
- human-only provisioning / credentials / dashboard → wizard
- knowledge only another person has → to-questionnaire

GitHub、GitLab、local files 可以依專案分別設定；不同 repository 的 tracker / credentials / workflow 不混用。


## Temp artifact overrides

Matt upstream 的 artifact ownership 原則上不改，只修三個容易找不到輸出的位置：

~~~text
handoff
→ 有 repo context：
  <repo-root>/.scratch/artifacts/handoff/
→ 沒有 repo context：保留 upstream OS temp

improve-codebase-architecture
→ 可以照 upstream 在 $TMPDIR render
→ 有 repo context 時，final HTML promotion 到：
  <repo-root>/.scratch/artifacts/architecture/

research
→ 優先沿用 project 既有 research-note convention
→ 沒有 convention 才 fallback：
  <repo-root>/.scratch/artifacts/research/
~~~

其他 Matt artifacts 不搬家：

- `to-spec` / `to-tickets` / `wayfinder`：維持 configured tracker。
- prototype source：維持 upstream prototype / throwaway-branch 規則。
- Glossary、ADR、`docs/agents/*`、accepted Design Doc 等 canonical docs：維持 project 原本位置。

`.scratch/artifacts/*` 視為 non-canonical working state，不自動修改 tracked `.gitignore`、也不預設 commit。

## Skill sources

Local skills：

~~~text
skills/design/
skills/challenge/
skills/review/
~~~

Upstream skills：

~~~text
upstream/mattpocock-skills/
~~~

實際曝光哪些 upstream skills 由 `skills-manifest.json` 控制。Installer 會把 local + manifest-selected upstream skills 合併成一個 catalog；名稱衝突會直接失敗，不做隱式 override。

## Command-line interface

日常只需要三個指令：

~~~text
./agent-skills install
./agent-skills update
./agent-skills verify
~~~

- **install**：第一次安裝或修復目前 checkout 宣告的 environment。
- **update**：更新本 repo、同步已鎖定的 Matt submodule 版本、reconcile installation 並驗證；不自動升級 Matt、不 Commit／Push。
- **verify**：唯讀檢查 upstream pin、installer tests、symlinks / manifest，不初始化或修復檔案。

`test`、`upstream` 不屬於公開 CLI；底層 Python commands 保留供 installer 開發與 troubleshooting。

## New device installation

需要 Git、Python 3.10+，以及可存取本 private repository 的 GitHub HTTPS 認證。

~~~sh
git clone --recurse-submodules https://github.com/iceboxi/agent-skills.git ~/Documents/agent-skills
cd ~/Documents/agent-skills
./agent-skills install
~~~

若 clone 時沒有帶 `--recurse-submodules`，`install` 會自行初始化 parent repo pin 指定的 upstream revision。

Installer 使用 symlink，不複製 skill files：

~~~text
~/.agents/skills/<name>
~/.codex/skills/<name>
~/.claude/skills/<name>
~/.cursor/skills/<name>
~/.codex/AGENTS.md
~/.claude/CLAUDE.md
~~~

`install` 會先跑 tests，再 reconcile，最後 verify。從舊版升級時，同一 repo 管理的 symlink 可自動 retarget；已移除的 managed skill link 會被清理。

想只看 installation plan：

~~~sh
./agent-skills install --dry-run
~~~

## Normal update

平常不要再手動記 `git pull`、submodule、test、verify：

~~~sh
cd ~/Documents/agent-skills
./agent-skills update
~~~

`update` 會：

1. 確認 tracked working tree 沒有未提交修改。
2. `git pull --ff-only` 更新本 repo。
3. checkout parent repo 已信任的 Matt submodule pin。
4. 驗證 Matt checkout 與 Repository pin 一致。
5. 執行 tests → reconcile installation → verify。

日常 update 不會檢查 Matt 最新版本、不變更 upstream pin，也不自動 Commit / Push。Matt 新版本由維護者另外評估，確認後再透過 Git 更新並發布 pin。

## Health check

環境看起來不對時：

~~~sh
./agent-skills verify
~~~

它唯讀檢查 Matt submodule pin、執行 installer/unit tests，並驗證實際安裝環境。一般使用者不需要分辨底層的 `test` / `verify`。

底層 troubleshooting：

~~~sh
python3 -m unittest discover -s tests -v
python3 install.py --dry-run
python3 install.py --verify
python3 update_upstream.py
python3 update_upstream.py --update
~~~

## Adding or removing upstream skills

不要複製 upstream skill。編輯 `skills-manifest.json` 的 `upstream.skills`，然後：

~~~sh
./agent-skills install --dry-run
./agent-skills install
~~~

## Adoption / conflicts

預設遇到一般檔案、一般目錄或非本 repo 管理的同名 symlink 就停止，不 force overwrite。

完全相同的既有 skill / global instruction 可明確採用：

~~~sh
./agent-skills install --adopt-identical --dry-run
./agent-skills install --adopt-identical
~~~

既有 global instructions 若完整文字已包含在 `instructions/common.md`：

~~~sh
./agent-skills install --adopt-instructions --dry-run
./agent-skills install --adopt-instructions
~~~

## Local skill contract

只有真正由本 repo 維護的 local skill 需要：

~~~text
skills/<name>/SKILL.md
skills/<name>/agents/openai.yaml
~~~

Installer 會驗證 local metadata。Upstream skill 使用 Matt 自己的 `SKILL.md` invocation metadata，不要求我們額外包一份 `agents/openai.yaml`。

## Project bootstrap and trackers

Matt 的 `setup-matt-pocock-skills` 也會被安裝。它目前支援 GitHub、GitLab、local files 或其他 tracker convention。這些是 project-local configuration，不寫回本 agent-skills repo。

例如：

- NovelReader：可以使用 GitHub issue / PR workflow。
- MobileApp：可以使用 GitLab 或 local-file workflow。

兩個 project 的設定彼此獨立。

## Ownership summary

~~~text
Upstream generic engineering discipline
    → mattpocock/skills submodule

Our architecture workflow
    → local design / challenge / review

Our lightweight behavioral differences
    → instructions/common.md

Which upstream skills are active
    → skills-manifest.json

Which upstream revision is trusted
    → Git submodule gitlink

Project-specific build/ownership/tracker rules
    → each project's AGENTS.md / repository docs
~~~
