Title: 設定 polymorphic association
Date: 2014-11-15
Tags: rails
Category: Web


假設我們有個布告版，上面可以張貼文章和留言，
如果我們希望新增一個功能讓使用者可以對文章或留言進行投票，
這時候可以透過 polymorphic association 來描述
Vote 和 Post 以及 Comment 三個物件模型之間的關係。

### 新增 Table

首先，在資料庫中新增一個 votes table 來儲存投票資訊;
在 votes 中，
`voteable_type` 和 `voteable_id` 分別代表被投票物件的名稱和 id。
新增完成後，查看 db/schema.rb 如下

    :::ruby
    create_table "votes", force: true do |t|
      t.boolean  "vote"
      t.integer  "user_id"
      t.string   "voteable_type"
      t.integer  "voteable_id"
      t.datetime "created_at"
      t.datetime "updated_at"
    end

    create_table "posts", force: true do |t|
      t.string   "url"
      t.string   "title"
      t.text     "description"
      t.integer  "user_id"
      t.datetime "created_at"
      t.datetime "updated_at"
    end

    create_table "comments", force: true do |t|
      t.text     "body"
      t.integer  "user_id"
      t.integer  "post_id"
      t.datetime "created_at"
      t.datetime "updated_at"
    end

### 設定 Models

新增檔案 app/models/vote.rb，
使用 `polymorphic: true` 來指定 `voteable` 是 polymorphic。
此外，我們進一步地規定每位使用者只能對每個 `voteable` 物件進行一次投票。

app/models/vote.rb:

    :::ruby
    class Vote < ActiveRecord::Base
      belongs_to :user
      belongs_to :voteable, polymorphic: true

      validates_uniqueness_of :user, scope: [:voteable_type, :voteable_id]
    end

接著在 post.rb 和 comment.rb 中加入 `has_many :votes, as: :voteable`
來指定每個 post 和 comment 都可以擁有多個投票。

app/models/post.rb:

    :::ruby
    class Post < ActiveRecord::Base
      belongs_to :user
      has_many :comments, :dependent => :destroy
      has_many :votes, as: :voteable

      validates :title, presence: true
      validates :description, presence: true

    end

app/models/comment.rb:

    :::ruby
    class Comment < ActiveRecord::Base
      belongs_to :user
      belongs_to :post
      has_many :votes, as: :voteable

      validates :body, presence: true
      validates :user_id, presence: true
      validates :post_id, presence: true

    end

設定好模型之間的關係後，
我們就可以開始在 Controllers 和 Views 中使用這些物件進行開發。
