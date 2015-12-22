Title: 使用 letter_opener 檢視郵件
Date: 2014-12-31
Tags: rails
Category: Web


在建構 Rails 應用時，
開發者常常需要反覆修改以及檢查欲寄送的 Email 內容是否正確，
[letter_opener](https://github.com/ryanb/letter_opener) 可以讓這工作變得更有效率。

### 安裝套件

在 Gemfile 裡面加入

```ruby
group :development do
  gem 'letter_opener'
end
```
接著執行 `bundle`。

### 郵件設定


在 config/environments/development.rb 裡面加入

```ruby
  config.action_mailer.delivery_method = :letter_opener
```
在開發模式下，當信件被寄出時，其內容會直接顯示在瀏覽器裡面。


### 操作範例

開啓 rails console，寄送一封測試郵件。
```
$ rails c
Loading development environment (Rails 4.1.1)
2.1.5 :001 > AppMailer.send_welcome_email(User.last).deliver
```

這時候 letter_opener 就會自動將信件內容傳送到瀏覽器的新分頁，如下
{% img https://farm9.staticflickr.com/8563/15996168469_b9f26d2f26_b.jpg %}
