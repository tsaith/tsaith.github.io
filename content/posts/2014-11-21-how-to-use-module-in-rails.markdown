Title: 在 Rails 中使用 module
Date: 2014-11-21
Tags: rails
Category: Web


在開發 Rails 時，我們常常遇到一種情況，
不同的物件模型需要用到相同的功能，
這時候可以考慮將這功能包裝成一個模組，
以方便調用。


### 設定搜尋路徑

首先，在 config/application.rb 裡面加入 `config.autoload_paths += %W(#{config.root}/lib)` 設定 lib 為 modules 的存放路徑。

```ruby
require File.expand_path('../boot', __FILE__)

require 'rails/all'

# Require the gems listed in Gemfile, including any gems
# you've limited to :test, :development, or :production.
Bundler.require(:default, Rails.env)

module PostitTemplate
  class Application < Rails::Application
    # Settings in config/environments/* take precedence over those specified here.
    # Application configuration should go into files in config/initializers
    # -- all .rb files in that directory are automatically loaded.

    # Module paths
    config.autoload_paths += %W(#{config.root}/lib)

    # Set Time.zone default to the specified zone and make Active Record auto-convert to this zone.
    # Run "rake -D time" for a list of tasks for finding time zone names. Default is UTC.
    config.time_zone = 'Taipei'

    # The default locale is :en and all translations from config/locales/*.rb,yml are auto loaded.
    # config.i18n.load_path += Dir[Rails.root.join('my', 'locales', '*.{rb,yml}').to_s]
    # config.i18n.default_locale = :de

    # Tealeaf note: Bootstrap sass gem addition
    config.assets.precompile += %w(*.png *.jpg *.jpeg *.gif)
  end
end
```
### 包裝模組

然後將模組的檔案放到 lib/ 下面; 請特別注意，
檔名和模組名稱需要一致，舉例來說，
如果檔名為 voteable_th.rb，那麼模組名稱就是 VoteableTh，
不然，Rails 會找不到這模組(至少在 4.1.6 以下的版本還是如此)。
而這裡的 voteable_th.rb 內容如下

```ruby
module VoteableTh
  extend ActiveSupport:: Concern

  included do
    has_many :votes, as: :voteable, :dependent => :destroy
  end

  def total_votes
    up_votes - down_votes
  end

  def up_votes
    self.votes.where(vote: true).size
  end

  def down_votes
    self.votes.where(vote: false).size
  end

end
```

### 調用模組

最後，我們可以直接在物件模型中透過 `include `來使用模組，如下

```ruby
class Post < ActiveRecord::Base
  include VoteableTh

  belongs_to :creator, class_name: "User", foreign_key: "user_id"
  has_many :comments, :dependent => :destroy

  validates :title, presence: true, length: {minimum: 3}
  validates :description, presence: true

end
```
