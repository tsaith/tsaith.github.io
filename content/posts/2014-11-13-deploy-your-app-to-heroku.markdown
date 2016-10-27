Title: 部署專案到 Heroku
Date: 2014-11-13
Tags: rails
Category: Web


[Heroku](https://www.heroku.com) 是個相當受歡迎的雲端平台，
為開發者建構了網站運行所需要的環境，
原則上，使用者只要將自己的應用程式部署上去便可直接運行;
目前，它還提供了免費試用的方案，相當適合學生練習實作。
而使用方法簡介如下

* 先到 Keroku 官網進行[註冊](https://id.heroku.com/login)

* 註冊後，登入官網然後下載 Heroku toolbelt 並且安裝

* 打開終端機，執行 `heroku login` 來登入使用者資訊並上傳 public ssh key

* 在專案下，執行 `heroku create`
```
$ heroku create
Creating agile-sea-7701... done, stack is cedar-14
https://agile-sea-7701.herokuapp.com/ | git@heroku.com:agile-sea-7701.git
Git remote heroku added
$ git remote
heroku
origin
```

* 執行 `git push heroku master` 將專案部署到Heroku上，
部署結束後，會顯示專案對應的網路位址

* 執行 `heroku ps:scale web=1` 確認至少有一個 instance 在運行
```
$ heroku ps:scale web=1
Scaling dynos... done, now running web at 1:1X.
```
* 執行 `heroku run rake db:migrate` 在 Heroku 上進行 database migration

* 如果希望對 app 重新命名可以執行 `heroku apps:rename 新名稱`

* 如果一切順利，我們現在就可以執行 `heroku open` 讓瀏覽器訪問網站的首頁

Good Luck!


