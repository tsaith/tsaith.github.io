Title: 實作簡易的搜尋功能
Date: 2014-12-02
Tags: rails
Category: Web


在電子商務中，商品的搜尋是很重要的一環，
這裡將介紹如何實作簡易的搜尋功能。

倘若我們現在希望開發一個搜尋影片的功能;
假設影片的類別名稱是 Video，
首先在 config/routes.rb 裡面加入 search 的路徑

```ruby
  resources :videos, only: [:show] do
    collection do
      get 'search', to: 'videos#search'
    end
  end
```

接著在 app/controllers/videos_controller.rb 裡面加入
search action

```ruby
  def search
    @videos = Video.search_by_title(params['search_term'])
  end
```

然後在 app/models/video.rb 裡面新增 search_by_title 方法

```ruby
  def self.search_by_title(str)
    return [] if str.blank?
    where("title LIKE ?" , "%#{str}%").order("created_at DESC")
  end
```

這裡使用 [Haml](http://haml.info/) 來撰寫 views;
若想為網站的 header 加入搜尋欄位，
請在 app/views/shared/_header.html.haml 裡面加入

```haml
  = form_tag search_videos_path, method: 'get', class: 'col-md-5 navbar-form'  do
    = text_field_tag :search_term, params['search_term'] ||= '', class: 'form-control', placeholder: "Search for videos here"
    = submit_tag 'Search', class: 'btn btn-default'
```

最後，新增搜尋頁面 app/views/videos/search.html.haml


```haml
- @videos.each do |video|
  .video.ul
    .li
      #{video.title}
    .li
      = image_tag(video.cover_image_url, size: cover_image_size)
```
