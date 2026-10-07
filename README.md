# Agent Environment

個人的跨裝置 agent engineering environment。這個 repository 以 Matt Pocock skills 作為 pinned upstream base，只保留真正不同的 local architecture authority 與少量 global overlay。

- Matt Pocock skills = generic engineering workflow base
- local skills = 真正新增的 authority / artifact
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
├─ design       # formal Architecture Design Doc + bounded document maintenance
├─ challenge    # optional multi-role adversarial strengthening
└─ review       # independent acceptance + optional spec-fidelity mode

Lightweight overlay
└─ instructions/common.md
   ├─ architecture handoff: design → review
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

Architecture-changing feature / refactor 的 local overlay：

~~~text
grill-with-docs / wayfinder decisions
        ↓
      design
        ↓
   Design Doc draft
        ├─ optional challenge
        │      ├─ human decisions → grilling / grill-me
        │      └─ revisions → design
        ↓
      review (independent acceptance)
   ┌────┴──────────────────────────┐
REVISE / BLOCKED                 ACCEPT
   │                               ├─ small → implement → code-review
   └────────────→ design            │
                                   └─ durable contract → to-spec
                                          ├─ high-risk / multi-session
                                          │      → review (spec-fidelity)
                                          ├─ single-context → implement
                                          └─ multi-context
                                                 → to-tickets
                                                 → implement / implement-spec
~~~

`challenge` 與 `review` 不同：前者用多個獨立角色高 recall 地找盲點、不給 verdict；後者以 fresh independent reviewer 驗證 acceptance-relevant claims，低噪音地給 ACCEPT / REVISE / BLOCKED。

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
./agent-skills doctor
~~~

- **install**：第一次安裝或修復目前 checkout 宣告的 environment。
- **update**：平常唯一的維護指令。更新本 repo、同步目前 pin、檢查 Matt upstream、reconcile installation，最後 health check。
- **doctor**：覺得環境有問題時使用；執行 installer tests 並驗證實際安裝的 symlinks / manifest。

`test`、`verify`、`upstream` 不再是 public CLI concepts。底層 Python commands 仍保留給 installer 開發與 troubleshooting。

## New device installation

需要 Git、Python 3.10+，以及可讀取本 private repository 的 GitHub SSH 設定。

~~~sh
git clone --recurse-submodules git@github.com:iceboxi/agent-skills.git ~/Documents/agent-skills
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
4. fetch Matt `origin/main` 並檢查是否有新版。
5. 若沒有新版：tests → install/reconcile → verify。
6. 若有新版：互動詢問是否升級。

若選擇不升 Matt，現有 pin 不變，仍會完成本 repo 的 update / reconcile / health check。

若接受 Matt 更新：

~~~text
checkout latest Matt revision
        ↓
validate selected upstream skills
        ↓
tests
        ↓
install / reconcile
        ↓
verify
        ↓
commit parent-repo submodule pin
        ↓
push
~~~

如果 validation 失敗，CLI 會把 submodule checkout 還原到更新前的 pin，不提交新版。在 non-interactive 環境發現 Matt 新版時，預設保持目前 pin。

## Health check

環境看起來不對時：

~~~sh
./agent-skills doctor
~~~

它同時執行 installer/unit tests 與 actual installed-environment verification。一般使用者不需要分辨底層的 `test` / `verify`。

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
