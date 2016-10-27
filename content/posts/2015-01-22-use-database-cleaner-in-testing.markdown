Title: 在測試中使用 Database Cleaner
Date: 2015-01-22
Tags: rails, testing
Category: Web


通常，我們在執行自動測試時，
會希望資料庫裡面沒有之前剩餘的記錄，
不然很容易導致難以發現的錯誤。
這裡將介紹如何使用 [Database Cleaner](https://github.com/DatabaseCleaner/database_cleaner/)，
讓每次測試前可以自動完成資料庫的清理。

### 安裝套件

在 Gemfile 裡面加入
```ruby
gem 'database_cleaner'
```
然後執行 `bundle install`。

### 進行設定

若是用 [RSpec](http://rspec.info/) 編寫測試，
請先將 `spec_helper.rb` 裡面的這一行
```ruby
  config.use_transactional_fixtures = true
```
修改成
```ruby
  config.use_transactional_fixtures = false
```

然後在 `spec/support/` 裡面新增 `database_cleaner.rb`，
內容如下

spec/support/database_cleaner.rb:

    :::ruby
    RSpec.configure do |config|

      config.before(:suite) do
        DatabaseCleaner.clean_with(:truncation)
      end

      config.before(:each) do
        DatabaseCleaner.strategy = :transaction
      end

      config.before(:each, :js => true) do
        DatabaseCleaner.strategy = :truncation
      end

      config.before(:each) do
        DatabaseCleaner.start
      end

      config.after(:each) do
        DatabaseCleaner.clean
      end

    end
    {% endcodeblock%}

若不清楚上述設定的意義，
可以參考 Avdi Grimm 的[原文](http://devblog.avdi.org/2012/08/31/configuring-database_cleaner-with-rails-rspec-capybara-and-selenium/)，其中有詳細的說明。
