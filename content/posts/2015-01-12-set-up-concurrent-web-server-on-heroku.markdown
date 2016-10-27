Title: 在 Heroku 上架設 concurrent server
Date: 2015-01-12
Tags: rails, heroku
Category: Web


這篇文章將介紹如何使用
[Unicorn](http://unicorn.bogomips.org/) 和
[Sidekiq](http://sidekiq.org/)
在 Heroku 上架設能夠處理 concurrent requests 的伺服器。

### 申請 Redis To Go

因為 Sidekiq 需要用到 [Redis](http://redis.io/)，
所以需要先在 Heroku 為你的 app 申請免費的
[Redis To Go](https://addons.heroku.com/redistogo) 服務。

### 安裝 gems

在專案目錄下的 Gemfile 中加入
```
gem 'unicorn'
gem 'sidekiq'
```
然後執行 `bundle install`。

### 設定 Unicorn

在 config/ 下新增檔案 `unicorn.rb`，內容如下

config/unicorn.rb:

    :::ruby
    worker_processes Integer(ENV["WEB_CONCURRENCY"] || 3)
    timeout 15
    preload_app true

    before_fork do |server, worker|
      Signal.trap 'TERM' do
        puts 'Unicorn master intercepting TERM and sending myself QUIT instead'
        Process.kill 'QUIT', Process.pid
      end

      defined?(ActiveRecord::Base) and
        ActiveRecord::Base.connection.disconnect!
    end

    after_fork do |server, worker|
      Signal.trap 'TERM' do
        puts 'Unicorn worker intercepting TERM and doing nothing. Wait for master to send QUIT'
      end

      defined?(ActiveRecord::Base) and
        ActiveRecord::Base.establish_connection
    end

關於 Unicorn 的設定，Heroku 有提供詳細的[說明](https://devcenter.heroku.com/articles/rails-unicorn)。

### 設定 Procfile

在專案目錄下設定 `Procfile`，如下

```
web: bundle exec unicorn -p $PORT -c ./config/unicorn.rb
worker: bundle exec sidekiq -c 2 -v
```

最後，再將專案部署到 Heroku 就完成了;
倘若想檢查目前有幾個 dynos 正在運行，
可以執行 `heroku ps` 來查看狀態。

### 同場加映

在上面的設定中，一共會使用到兩個 dynos;
一個給 web，另一個給 Sidekiq。
但 Heroku 的免費方案只提供一個 dyno，
倘若只是想要練習，
我們可以修改 `unicorn.rb`，
要求 unicorn 的 worker 來跑 Sidekiq

config/unicorn.rb:

    :::ruby
    worker_processes Integer(ENV["WEB_CONCURRENCY"] || 3)
    timeout 15
    preload_app true

    before_fork do |server, worker|
      Signal.trap 'TERM' do
        puts 'Unicorn master intercepting TERM and sending myself QUIT instead'
        Process.kill 'QUIT', Process.pid
      end

      defined?(ActiveRecord::Base) and
        ActiveRecord::Base.connection.disconnect!

      # 加入這一行
      @sidekiq_pid ||= spawn("bundle exec sidekiq -c 2")
    end

    after_fork do |server, worker|
      Signal.trap 'TERM' do
        puts 'Unicorn worker intercepting TERM and doing nothing. Wait for master to send QUIT'
      end

      defined?(ActiveRecord::Base) and
        ActiveRecord::Base.establish_connection

    end

然後再修改 `Procfile`，保留 web dyno 即可。
```
web: bundle exec unicorn -p $PORT -c ./config/unicorn.rb
```
