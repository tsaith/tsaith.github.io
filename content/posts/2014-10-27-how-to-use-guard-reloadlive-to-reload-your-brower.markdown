Title: 使用 Guard::LiveReload 自動刷新瀏覽器
Date: 2014-10-27
Tags: rails
Category: Web


在編寫網頁的過程中，如果每次修改程式後總是需要手動刷新網頁來檢查結果，
實在是件很麻煩又浪費時間的事; 為了解決這問題，於是有人開發了 LiveReload
這工具，每當程式存檔後，網頁就會自動刷新，於是工程師們可以早點收工回家打電動了(誤)。

### 套件安裝

假設你使用的是 [bundler](http://bundler.io/) 來管理套件，
首先將 [guard](https://github.com/guard/guard) 和
[guard-livereload](https://github.com/guard/guard-livereload)
加到 Gemfile 中
```
group :development do
  gem 'guard'
  gem 'guard-livereload'
end
```
接著執行 `bundle` 開始安裝套件
```
bundle
```

然後，初始化一個新的 Guardfile
```
bundle exec guard init
```
這個檔案記錄了哪些檔案會被監控，可依自己的需求再進行修改

    :::ruby
    # A sample Guardfile
    # More info at https://github.com/guard/guard#readme

    #guard 'livereload', port: '4000' do
    guard 'livereload' do
      watch(%r{app/views/.+\.(erb|haml|slim)$})
      watch(%r{app/helpers/.+\.rb})
      watch(%r{public/.+\.(css|js|html)})
      watch(%r{config/locales/.+\.yml})
      # Rails Assets Pipeline
      watch(%r{(app|vendor)(/assets/\w+/(.+\.(css|js|html|png|jpg))).*}) { |m| "/assets/#{m[3]}" }
    end

另外，瀏覽器也需要安裝對應套件，假設我們使用的是 Google Chrome，
那麼就需要安裝 [Chrome LiveReload Extension](https://chrome.google.com/webstore/detail/livereload/jnihajbhpnppcggbcgedagnkighmdlei/related)。

### 使用方法

在專案目錄下，執行
```
bundle exec guard
```
如果想看到額外的偵錯資訊，則執行
```
bundle exec guard --debug
```
最後，點選 Google Chrome 瀏覽器的工具列上的 LiveReload 的圖示，
然後 Chrome 將會與 Guard::LiveReload 作連結。
如果一切順利，現在你每次將程式存檔後，就會看到瀏覽器的頁面自動刷新。
