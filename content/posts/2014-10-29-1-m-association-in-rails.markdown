Title: 在 Rails 中設定一對多關聯性
Date: 2014-10-29
Tags: rails
Category: Web


物件與物件之間的關係,可以是一對一、一對多或多對多;
這裡將介紹如何在 Rails 中設定一對多關聯性。

假設我們現在想設計一個網站讓使用者可以在上面發表文章，
由於每位使用者可以發表多篇文章，
於是使用者和文章之間就存在著一對多的關係;
以下將敘述如何實作這樣的關聯性。

### 建立 migration

首先， 為 users table 建立 migration 檔案
```
rails generate migration create_users
```
執行命令後，將產生對應的檔案(數字部分代表建立的時間)
```plain
db/migrate/20141028055510_create_users.rb
```
編輯此檔案的內容，指定 table 包含一個 username 的 column，如下
```ruby
class CreateUsers < ActiveRecord::Migration
  def change
    create_table :users do |t|
      t.string :username

      t.timestamps
    end
  end
end
```
然後執行
```
bundle exec rake db:migrate
```
這時候資料庫就會產生 users 這個 table。


接下來使用類似步驟來產生 posts table;
先執行
```plain
rails generate migration create_posts
```

然後編輯
```plain
db/migrate/20141028043352_create_posts.rb
```
指定 table 擁有 title 和 user_id 兩個 column
```ruby
class CreatePosts < ActiveRecord::Migration
  def change
    create_table :posts do |t|
      t.string :title
      t.integer :user_id

      t.timestamps
    end
  end
end
```

最後，執行 `bundle exec rake db:migrate` 來產生 posts table。

### 檢查 database schema

我們可以在專案目錄下查看 db/schema.rb 的內容, 如下

```ruby
ActiveRecord::Schema.define(version: 20141028103914) do

  create_table "users", force: true do |t|
    t.string   "username"

    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "posts", force: true do |t|
    t.string   "title"
    t.integer  "user_id"

    t.datetime "created_at"
    t.datetime "updated_at"
  end

end
```
這裡面記錄了資料庫中 users 和 posts 兩個 tables 分別具有哪些 columns。

### 設定 models

現在，我們要指定 User model 和 Post model 之間的關係。

首先，新增並編輯 app/models/user.rb，指定 user 可以擁有多個 posts
```ruby
 class User < ActiveRecord::Base
   has_many :posts
 end
```

然後，新增並編輯 app/models/post.rb，指定 post 屬於 user
```ruby
class Post < ActiveRecord::Base
  belongs_to :user
end
```

倘若一切順利，現在你已經完成 User 和 Post 一對多的關聯性實作。
