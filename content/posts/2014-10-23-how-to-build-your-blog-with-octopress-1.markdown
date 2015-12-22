Title: 使用 Octopress 建構部落格
Date: 2014-10-23
Tags: octopress
Category: Web

[Octopress](http://octopress.org/) 是一套優良的部落格框架，
使用者可依照個人需求，設計專屬版面和擴充新功能，關於使用它的種種好處，
可參考神人xdite的[文章](http://blog.xdite.net/posts/2011/10/07/what-is-octopress/)。


### 安裝 Octopress

打開終端機，將 Octopress 的 [repository](https://github.com/imathis/octopress) 複製一份到本地端，並指定希望的資料夾名稱。
```
git clone git://github.com/imathis/octopress.git directory_name
```

進入資料夾，安裝相關套件;
```
bundle install
```

然後，安裝預設主題，
```
rake install
```
現在，我們已經完成所有的安裝步驟。

### 將檔案部署到 GitHup

首先在 GitHup 建立新的 repository，並命名為 [帳號].github.io; 例如，我的帳號是 tsaith，所以對應的名字就是 [tsaith.github.io](https://github.com/tsaith/tsaith.github.io) 。

然後使用終端機，在對應的部落格資料夾下執行
```
rake setup_github_pages
```
`setup_github_pages` 將會請你輸入 GitHup repository 的 URL 來設定 GitHup pages。

執行下面指令來產生部落格檔案，
```
rake generate
```

接著 deploy 檔案到 GitHup pages，
```
rake deploy
```

最後，將 source 也 push 到 GitHub repository。
``` 
git add .
git commit -m "你的訊息"
git push origin source
```
如果一切順利，你現在已經有了自己的部落格，而對應網址是 [使用者帳號].github.io。

### 新增文章

我們可以使用 `new_post` 來新增文章，這指令將會在 source/_posts/ 下面產生對應的檔案。

```
rake new_post["article title"]
```
就會在 source/_posts/ 下面新增文章的草稿。

若打開每篇文章的內容會看到最上方會有一些設定資訊如下

```
---
layout: post
title: "在 Mac 上安裝 Rails"
date: 2014-10-22 12:04:25 +0800
comments: true
categories: Rails
---
```

我們將內容編寫於設定資訊的下方，而撰寫格式則是採用 [Markdown](http://markdown.tw/) 語法。

當撰寫文章時，我們可以新開一個終端機視窗並在專案資料夾下執行 `rake preview`，然後開啟瀏覽器連到 http://localhost:4000 進行預覽。
```
rake preview
```

當編輯完新文章後，執行 `rake generate` 產生部落格檔案，然後再將它們 deploy 到 GitHup pages;
```
rake generate
rake deploy
```
最後，別忘了 push 對應的 source 到你的 GitHup repository!

### 連結內部文章

編輯文章時，常常會需要連結到之前的文章作為參考，
假設欲連結的文章檔名是 2014-10-22-install-rails-on-mac.markdown，那麼可以使用下列的語法

```plain
[名稱]({% post_url 2014-10-22-install-rails-on-mac %})
```

倘若上面的語法出現語法解析錯誤，則可以嘗試使用

```plain
[名稱]( /blog/2014/10/22/install-rails-on-mac )
```
