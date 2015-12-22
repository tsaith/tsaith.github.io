Title: 整合測試的郵件工具: capybara-email
Date: 2015-01-05
Tags: rails, testing
Category: Web


撰寫整合測試時，倘若需要模擬點選郵件內容的連結，
進而訪問某個網頁時，
可以使用 [capybara-email](https://github.com/dockyard/capybara-email) 這個 gem。

### 安裝套件

在 Gemfile 裡面加入
```ruby
gem 'capybara-email'
```
然後執行 `bundle` 進行安裝。

### 設定郵件主機

在 config/environmnets/test.rb 加入本地端的 host，如下
```ruby
  config.action_mailer.default_url_options = { :host => 'localhost:3000' }
```

### 設定套件路徑

在 spec/spec_helper.rb 裡面加入
```ruby
require 'capybara/email/rspec'
```

### 撰寫測試

下面的範例是用來測試使用者重設密碼的流程，
當使用者點選了郵件的連結後，將會被導向重設密碼的網頁

spec/features/user_resets_password_spec.rb:

    :::ruby
    require 'spec_helper.rb'

    feature "User resets password" do

      scenario "user sucessfully resets the password" do

        # 在資料庫先產生一個使用者 alice
        alice = Fabricate(:user, password: "old_password")

        # 訪問登入頁面，並點選 Forgot Password? 連結
        # (然後會被導向填寫郵件地址的頁面)
        visit sign_in_path
        click_link "Forgot Password?"

        # 填寫郵件地址並送出
        # (這時候網站將自動寄信給使用者，內含變更密碼的網頁連結)
        fill_in "Email Address", with: alice.email
        click_button "Send Email"

        # 開啓寄給使用者的郵件，並點選信件內容中的連結
        # (然後使用者會被導向設定新密碼的網頁)
        open_email(alice.email)
        current_email.click_link "Reset My Password"

        # 填寫新密碼，並送出
        # (然後會自動回到登入頁面)
        fill_in "New Password", with: "new_password"
        click_button "Reset Password"

        # 在登入頁面中，填寫使用者郵件地址和新密碼，然後送出
        fill_in "Email Address", with: alice.email
        fill_in "Password", with: "new_password"
        click_button "Sign in"

        # 預期在更新後的網頁看到歡迎使用者的訊息
        expect(page).to have_content "Welcome, #{alice.full_name}"
      end

    end
    {% endcodeblock %}

    {% blockquote Bill Gates %}
    Measuring programming progress by lines of code is like measuring aircraft building progress by weight.
