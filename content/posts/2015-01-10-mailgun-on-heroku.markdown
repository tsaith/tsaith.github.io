Title: Heroku 上的郵件服務: Mailgun
Date: 2015-01-10
Tags: rails, heroku
Category: Web


信件服務對許多網路應用都是相當重要的一環，
雖然我們可以使用免費的 gmail 帳號來寄送郵件，
但因為 gmail 每天可寄送的郵件數量有一定的上限(目前是每天 2,000 封)以及其他[限制](https://support.google.com/a/answer/166852)，
所以在正式上線的環境，
我們還是會使用專業的郵件服務，例如 [Mailgun](http://www.mailgun.com/);
接下來將介紹如何在 Heroku 上使用 [Mailgun add-on](https://addons.heroku.com/mailgun)。

### 申請 Mailgun add-on

登入 Heroku 後填寫信用卡資料，
然後就可以申請免費的 [Mailgun starter plan](https://addons.heroku.com/mailgun)。

### 設定郵件環境

在 config/environments/production.rb 裡面加入

    :::ruby
    # Mailer
    config.action_mailer.default_url_options = { :host => 'yourapp.herokuapp.com' } # 修改為您的 host
    config.action_mailer.delivery_method = :smtp
    config.action_mailer.smtp_settings = {
      address: ENV['MAILGUN_SMTP_SERVER'],
      port: ENV['MAILGUN_SMTP_PORT'],
      user_name: ENV['MAILGUN_SMTP_LOGIN'],
      password: ENV['MAILGUN_SMTP_PASSWORD'],
      domain: 'yourapp.herokuapp.com', # 修改為您的 domain
      authentication: :plain,
    }

設定完後，將專案部署到 Heroku 上面即可開始工作。
