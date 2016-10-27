Title: 製作和發佈 gem
Date: 2014-11-21
Tags: rails
Category: Web


當我們在某個專案中完成了某個功能並且模組化後，
倘若其他專案也需要同樣功能，
或是希望分享給開源社群時，
這時候就可以將它製作成 gem 方便大家使用。

### 製作過程

* 新增一個 gem 的資料夾，假設名稱為 voteable-gem
* 進入資料夾中，新增 lib 資料夾，並將寫好的程式檔案放進 lib/
```
$ ls lib
voteable_th.rb
```
在上面的範例中，voteable_th.rb 是一個用來投票的模組，內容如下

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

* 在 voteable-gem 資料夾下新增檔案 voteable.gemspec 來定義
gem specification，內容如下

```ruby
Gem::Specification.new do |s|
  s.name        = 'voteable_th'              # gem 的名字
  s.version     = '0.0.0'                    # 版本號碼
  s.summary     = "A voting gem"
  s.description = "A voting gem for Rails"
  s.authors     = ["Tsung-Hua Tsai"]
  s.email       = 'tsai.tsunghua@gmail.com'
  s.files       = ["lib/voteable_th.rb"]     # 檔案位置
  s.homepage    = 'http://tsaith.github.io/'
  s.license     = 'MIT'
end
```

* 使用 `gem build` 來製作 gem
```
$ gem build voteable.gemspec
Successfully built RubyGem
Name: voteable_th
Version: 0.0.1
File: voteable_th-0.0.0.gem
```
### 發佈到開源社群

* 到 [Rubygems.org](https://rubygems.org/) 上面[註冊](https://rubygems.org/sign_up)

* 使用 `gem push` 將 gem 發佈到 Rubygems.org
```
$ gem push voteable_th-0.0.0.gem
Pushing gem to https://rubygems.org...
Successfully registered gem: voteable_th (0.0.0)
```

倘若一切順利，恭喜你已經成功地將 gem 發佈出去。
如果要查詢剛剛發佈的 gem 請執行
```
$ gem search -r voteable_th

*** REMOTE GEMS ***

voteable_th (0.0.0)
```

假設發現已發佈的 gem 有嚴重 bug 時，
可使用 `gem yank` 來避免以後的使用者下載
```
$ gem yank voteable_th -v 0.0.0
Yanking gem from https://rubygems.org...
Successfully yanked gem: voteable_th (0.0.0)
```

倘若想回復上面的動作，則執行
```
$ gem yank voteable_th -v 0.0.0 --undo
Unyanking gem from https://rubygems.org...
Successfully unyanked gem: voteable_th (0.0.0)
```

其他進階的操作說明可參考[RubyGems Guides](http://guides.rubygems.org/)。
