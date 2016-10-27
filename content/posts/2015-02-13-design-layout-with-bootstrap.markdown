Title: 在 Rails 中安裝與設定 Bootstrap
Date: 2015-02-13
Tags: rails
Category: Web


[Bootstrap](http://getbootstrap.com/) 是目前相當受歡迎的前端開發框架，提供了許多現成的元件，幫助人們可以快速設計網站頁面，
此外還提供 Responsive Web Design 的功能，
讓網頁可以自動在不同尺寸的裝置上縮放;
以下將介紹如何在 Rails 中進行 Bootstrap 的安裝與設定。

### 安裝套件

在 Gemfile 中加入

```ruby
gem 'bootstrap-sass'
gem 'autoprefixer-rails'
gem 'sass-rails'
gem 'sprockets-rails', :require => 'sprockets/railtie'
```

然後執行 `bundle install` 安裝套件。

### 載入 Bootstrap 函式庫

進入 app/assets/stylesheets/，
將原有的 `application.css` 移除，
然後新增檔案 `application.css.sass` 並加入以下的內容

app/assets/stylesheets/application.css.sass:

    :::sass
    @import "bootstrap-sprockets"
    @import "bootstrap"

請注意 `bootstrap-sprockets` 的載入順序必須在 `bootstrap` 之前。

編輯 `app/assets/javascripts/application.js`，
在檔案中加入 `//= require bootstrap-sprockets` 如下

app/assets/javascripts/application.js:

    :::js
    // This is a manifest file that'll be compiled into application.js, which will include all the files
    // listed below.
    //
    // Any JavaScript/Coffee file within this directory, lib/assets/javascripts, vendor/assets/javascripts,
    // or vendor/assets/javascripts of plugins, if any, can be referenced here using a relative path.
    //
    // It's not advisable to add code directly here, but if you do, it'll appear at the bottom of the
    // compiled file.
    //
    // Read Sprockets README (https://github.com/sstephenson/sprockets#sprockets-directives) for details
    // about supported directives.
    //
    //= require jquery
    //= require jquery_ujs
    //= require turbolinks
    //= require bootstrap-sprockets
    //= require_tree .

最後，請確定在 `app/views/layouts/application.html.haml`
裡面有個別載入 Stylesheet 和 Javascript

app/views/layouts/application.html.haml:

    :::haml
    !!! 5
    %html(lang="en-US")
      %head
        %title Bed & Breakfast
        %meta(charset="UTF-8")
        %meta(name="viewport" content="width=device-width, initial-scale=1.0")
        = csrf_meta_tag
        -# 載入 Stylesheet
        = stylesheet_link_tag "application", :media => "all", 'data-turbolinks-track' => true
        -# 載入 Javascript
        = javascript_include_tag "application", 'data-turbolinks-track' => true
      %body
        %header
          = render 'shared/header'
        %section.content.clearfix
          = render 'shared/messages'
          = yield
        %footer
          &copy 2015 Bed & Breakfast

完成以上的設定後，我們就可以開始使用 `Bootstrap` 的各種功能來進行網頁的設計。
