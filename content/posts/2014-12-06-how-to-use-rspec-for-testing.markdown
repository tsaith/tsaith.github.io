Title: 使用 RSpec 做自動測試
Date: 2014-12-06
Tags: rails, testing
Category: Web


[RSpec](https://github.com/rspec/rspec) 是一套專為 Ruby
設計的 BDD (Behavior Deriven Development) 測試框架，
基於它所撰寫出的測試程式有著相當高的可讀性，
感覺就像是在閱讀產品的規格書。

### 安裝套件

在專案的 Gemfile 中加入 rspec-rails 的 gem，如下
```plain
group :development, :test do
  gem 'rspec-rails', '2.99'
end
```

除了 RSpec 之外， 因為 [shoulda-matchers](https://github.com/thoughtbot/shoulda-matchers)，
額外提供了許多有用的測試函式，建議一併安裝。

```plain
group :test do
  gem 'shoulda-matchers', '2.7.0', require: false
end
```

編輯完 Gemfile 後，請執行 `bundle` 進行套件安裝。


最後，再執行
```plain
rails g rspec:install
```
以產生 RSpec 運作所需的相關檔案。

### 設定 spec_helper.rb

在 spec/spec_helper.rb 檔案的開頭加入以下內容

```ruby
ENV["RAILS_ENV"] ||= 'test'
require File.expand_path("../../config/environment", __FILE__)
require 'rspec/rails'
```

### 撰寫測試

假設我們在 app/models/video.rb 有個 Video model， 如下
```ruby
class Video < ActiveRecord::Base
  belongs_to :category

  validates_presence_of :title, :description
end
```

這個 Video model 屬於 Category
並且要求在產生物件時需要檢驗 title 和 description 已經存在，
那麼對應的測試檔案 spec/models/video_spec.rb 的內容可以寫成

```ruby
require 'spec_helper'
require 'shoulda/matchers'

describe Video do

  it { should belong_to :category }
  it { should validate_presence_of :title }
  it { should validate_presence_of :description }

end
```

寫好測試程式後，請在專案目錄下執行
```plain
rspec spec/models/video_spec.rb
```
就能看到測試結果。

倘若要一次跑多個測試，請直接執行 `rspec` ，
就會跑放在 spec/ 下面的所有測試程式。
