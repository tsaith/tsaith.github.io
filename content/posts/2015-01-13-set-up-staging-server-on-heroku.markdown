Title: 在 Heroku 上架設 staging server
Date: 2015-01-13
Tags: rails, heroku
Category: web

開發專案時，
有時候我們會遇到在本地端測試過的功能無法在上線時正常運作，
這往往是因為開發環境(通常是我們的個人電腦)，
與上線的環境並不相同;
為了解決這問題，
我們將程式更新到 production 之前，
需要先在 staging server 上測試過。
簡單地說，staging 所扮演的角色就是在模擬 production;
所以，我們應該盡可能地讓 staging 環境與 production 所在的環境一致。
這裡將介紹如何在 Heroku 平台上架設 staging server。


假設，我們在 Heroku 上有一個 production 名字叫 `myflix`，
而希望的 staging 名稱為 `myflix-staging`;
那麼只要執行
```
$ heroku fork -a myflix myflix-staging
```
Heroku 就會 fork 出 `myflix-staging`，並且自動複製 `myflix` 的資料庫與 add-ons，讓 staging 與 production 有相同的運作環境。

此外，我們還需要在 git 中設定 `myflix-staging` 的 repository，之後才能將程式也 push 到 staging 中。
```
$ git remote add myflix-staging git@heroku.com:myflix-staging.git
```
