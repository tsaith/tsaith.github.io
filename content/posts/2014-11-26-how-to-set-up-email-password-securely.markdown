Title: 安全地設定 Rails 郵件密碼
Date: 2014-11-26
Tags: rails
Category: Web


將密碼寫進程式通常不是個好主意，因為當我們使用版本控制系統(例如 git)
儲存程式時，密碼也將會被一併存入，如果是開源的專案，
那麼任意人都可以取得這資訊;為避免此問題，
我們可以使用環境變數讓 Rails 較安全地存取密碼資訊。

### 設定郵件密碼

這裡以 config/environments/ 下的 production.rb 為例子，
在 password 這裡，我們可以使用 ENV 來讀取系統的環境變數。

```ruby
  # Delivery method of mailer
  config.action_mailer.delivery_method = :smtp

  # Settings of the mailer
  config.action_mailer.smtp_settings = {
    address: "smtp.gmail.com",
    port: 587,
    domain: "gmail.com",
    authentication: "plain",
    user_name: thtsai.demo@gmail.com,
    password: ENV['SMTP_PASSWORD'],
    enable_starttls_auto: true
  }
```

### 設定環境變數

若開發環境是 Mac，可在 ~/.profile 裡面加入
```plain
export SMTP_PASSWORD='My password'
```

當專案上傳到遠端主機後，記得將密碼寫到遠端的環境變數;
下面以 Heroku 為例

```plain
heroku config:add SMTP_PASSWORD='My password'
```

這樣一來，Rails 就能通過環境變數來取得密碼資訊。
