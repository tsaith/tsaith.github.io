Title: 在 Rails 中設定 routes
Date: 2014-10-29
Tags: rails
Category: Web


在 Rails 中，當伺服器接受到 http request 時將會根據路由中的設定，
來決定這個 request 將會送往 controller 的哪個 action 進行處理;
這裡將介紹如何設定路由的路徑表。

在 config/routes.rb 可使用 `root to:` 來設定當使用者存取網站根目錄時的伺服器將會將 request 導向哪裡;假設我們設定如下
```ruby
PostitTemplate::Application.routes.draw do
  root to: 'posts#index'
end
```
接著使用 `bundle exec rake routes` 來查詢路徑表
```
$ bundle exec rake routes
Prefix Verb URI Pattern Controller#Action
root   GET  /   posts#index
```
在上面的範例中，當 http verb 為 GET 而存取路徑是 / 時，伺服器會將 request
導向 posts controller 的 index action。

倘若我們有個物件模型 Post，這時可以使用 `resources` 簡潔地來設定對這類物件的一些常用存取路徑
```ruby
PostitTemplate::Application.routes.draw do
  resources :posts
end
```
這時候的路徑表為
```
$ bundle exec rake routes
   Prefix Verb   URI Pattern               Controller#Action
    posts GET    /posts(.:format)          posts#index
          POST   /posts(.:format)          posts#create
 new_post GET    /posts/new(.:format)      posts#new
edit_post GET    /posts/:id/edit(.:format) posts#edit
     post GET    /posts/:id(.:format)      posts#show
          PATCH  /posts/:id(.:format)      posts#update
          PUT    /posts/:id(.:format)      posts#update
          DELETE /posts/:id(.:format)      posts#destroy
```

如果我們只想使用其中幾個路徑，可以用 `only:` 來達成
```ruby
PostitTemplate::Application.routes.draw do
  resources :posts, only: [:new, :create]
end
```
上面只允許加入 `new` 和 `create` 兩個對應的路徑
```
$ bundle exec rake routes
  Prefix Verb URI Pattern          Controller#Action
   posts POST /posts(.:format)     posts#create
new_post GET  /posts/new(.:format) posts#new
```

如果要排除一些路徑，則使用 `except:`
```ruby
PostitTemplate::Application.routes.draw do
  resources :posts, except: [:new, :create]
end
```
這時將加入除了 `new` 和 `create` 之外的其他路徑
```
$ bundle exec rake routes
   Prefix Verb   URI Pattern               Controller#Action
    posts GET    /posts(.:format)          posts#index
edit_post GET    /posts/:id/edit(.:format) posts#edit
     post GET    /posts/:id(.:format)      posts#show
          PATCH  /posts/:id(.:format)      posts#update
          PUT    /posts/:id(.:format)      posts#update
          DELETE /posts/:id(.:format)      posts#destroy
```

倘若需要多層的路徑組合，例如每個 post 下面可以 create comment，
這時候可以寫成
```ruby
PostitTemplate::Application.routes.draw do
  resources :posts do
    resources :comments, only: [:create]
  end
end
```
這樣一來，路徑表就會新增一個 comments controller 的 create action 對應的路徑
```
$ bundle exec rake routes
       Prefix Verb   URI Pattern                        Controller#Action
post_comments POST   /posts/:post_id/comments(.:format) comments#create
        posts GET    /posts(.:format)                   posts#index
              POST   /posts(.:format)                   posts#create
     new_post GET    /posts/new(.:format)               posts#new
    edit_post GET    /posts/:id/edit(.:format)          posts#edit
         post GET    /posts/:id(.:format)               posts#show
              PATCH  /posts/:id(.:format)               posts#update
              PUT    /posts/:id(.:format)               posts#update
              DELETE /posts/:id(.:format)               posts#destroy
```

{% blockquote Rick Cook %}
Programming today is a race between software engineers striving to build bigger and better idiot-proof programs, and the universe trying to build bigger and better idiots. So far, the universe is winning.
{% endblockquote %}
