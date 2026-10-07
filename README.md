# Agent Environment

個人的跨裝置 agent engineering environment。這個 repository 不再 fork 大量通用 engineering skills；改成：

- Matt Pocock skills = pinned upstream base
- 本 repo skills = 我們真正不同的 workflow / architecture overlay
- skills-manifest.json = 決定哪些 upstream skills 會被安裝
- Git submodule gitlink = upstream 版本唯一 pin

Matt upstream 採 MIT License；upstream 原始內容保持在 submodule，不直接修改。

## Layering

~~~text
Matt upstream
├─ grilling / grill-with-docs / domain-modeling
├─ research / diagnosing-bugs / codebase-design
├─ to-spec / to-tickets
├─ implement / implement-spec / code-review
├─ triage / pr / wizard
├─ handoff / teach / wait-what / questionnaire
└─ retro / writing-for-agents / ...

Our local layer
├─ design         # formal Architecture Design Doc + bounded document maintenance
├─ review         # design acceptance + optional spec-fidelity mode
├─ prototype      # currently local Apple-platform adaptation
├─ tdd            # currently local characterization adaptation
└─ wayfinder      # currently local planning adaptation
~~~

原則：沒有真正差異就直接使用 upstream；不要複製 upstream SKILL.md 再改幾行。Router 直接使用 upstream `ask-matt`。只有新的 authority / artifact 才保留 local skill；較小差異優先以 reference / workflow overlay 表達。

## Main engineering flow

不知道該用哪支 skill 時，直接使用 upstream router：

~~~text
$ask-matt
~~~

Architecture-changing feature / refactor 的 local overlay：

~~~text
grill-with-docs
    ↓
design
    ↓
review
 ┌──┴──────────────────────────────────┐
REVISE                              ACCEPT
  │                                     ├─ small → implement → code-review
  └────────────→ design                  │
                                        └─ durable contract → to-spec
                                               ├─ high-risk / multi-session
                                               │      → review (spec-fidelity)
                                               ├─ single-context → implement
                                               └─ multi-context
                                                      → to-tickets
                                                      → implement / implement-spec
~~~

Repository current-state inspection 不再是獨立 skill；各 workflow 直接依需要讀 code/tests。Accepted Design Doc 的 bounded maintenance 也不是獨立 skill，而是 `design` 的 document-maintenance mode。

Side paths:

- hard bug / flake / perf regression → diagnosing-bugs
- architecture health survey → improve-codebase-architecture
- huge route-invisible effort → wayfinder
- external technical fact → research
- runnable iOS / state / compatibility uncertainty → prototype
- stateful learning → teach
- explanation did not land → wait-what
- GitHub/GitLab issue or external PR/MR intake → triage
- PR/MR reviewer summary → pr
- human-only provisioning / credentials / dashboard → wizard
- knowledge only another person has → to-questionnaire

GitHub、GitLab、local files 可以依專案分別設定；不同 repository 的 tracker / credentials / workflow 不混用。

## Skill sources

Local skills 位於 skills/。

Upstream skills 位於：

~~~text
upstream/mattpocock-skills/
~~~

實際曝光哪些 upstream skills 由 skills-manifest.json 控制。Matt repo 裡其他 experimental、writing、course 或 platform-specific skills 不會因 submodule 存在就自動安裝。

Installer 會把 local + manifest-selected upstream skills 合併成一個 catalog；名稱衝突會直接失敗，不做隱式 override。

## Command-line interface

日常操作只需要記 root-level `./agent-skills`：

~~~text
./agent-skills install [install.py options]
./agent-skills update
./agent-skills upstream [--update]
./agent-skills verify
./agent-skills test
./agent-skills help
~~~

Shell 只負責 human-facing orchestration；symlink safety、manifest validation、rollback 與 reconciliation 仍由 Python engine 負責。

## New device installation

需要 Git、Python 3.10+，以及可讀取本 private repository 的 GitHub SSH 設定。

~~~sh
git clone --recurse-submodules git@github.com:iceboxi/agent-skills.git ~/Documents/agent-skills
cd ~/Documents/agent-skills
./agent-skills install
~~~

若 clone 時沒有帶 `--recurse-submodules`，`install` 會自行初始化目前 parent repo pin 指定的 upstream revision。

Installer 使用 symlink，不複製 skill files。安裝入口：

~~~text
~/.agents/skills/<name>
~/.codex/skills/<name>
~/.claude/skills/<name>
~/.cursor/skills/<name>
~/.codex/AGENTS.md
~/.claude/CLAUDE.md
~~~

從舊版（所有 skill 都在 local `skills/`）升級時，installer 會辨識仍指向本 repo 的 managed symlink，並把同名 skill retarget 到 pinned upstream source；不需要手動刪舊 link。

## Normal repository update

取得這個 repository 已確認的 workflow 與 Matt pin：

~~~sh
cd ~/Documents/agent-skills
./agent-skills update
~~~

`update` 會依序：

1. 拒絕在 tracked working tree 有未提交修改時 pull。
2. `git pull --ff-only`。
3. checkout parent repo pin 指定的 submodule revision。
4. 跑 unit tests。
5. install / reconcile。
6. verify symlinks。

它**不會**把 Matt upstream 偷偷更新到 latest。

## Updating Matt upstream

先檢查是否有新版：

~~~sh
./agent-skills upstream
~~~

要評估 latest upstream：

~~~sh
./agent-skills upstream --update
~~~

這會：

1. fetch Matt `origin/main`；
2. 將 submodule working checkout 移到 latest；
3. validate manifest-selected skills；
4. 跑 tests；
5. 跑 installer dry-run；
6. 停下來讓你 review。

接著人工檢查：

~~~sh
git diff --submodule=log
~~~

確認接受後才更新 parent repo pin：

~~~sh
git add upstream/mattpocock-skills skills-manifest.json
git commit -m "Update Matt skills upstream"
git push
./agent-skills install
~~~

Parent repo 的 submodule gitlink commit 是唯一 upstream pin；`skills-manifest.json` 不重複保存 SHA。

若 Matt 移動或刪除 manifest-selected skill，validation 會失敗；先更新 manifest 或決定是否保留 local adaptation，再提交新的 pin。

若升級後行為不如預期：

1. 先判斷是單次執行問題還是 recurring workflow problem。
2. recurring 問題用 upstream `retro`。
3. 若 upstream 行為真的不符合我們，優先新增小型 overlay / custom skill；只有必要時才 fork。
4. 回退只需把 parent repo 的 submodule pin 回先前 commit。

## Adding or removing upstream skills

不要複製 upstream skill。編輯 `skills-manifest.json` 的 `upstream.skills`，然後：

~~~sh
./agent-skills install --dry-run
./agent-skills install
~~~

移除的 managed skill symlink 會 reconcile；新增的會建立。

## Validation

日常：

~~~sh
./agent-skills test
./agent-skills verify
~~~

想看安裝計畫但不寫入：

~~~sh
./agent-skills install --dry-run
~~~

底層 Python 指令仍可用於 installer 開發 / troubleshooting：

~~~sh
python3 -m unittest discover -s tests -v
python3 install.py --dry-run
python3 install.py --verify
python3 update_upstream.py
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

Installer 會驗證 local metadata。Upstream skill 使用 Matt 自己的 SKILL.md invocation metadata，不要求我們額外包一份 agents/openai.yaml。

Local Markdown references 必須留在 local skills tree 內；upstream references 必須留在 upstream submodule tree 內。跨 layer 依賴以 skill name / workflow composition 表達，不使用相對 Markdown link 穿越 submodule boundary。

## Project bootstrap and trackers

Matt 的 setup-matt-pocock-skills 也會被安裝。它目前支援 GitHub、GitLab、local files 或其他 tracker convention。

在實際 project 第一次採用 upstream engineering workflow 時，可用它設定該 repository 的 tracker / triage labels / domain-doc layout；這些是 project-local configuration，不寫回本 agent-skills repo。

例如：

- NovelReader：可以使用 GitHub issue / PR workflow。
- MobileApp：可以使用 GitLab 或 local-file workflow。

兩個 project 的設定彼此獨立。

## Ownership summary

~~~text
Upstream generic engineering discipline
    → mattpocock/skills submodule

Our architecture/process differentiation
    → local skills/

Which upstream skills are active
    → skills-manifest.json

Which upstream revision is trusted
    → Git submodule gitlink

Cross-project persistent rules
    → instructions/common.md

Project-specific build/ownership/tracker rules
    → each project's AGENTS.md / repository docs
~~~
