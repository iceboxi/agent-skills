# Agent Skills

個人使用的架構探索、規劃與設計文件 skills。核心內容與 CLI 無關，使用繁體中文說明，保留 code identifiers、API names 與 technical terminology。

| Skill | 用途 |
| --- | --- |
| `architecture` | 先查 code、建立 current model，再逐步澄清、比較方案、確認決策與規劃。包含 explore、plan、refactor 模式。 |
| `design-doc` | 將已有模型、evidence 與決策整理成可獨立 review 的 Markdown 文件。 |

`architecture` 按需載入 planning 與 refactoring 指引。規劃可以交付 Resolved、Draft / Pending Decisions 或 Blocked；refactor 先驗證 premise，PREMISE REJECTED 也是成功結果。只有明確要求文件，或接受保存建議時，才交接給 `design-doc`，沿用同一份模型與決策。Reasoning completion 與文件產出獨立；實作需要使用者另行要求。

```text
agent-skills/
  skills/
    architecture/
      SKILL.md
      references/
        planning.md
        refactoring.md
      agents/openai.yaml
    design-doc/
      SKILL.md
      agents/openai.yaml
  install.py
  tests/test_install.py
```

## 新電腦安裝

需要 Git、Python 3.10+，以及能讀取此 private repository 的 GitHub 帳號。Installer 使用 Python standard library。安裝方式使用 directory symlinks，適用 macOS 與 Linux。

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

Installer 依目前電腦的 home 與 clone 位置建立連結。不要從其他電腦複製舊的絕對路徑 symlinks。

```text
~/.agents/skills/   (Codex)
~/.codex/skills/    (Codex 相容路徑)
~/.claude/skills/   (Claude Code)
~/.cursor/skills/   (Cursor)
        |
        | directory symlinks
        v
<clone>/skills/{architecture,design-doc}
```

各入口都指向同一份內容。保留整個 repository，兩個 skills 的相對引用需要相鄰目錄。安裝後重新載入 CLI 的 skills，必要時開啟新的 session。

可由任務意圖自動選擇，也可明確指定。例如在 Codex 使用 `$architecture` 或 `$design-doc`；在 Claude Code 使用 `/architecture` 或 `/design-doc`。

Global／project `AGENTS.md`、`CLAUDE.md` 與專案 architecture 文件仍由各自環境管理。

## 更新與跨電腦同步

```sh
cd ~/Documents/agent-skills
git pull --ff-only
python3 install.py --dry-run
```

Skill 內容透過 symlinks 更新。新增 skill 時再執行 `python3 install.py`。重跑安裝會保留已正確指向此 repository 的連結。

在任何電腦修改 `skills/` 後，以一般 Git commit／push 同步；其他電腦再 pull。保留穩定的 clone 位置。若改用另一個 clone 位置，先保留原 clone，再以 `--adopt-identical` 移轉相同內容的既有連結。

## 移轉現有安裝

預設遇到同名的既有目錄或不同連結就停止，並在全部目的路徑檢查完成前不寫入。只有內容完全相同時，才可以明確移轉：

```sh
python3 install.py --adopt-identical --dry-run
python3 install.py --adopt-identical
```

移轉會比較全部檔案與目錄，先把原項目移到 `~/.local/share/agent-skills/backups/<timestamp>/`，再建立新連結。內容不同、dangling symlink 或內部另含 symlinks 的項目會停止移轉。Installer 不提供強制覆寫。

如果安裝過程發生錯誤，installer 會嘗試還原此次已修改的項目。成功移轉後保留備份；確認各 CLI 可以使用後，再自行整理。

## 驗證

```sh
python3 -m unittest discover -s tests -v
python3 install.py --dry-run
```

Tests 在 temporary directories 驗證首次安裝、重跑、來源更新、同名衝突、相同內容移轉、備份、安裝錯誤回復與相對引用。它們不會修改真實的 CLI 設定，也不代表 skills 的多輪模型行為已實測。
