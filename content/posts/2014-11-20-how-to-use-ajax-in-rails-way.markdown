Title: 在 Rails 中使用 Ajax
Date: 2014-11-20
Tags: rails
Category: Web


假設有一個投票功能，每次按文章左側的上下箭頭可以表示贊成或反對，
但我們不希望使用者每次投票時，瀏覽器都必須重新載入頁面，
這時候可以使用 [Ajax](http://zh.wikipedia.org/wiki/AJAX) 技術來實現。

{% img https://farm8.staticflickr.com/7518/15646273670_3d1f14d6e4_b.jpg %}

{% img https://farm8.staticflickr.com/7564/15807472506_af32ac663c_b.jpg %}

### 設定 routes

對應上面的範例，我們先設定 config/routes.rb，
因為投票動作本身沒有 view， 所以將動作設定為 post

```ruby
resources :posts do
  member do
    post :vote
  end
end
```

### 設定 view

接著開啟 html 檔案 app/views/posts/_post.html.erb
加入 `remote: true`，來呼叫 javascript 動作

```ruby
<div class="row">
  <div id="post_vote_error_<%= post.to_param %>" class="alert alert-error" style="display:none">
    You can only vote on a post once.
  </div>
  <div class="span0 well text-center">
    <%= link_to vote_post_path(post, vote: true), method: 'post', remote: true do %>
      <i class='icon-arrow-up'></i>
    <% end %>
    <br/>
    <span id="post_<%= post.slug %>_votes"><%= post.total_votes %> votes </span>
    <br/>
    <%= link_to vote_post_path(post, vote: false), method: 'post', remote: true do %>
      <i class='icon-arrow-down'></i>
    <% end %>
  </div>
</div>
...
```

然後在同個資料夾下新增檔案 app/views/posts/vote.js.erb，於其中撰寫
javascript 的工作邏輯;
若投票成功，就更新投票數，如果失敗，則顯示錯誤訊息。

```ruby
<% if @vote.valid? %>
  $('#post_<%= @post.slug %>_votes').html('<%= @post.total_votes %> votes');
<% else %>
  $('#post_vote_error_<%= @post.to_param %>').show().fadeOut(3000);
<% end %>
```


因為在投票的物件模型中，使用了 `validates_uniqueness_of`
來限定每位使用者只能投票一次

```ruby
class Vote < ActiveRecord::Base
  belongs_to :user
  belongs_to :voteable, polymorphic: true

  validates_uniqueness_of :user, scope: [:voteable_type, :voteable_id]
end
```

所以當重複投票時，將產生投票失敗，
javascript 將會搜尋 html 中 id 為`post_vote_error_<%= @post.to_param %>` 的元件並顯示，如下

{% img https://farm8.staticflickr.com/7499/15831102395_739f1b9171_b.jpg %}


### 設定 controller

最後，我們需要在 controller 的 vote method 中使用 `respond_to`
來分別撰寫對應 html 和 javascript 的處理

```ruby
  def vote
    @vote = Vote.create(voteable: @post, creator: current_user, vote: params[:vote])
    respond_to do |format|
      format.html do
        if @vote.valid?
          flash[:notice] = "Your vote is counted."
        else
          flash[:error] = "You can only vote on a post once."
        end
        redirect_to :back
      end
      format.js
    end
  end
```

