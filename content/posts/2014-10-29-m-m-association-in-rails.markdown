Title: 在 Rails 中設定多對多關聯性
Date: 2014-10-29
Tags: rails
Category: Web



這裡將介紹如何在 Rails 中透過 `has_many through:` 來設定多對多關聯性。
而一對多關聯性的介紹可參考先前的[文章](/blog/2014/10/29/1-m-association-in-rails/)。

假設我們有兩種模型 Post 和 Category，
倘若每個 post 可擁有多個 categories，
而每個 Category 也可以擁有多個 posts，
於是 Post 和 Category 之間就存在著多對多的關係;
以下將敘述如何實作這樣的關聯性。

### 建立 tables

首先我們需要在資料庫中新增三個 tables，
分別是 posts、categories 和 post_categories;
在 post_categories 中應包含 post_id 和 category_id 這兩個 column。
(如果不清楚如何新增 table 可參考[這裡](/blog/2014/10/29/1-m-association-in-rails/))

新增完 tables 後，請檢查 db/schema.rb 以確定 table 的格式的確如你所預期的
```ruby
ActiveRecord::Schema.define(version: 20141031042824) do

  create_table "posts", force: true do |t| 
    t.string   "title"
    t.string   "url"
    t.text     "description"

    t.datetime "created_at"
    t.datetime "updated_at"
  end

  create_table "categories", force: true do |t| 
    t.string   "name"

    t.datetime "created_at"
    t.datetime "updated_at"
  end 

  create_table "post_categories", force: true do |t|
    t.integer  "post_id"
    t.integer  "category_id"
 
    t.datetime "created_at"
    t.datetime "updated_at"
  end 

end
```

### 設定 models

最後，我們需要指定 Post 和 Category 以及 PostCategory 三個模型之間的關係。

編輯 app/models/post.rb，如下 
```ruby
class Post < ActiveRecord::Base
  has_many :post_categories
  has_many :categories, through: :post_categories 
end
```

編輯 app/models/category.rb，如下 

```ruby
class Category < ActiveRecord::Base
  has_many :post_categories
  has_many :posts, through: :post_categories 
end
```

編輯 app/models/post_category.rb，如下

```ruby
class PostCategory < ActiveRecord::Base
  belongs_to :post
  belongs_to :category
end
```

以上，就是在 Rails 中多對多關聯性的實作步驟。

