Title: 產生 SSH Key
Date: 2014-10-26
Tags: utils
Category: Web

在 web 開發中，許多平台 (例如 GitHup, Heroku, AWS ...等) 
都使用 SSH Key 來提供安全認證機制; 這裡將說明如何產生 SSH Key。

### 產生 SSH key

在終端機的命令列，我們可以利用 `ssh-keygen` 來產生 private key 和
對應的 public key ; 其預設檔名分別是 id_rsa 和 id_rsa.pub，
而預設的儲存路徑為使用者目錄下的 .ssh/ 資料夾。
執行過程中，會詢問是否要設定密碼? (為了安全性的考量，建議設定)
```
ssh-keygen -t rsa -C "your_email@example.com"
```

### 使用 ssh-agent

如果在產生 SSH key 的過程中，有設定密碼的話，
你會發現每次登入遠端都要重新輸入密碼，相當麻煩; 
不過，我們可以使用 `ssh-agent` 來解決這問題。
假設你的 private key 是 ~/.ssh/id_rsa，這時我們在命令列執行
```
ssh-add ~/.ssh/id_rsa
```
然後程式會詢問你的密碼，並儲存下來，之後每次登入就不再需要另外輸入密碼了。





