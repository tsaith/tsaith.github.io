Title: 安裝和使用 Git
Date: 2014-10-26
Tags: utils
Category: Web


在軟體開發中過程中，版本控制無疑是相當重要的一環; 
而 [Git](http://git-scm.com/) 由於它的優良設計和開源已被廣泛地使用，
這裡將介紹如何在 Mac 上安裝 Git 和基本的使用方法。

### 套件安裝
在 Mac 上我們可以利用 [Homebrew](http://brew.sh/index_zh-tw.html) 來
安裝 Git 套件
```
  brew install git
```
安裝成功後，接下來設定使用者的姓名和郵件位址
```
git config --global user.name "Your Name"
git config --global user.email "user@gmail.com"
```
也許你會希望加入顏色支援
```
git config --global color.ui true
```

### 使用方法

進入你的專案目錄後，我們需要先初始化環境
```
git init
```
然後會產生 .git/ 資料夾，它儲存著版本控制的各種相關檔案。 

如果你有一個 GitHup repository ，並想將它作為遠端儲存
(假設你的帳號是 silver， repository 名稱是 repo); 那麼請執行
```
git remote add origin https://github.com/silver/repo.git
```

若想將專案目錄下的所有檔案加入版本控制系統，請執行
```
git add -A
```

倘若你只想加入單一檔案，可執行
```
git add [File Name]
```

若是想加入當前目錄下所有 .txt 結尾的檔案則執行
```
git add *.txt
```

若是想刪除當前目錄下的某一個檔案則執行
```
git rm [File Name]
```

若是想刪除當前目錄下所有 .txt 結尾的檔案則執行
```
git rm *.txt
```

在 新增/刪除/修改 檔案後，使用 `commit` 提交，-m 之後是提交訊息
```
git commit -m "Add test.txt"
```

倘若你使用的是遠端 repository， 那麼還需要將資料 `push` 出去
```
git push -u origin --all
```

若想查詢目前的控制系統的狀態，請執行
```
git status
```

如果想查詢歷史記錄，則使用 `log`
```
git log
```

若想查詢某一命令的說明可利用 `help`，例如
```
git help log
```

倘若有些檔案你不想加入版本控制系統，
可以在專案目錄下新增一個檔案 .gitignore 並將那些檔案記錄下來;
例如，假設你不想記錄那些 .tmp 和 .swp 結尾的檔案，
那麼 .gitignore 的內容為
```
*.tmp
*.swp
```

若想比較目前和上次 commit 版本的整體差異
```
git diff HEAD
```

若只想比較單一檔案在目前和上次 commit 的差別
```
git diff HEAD^ HEAD [Path / File]
```

若想回復到前一次的 commitment
```
git reset --hard Head^
```

以上是一些 Git 的基本用法，如果需要更多進階的操作，
請參考[官方文件](http://git-scm.com/doc)。

