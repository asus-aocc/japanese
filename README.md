# 毎日日本語 — 自動更新セットアップガイド

每天早上 8 點（日本時間）自動用 AI 更新日文學習內容，完全免費。

---

## 需要準備的東西

- [GitHub 帳號](https://github.com/signup)（免費）
- [Anthropic API Key](https://console.anthropic.com/settings/keys)（按用量付費，每天更新約 $0.01〜0.02 USD）

---

## 步驟一：建立 GitHub Repository

1. 登入 GitHub，點右上角 **+** → **New repository**
2. Repository name 填 `japanese-daily`（或任何名字）
3. 選 **Public**（GitHub Pages 免費版需要 Public）
4. 點 **Create repository**

---

## 步驟二：上傳檔案

把以下四個檔案上傳到 repository：

```
japanese-daily/
├── index.html          ← 網站主頁
├── generate.py         ← AI 生成腳本
├── content.json        ← 每日內容（先放一個空的 {} 即可）
└── .github/
    └── workflows/
        └── daily-update.yml  ← 自動排程設定
```

上傳方式（最簡單）：
1. 在 repository 頁面點 **Add file** → **Upload files**
2. 把 `index.html`、`generate.py`、`content.json` 拖進去，點 Commit
3. `.github/workflows/daily-update.yml` 需要手動建立：
   - 點 **Add file** → **Create new file**
   - 檔名輸入 `.github/workflows/daily-update.yml`
   - 把 `daily-update.yml` 的內容貼進去

---

## 步驟三：設定 API Key（Secret）

1. 在 repository 頁面點 **Settings**
2. 左側選單 **Secrets and variables** → **Actions**
3. 點 **New repository secret**
4. Name 填 `ANTHROPIC_API_KEY`
5. Secret 貼上你的 API Key（`sk-ant-api03-...`）
6. 點 **Add secret**

---

## 步驟四：開啟 GitHub Pages

1. 在 repository 頁面點 **Settings**
2. 左側選單 **Pages**
3. Source 選 **Deploy from a branch**
4. Branch 選 **main**，資料夾選 **/ (root)**
5. 點 **Save**
6. 等 1〜2 分鐘，頁面會顯示你的網址：
   `https://你的帳號名.github.io/japanese-daily`

---

## 步驟五：手動執行一次（初始內容）

1. 在 repository 頁面點 **Actions**
2. 左側選 **毎日コンテンツ更新**
3. 右側點 **Run workflow** → **Run workflow**
4. 等約 30〜60 秒執行完成
5. 重新整理你的網站，內容就會出現！

---

## 之後

- **每天早上 8:00（JST）** GitHub Actions 自動執行，更新 `content.json`，網站內容自動刷新
- 想手動更新隨時可以在 Actions 頁面點 **Run workflow**
- 想新增 Podcast 或修改網站樣式，直接編輯 `index.html`

---

## 常見問題

**Q: 免費嗎？**  
GitHub 免費帳號每月有 2,000 分鐘 Actions 額度，每次執行約 1〜2 分鐘，每天跑一次完全用不完。GitHub Pages 也免費。只有 Anthropic API 按量計費，每天約 $0.01 USD。

**Q: content.json 在哪裡？**  
每次 Actions 執行後，`generate.py` 會更新 `content.json` 並自動 commit 到 repository。

**Q: 想改成幾點更新？**  
修改 `daily-update.yml` 裡的 `cron: "0 23 * * *"`。  
格式是 UTC 時間，台灣 = UTC+8，所以早上 8 點 JST = UTC 23:00（前一天）。  
想改成早上 7 點：`cron: "0 22 * * *"`
