Title: 在整合測試中執行 Javascript
Date: 2015-01-30
Tags: rails, testing
Category: Web


這篇文章將介紹如何使用 [Capybara](https://github.com/jnicklas/capybara)
來測試內含 `javascript` 的頁面。

### 安裝套件

在 Gemfile 加入
```ruby
  gem 'capybara'
  gem 'selenium-webdriver'
  gem 'capybara-webkit'
```
然後執行 `bundle install` 安裝套件。

### 設定 port

請在 `spec_helper.rb`裡面設定 Capybara 所使用的 port

spec/spec_helper.rb:

    :::ruby
    Capybara.server_port = 52662 # this line is required by Selenium

### 使用說明

撰寫[整合測試](blog/2014/12/07/feature-testing-with-rspec)時，
只要加入 `js: true`，
Capybara 就會自動使用預設的 Selenium 開啓 [Firefox](https://www.mozilla.org/en-US/firefox/new/) 進行測試，
如下面的範例

spec/features/user_registers_spec.rb:

    :::ruby
    require 'spec_helper.rb'

    feature "User registers", { js: true, vcr: true } do # 請加入 js: true

      background do
        page.driver.allow_url("js.stripe.com")
        page.driver.allow_url("api.stripe.com")
        page.driver.allow_url("www.gravatar.com")
        visit sign_up_path
      end
      after { clear_email }

      scenario "with valid user info and valid card" do
        fill_in_valid_user_info
        fill_in_valid_card
        click_button "Sign Up"
        expect_to_see_welcome_message
      end
      scenario "with valid user info and invalid card" do
        fill_in_valid_user_info
        fill_in_invalid_card
        click_button "Sign Up"
        expect_to_see_invalid_card_message
      end

      def fill_in_valid_user_info
        fill_in "Email Address", with: "cloud@example.com"
        fill_in "Password", with: "password"
        fill_in "Full Name", with: "Cloud Strife"
      end

      def fill_in_valid_card
        fill_in "Credit Card Number", with: "4242424242424242"
        fill_in "Security Code", with: "123"
        select "4 - April", from: "date_month"
        select "2018", from: "date_year"
      end

      def fill_in_invalid_card
        fill_in "Credit Card Number", with: "4242424242424242"
        fill_in "Security Code", with: ""
        select "4 - April", from: "date_month"
        select "2018", from: "date_year"
      end

      def expect_to_see_welcome_message
        expect(page).to have_content "Welcome, Cloud Strife"
      end

      def expect_to_see_invalid_card_message
        expect(page).to have_content "Your card's security code is invalid."
      end

    end

使用 Selenium 的優點是可以看到瀏覽器執行測試的過程，
方便偵錯，
而缺點是比較花時間。
倘若希望加快測試速度，
則可以在 `spec_helper.rb`裡面將預設改成 `:webkit`，如下

```ruby
Capybara.javascript_driver = :webkit
```

此外，我們可以使用 `:driver` 以指定某個測試希望使用的驅動引擎

```ruby
describe 'some stuff which requires js', :js => true do
  it 'will use the default js driver'
  it 'will switch to one specific driver', :driver => :selenium
end
```

