Title: 使用 Concerns 幫 Model 瘦身
Date: 2015-01-09
Tags: rails
Category: Web


### 設定模組路徑

在 config/application.rb 加入
```ruby
config.autoload_paths += %W(#{Rails.root}/lib) # module paths
```
來告訴 Rails 自動載入專案 lib 下的 module files

### 抽出可共用的邏輯

假設我們有一個 Invitation model，
裡面定義了 token 的產生和清除

app/models/invitation.rb:

    :::ruby
    class Invitation < ActiveRecord::Base

      before_create :generate_token # 在 create 前自動產生 token

      belongs_to :inviter, class_name:"User"
      validates_presence_of :recipient_name, :recipient_email, :message

      def generate_token # 產生 token
        self.token = SecureRandom.urlsafe_base64
      end

      def clear_token # 清除 token
        self.update_column(:token, nil)
      end

    end

這時候我們可以考慮使用 ActiveSupport::Concern
將 token 處理的相關邏輯抽離出來並封裝成一個模組，如下

lib/tokenable.rb:

    :::ruby
    module Tokenable
      extend ActiveSupport:: Concern

      included do
        before_create :generate_token
      end

      def generate_token
        self.token = SecureRandom.urlsafe_base64
      end

      def clear_token
        self.update_column(:token, nil)
      end

    end

然後，原先的 model 就可以改寫成

app/models/invitation.rb:

    :::ruby
    class Invitation < ActiveRecord::Base

      include Tokenable # 處理 token

      belongs_to :inviter, class_name:"User"
      validates_presence_of :recipient_name, :recipient_email, :message

    end

正如所見，改寫後的 model 變得更加簡潔;
此外，倘若其他 model 需要同樣功能時，也可以很方便地調用已封裝好的模組。
對於此議題，在 DHH 的[文章](https://signalvnoise.com/posts/3372-put-chubby-models-on-a-diet-with-concerns)中有更詳細的討論。
