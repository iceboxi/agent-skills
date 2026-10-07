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

Our overlay
├─ ask-skills
├─ explore
├─ design
├─ review
├─ doc-sync
├─ spec-review
├─ report
├─ prototype      # iOS / integration spike adaptation
├─ tdd            # legacy characterization branch
└─ wayfinder      # no ticket/issue-tracker requirement
~~~

原則：沒有真正差異就直接使用 upstream；不要複製 upstream SKILL.md 再改幾行。需要組合上的差異，優先放在 ask-skills / workflow handoff，而不是 patch upstream body。

## Main engineering flow

~~~text
idea / change
    ↓
grill-with-docs                     (upstream)
    ↓
explore                             (ours, when repository grounding is needed)
    ↓
design                              (ours)
    ↓
review                              (ours)
 ┌──┴────────────────────────────────────────────────────┐
 │                                                       │
REVISE                                                 ACCEPT
 │                                                       │
 └──────────────→ design                                  ├─ small → implement
                                                         │            ↓
                                                         │        code-review
                                                         │
                                                         └─ durable contract
                                                                ↓
                                                             to-spec
                                                                ↓
                                                           spec-review
                                                                ├─ single-context → implement
                                                                └─ multi-context
                                                                       ↓
                                                                  to-tickets
                                                                       ├─ per item → implement
                                                                       └─ whole graph → implement-spec
                                                                                              ↓
                                                                                         code-review

after difficult or surprising work
    ↓
retro
~~~

Side paths:

- hard bug / flake / perf regression → diagnosing-bugs
- architecture health survey → improve-codebase-architecture
- huge route-invisible effort → our wayfinder
- external technical fact → research
- runnable iOS / state / compatibility uncertainty → our prototype
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

## New device installation

需要 Git、Python 3.10+，以及可讀取本 private repository 的 GitHub SSH 設定。

推薦直接 clone submodule：

~~~sh
git clone --recurse-submodules git@github.com:iceboxi/agent-skills.git ~/Documents/agent-skills
cd ~/Documents/agent-skills
python3 -m unittest discover -s tests -v
python3 install.py --dry-run
python3 install.py
~~~

若已經 clone 但 upstream 尚未初始化：

~~~sh
cd ~/Documents/agent-skills
git submodule update --init --recursive
python3 install.py --dry-run
python3 install.py
~~~

Installer 使用 symlink，不複製 skill files。安裝入口：

~~~text
~/.agents/skills/<name>
~/.codex/skills/<name>
~/.claude/skills/<name>
~/.cursor/skills/<name>
~/.codex/AGENTS.md
~/.claude/CLAUDE.md
~~~

從舊版（所有 skill 都在 local skills/）升級時，installer 會辨識仍指向本 repo 的 managed symlink，並將同名 skill 自動 retarget 到 pinned upstream source；不需要手動刪舊 link。

## Normal repository update

其他裝置取得本 repo 已確認的 upstream pin：

~~~sh
cd ~/Documents/agent-skills
git pull --ff-only
git submodule update --init --recursive
python3 -m unittest discover -s tests -v
python3 install.py --dry-run
python3 install.py
~~~

如果只是 upstream skill 內容更新、skill path/name 沒變，既有 symlink 會直接看到新 submodule 內容；再次跑 installer 仍建議用來驗證 manifest、retarget 與 stale links。

## Updating Matt upstream

Upstream 不會在 install 時自動追 latest。這是刻意的：engineering workflow 是 infrastructure，升級必須可 review、可回退。

先檢查：

~~~sh
cd ~/Documents/agent-skills
python3 update_upstream.py
~~~

有新版本時：

~~~sh
python3 update_upstream.py --update
git diff --submodule=log
python3 -m unittest discover -s tests -v
python3 install.py --dry-run
~~~

如果 Matt 移動或刪除 manifest-selected skill，validation 會失敗；先更新 skills-manifest.json 或決定是否保留 local adaptation，再繼續。

確認後正式更新 pin：

~~~sh
git add upstream/mattpocock-skills skills-manifest.json
git commit -m "Update Matt skills upstream"
git push
python3 install.py
~~~

Parent repo 的 submodule gitlink commit 是唯一 upstream pin。skills-manifest.json 不重複保存 SHA。

若升級後行為不如預期：

1. 先判斷是單次執行問題還是 recurring workflow problem。
2. recurring 問題使用 retro。
3. 若 upstream 行為本身不適合我們，優先新增小型 overlay / custom skill；只有必要時才 fork 該 skill。
4. 回退 upstream 只需把 submodule pin 回到先前 parent commit。

## Adding or removing upstream skills

不要複製檔案。編輯 skills-manifest.json 中 upstream.skills 的 relative path，然後：

~~~sh
python3 install.py --dry-run
python3 install.py
~~~

移除的 managed skill symlink 會被 reconcile；新增的會被建立。

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

## Validation

~~~sh
python3 -m unittest discover -s tests -v
python3 install.py --dry-run
python3 install.py --verify
~~~

--verify 只檢查目前 symlink 是否指向 manifest 選定的 local/upstream source，不建立或移轉內容。

## Adoption / conflicts

預設遇到一般檔案、一般目錄或非本 repo 管理的同名 symlink 就停止。

完全相同的既有 skill / global instruction 可明確採用：

~~~sh
python3 install.py --adopt-identical --dry-run
python3 install.py --adopt-identical
~~~

既有 global instructions 若完整文字已包含在 instructions/common.md：

~~~sh
python3 install.py --adopt-instructions --dry-run
python3 install.py --adopt-instructions
~~~

Installer 不提供 force overwrite。衝突要先人工比較，避免吃掉其他工具或 repository 的設定。

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
