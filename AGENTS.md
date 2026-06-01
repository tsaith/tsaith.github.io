# AGENTS.md

## 溝通

- 請用中文與我交談。
- 回覆要直接、務實，優先給可執行的指令、檔案路徑與原因。

## 專案概況

- 這是 Hugo 靜態網站專案，部署目標是 GitHub Pages：`https://tsaith.github.io/`。
- 目前使用 Blowfish 主題，主題以 Git submodule 放在 `themes/blowfish`。
- Hugo 設定主要在 `config/_default/`，根目錄 `hugo.toml` 只保留少量站台層級設定。
- 文章放在 `content/posts/`，圖片等 Hugo assets 放在 `assets/`。

## 開發規範

- 優先修改專案自己的設定與內容，不直接改 `themes/blowfish` 內的主題檔；若需要主題變更，先確認是否能透過 `config/_default/*.toml`、`layouts/` override 或 assets 解決。
- 新文章使用 `hugo new posts/<slug>.md` 建立，再編輯 front matter 與內容。
- 修改設定後使用 `hugo config` 檢查最終合併結果。
- 發布前使用 `hugo --gc --minify` 驗證 production build。
- 本機預覽使用 `hugo server -D`，預設網址是 `http://localhost:1313/`。

## 重要設定位置

- 主題與站台建置設定：`config/_default/hugo.toml`
- 語系、站名、作者與 header 文字：`config/_default/languages.en.toml`
- Blowfish 外觀與版面參數：`config/_default/params.toml`
- 導覽選單：`config/_default/menus.en.toml`
- Markdown、KaTeX passthrough 與語法高亮：`config/_default/markup.toml`
- GitHub Pages 部署流程：`.github/workflows/hugo.yml`

## 注意事項

- `config/_default/languages.en.toml` 的 `title` 目前會覆蓋根目錄 `hugo.toml` 的 `title`，也是 header 左上角文字來源。
- `config/_default/languages.en.toml` 內的 `params.logo = "img/logo.png"` 目前指向尚不存在的檔案；若未提供 logo，Blowfish 會以文字標題顯示站台識別。
- 目前 Blowfish submodule 的 `themes/blowfish/config.toml` 宣告 Hugo extended 支援範圍為 `0.158.0` 到 `0.161.1`；若使用更新版 Hugo 看到相容性警告，先確認 build 是否正常。
