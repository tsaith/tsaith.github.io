# Tsunghua Blog

這是一個使用 [Hugo](https://gohugo.io/) 與 Blowfish 主題建立的個人部落格，部署到 GitHub Pages：`https://tsaith.github.io/`。

## 專案結構

```text
.
├── .github/workflows/hugo.yml      # GitHub Pages 自動部署
├── archetypes/default.md           # hugo new 的文章樣板
├── assets/img/headshot.png         # 作者頭像
├── config/_default/
│   ├── hugo.toml                   # Hugo/主題/輸出設定
│   ├── languages.en.toml           # 語系、站名、作者資訊
│   ├── markup.toml                 # Markdown、KaTeX、語法高亮設定
│   ├── menus.en.toml               # Header/footer 選單
│   ├── module.toml                 # Hugo module 設定，目前為空
│   └── params.toml                 # Blowfish 外觀與功能參數
├── content/posts/                  # 部落格文章
├── hugo.toml                       # 根目錄站台基本設定
└── themes/blowfish                 # Blowfish Git submodule
```

## 環境需求

- Hugo Extended。此專案已在 `hugo v0.162.1+extended` 下檢查過；目前主題 submodule 宣告支援到 `0.161.1`，新版 Hugo 可能會顯示相容性警告。
- Git submodule。初次 clone 後需要抓取 Blowfish 主題：

```bash
git submodule update --init --recursive
```

## 本機開發

啟動預覽伺服器：

```bash
hugo server -D
```

開啟：

```text
http://localhost:1313/
```

檢查 Hugo 最終合併後的設定：

```bash
hugo config
```

產生 production build：

```bash
hugo --gc --minify
```

輸出會產生在 `public/`，此資料夾已被 `.gitignore` 排除。

## 新增文章

建立新文章：

```bash
hugo new posts/my-post.md
```

文章會建立在 `content/posts/my-post.md`。確認 front matter 的 `draft` 狀態；`draft = true` 時只有 `hugo server -D` 會顯示，正式 build 不會發布。

## 修改網站左上角 header 的文字

目前 header 左上角顯示 `Blowfish`，來源是：

```toml
# config/_default/languages.en.toml
title = "Blowfish"
```

要改成 `AI Mind`，把它改成：

```toml
title = "AI Mind"
```

修改後建議執行：

```bash
hugo config | rg 'title|languages'
hugo server -D
```

如果想讓根目錄基本設定也保持一致，也可以同步把 `hugo.toml` 的：

```toml
title = 'Tsunghua Blog'
```

改成：

```toml
title = 'AI Mind'
```

但目前實際覆蓋 header 文字的是 `config/_default/languages.en.toml` 裡的 `title`。

## 部署

`.github/workflows/hugo.yml` 會在 push 到 `main` 時執行：

1. checkout repository 與 submodule
2. 安裝 Go、Node.js 與 Hugo Extended
3. 執行 `hugo --gc --minify`
4. 上傳 `public/`
5. 部署到 GitHub Pages

## 常見設定

- 作者資訊與首頁 profile：`config/_default/languages.en.toml` 的 `[params.author]`
- 主題色、首頁版型、文章顯示選項：`config/_default/params.toml`
- Header 選單：`config/_default/menus.en.toml`
- KaTeX/LaTeX 支援：`config/_default/markup.toml` 搭配文章中的 `{{< katex >}}`
