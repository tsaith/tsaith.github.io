Title: 使用 Figaro 設定環境變數
Date: 2015-01-16
Tags: rails
Category: Web


開發專案時，
我們常常需要在不同的環境下(例如 development、test 或 production)為環境變數設定不同的值，
倘若每次都要手動設定，
不僅浪費時間而且很容易發生錯誤;
對於這個問題，
[Figaro](https://github.com/laserlemon/figaro)
提供了一個簡潔的方法來處理。

### 安裝套件

在 Gemfile 中加入
```ruby
gem 'figaro'
```
然後執行 `bundle install` 進行安裝。

### 設定環境變數

請在專案目錄下，執行 `figaro install`，這命令將

* 自動產生 `config/application.yml`
* 將此檔案加到 `.gitignore` 裡面

然後就可以在 `application.yml` 裡面針對不同環境來設定變數，
如下

config/application.yml:

    :::yaml
    development:
      SMTP_USER_NAME: test@example.com
      SMTP_PASSWORD: test_password

    test:
      SMTP_USER_NAME: test@example.com
      SMTP_PASSWORD: test_password

    staging:
      SMTP_USER_NAME: test@example.com
      SMTP_PASSWORD: test_password

    production:
      SMTP_USER_NAME: live@example.com
      SMTP_PASSWORD: live_password

設定後，請記得重新啟動伺服器以載入變數。

### 設定 Heroku 環境變數

Figaro 還提供了方便的指令可以一次將設定檔的環境變數輸出到 Heroku 上，如下

```
figaro heroku:set -e production
```
