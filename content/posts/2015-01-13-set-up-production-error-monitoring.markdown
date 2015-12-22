Title: 監視產品錯誤: Sentry
Date: 2015-01-13
Tags: rails
Category: Web


當產品在線上工作時，如果發生意外的錯誤，
為了保持好的使用者體驗，
我們必須盡可能地在第一時間發現問題並迅速解決;
這裡要介紹一項好用的服務 [Sentry](https://getsentry.com)，
它可以為我們監控產品的運作狀況，
當錯誤發生時自動寄信通知我們並且記錄 log 中的錯誤訊息。

### 申請帳號

Sentry 有提供 [Trial plan](https://www.getsentry.com/register/) 只要註冊就可以免費使用;
註冊後，請先新增 `Team` 然後再新增 `Project`，
在 `Project` 的設定裡面可以取得 `API Key`。

### 安裝套件

在 Gemfile 加入 Sentry 的 Ruby 客戶端套件，
[raven-ruby](https://github.com/getsentry/raven-ruby)

    :::ruby
    group :production, :staging do
      gem "sentry-raven"
    end

然後執行 `bundle install`。

接下來，請為 `production` 和 `staging` 環境，
設定 `SENTRY_DSN` 環境變數，如下
```
# 請填入專案的 API Key
export SENTRY_DSN=http://public:secret@example.com/project-id
```
設定完成並且部署到遠端後，
以後只要產品的運作出現錯誤，
Sentry 就會自動將錯誤訊息寄送到我們的信箱。

