Title: 使用 Decorator 作為物件的表達層
Date: 2015-02-01
Tags: rails, design pattern
Category: Web


這篇文章將介紹如何使用 [Decorator Pattern](http://en.wikipedia.org/wiki/Decorator_pattern) 的技巧來封裝物件的表達邏輯。

假設有個頁面的部分程式碼如下

```ruby
%header
  %h3 #{@video.title}
  %span Rating:
  - if @video.rating
    = "#{@video.rating}/5.0"
  - else
    N/A
%p #{@video.description}
```

若想將上面的程式碼簡化成

```ruby
%header
  %h3 #{@video.title}
  %span Rating:
  = @video.rating
%p #{@video.description}
```

一種做法是將顯示 video rating 相關的邏輯放到 Video model 裡面，
但這卻會造成物件的表達邏輯與基本方法混合在一起;
這時候比較好的做法是使用 decorator 來封裝物件的表達邏輯。
下面我們將示範如何透過 [Draper gem](https://github.com/drapergem/draper) 來編寫 decorator。

### 安裝套件

在 Gemfile 加入
```ruby
gem 'draper'
```
然後執行 `bundle install`。

### 使用範例

請在 `app/decorators/` 下面新增檔案 `video_decorator.rb` 並加入內容如下

app/decorators/video_decorator.rb:

    :::ruby
    class VideoDecorator < Draper::Decorator
      delegate_all # 引入 Video model 的所有方法

      def rating
        object.rating.present? ? "#{object.rating}/5.0" : "N/A"
      end

    end

在 VideoController 裡面，使用 `decorate` 來設定 `@video`

app/controllers/videos_controller.rb:

    :::ruby
    class VideosController < ApplicationController

      ... 省略程式碼 ...

      def show
        @video = Video.find_by(slug: params[:id]).decorate
        #@video = Video.find_by(slug: params[:id])
      end

    end

之後就可以在 view 裡面使用 `@video.rating`

```ruby
%header
  %h3 #{@video.title}
  %span Rating:
  = @video.rating
%p #{@video.description}
```
