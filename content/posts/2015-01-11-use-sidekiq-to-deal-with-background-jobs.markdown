Title: 使用 Sidekiq 處理背景工作
Date: 2015-01-11
Tags: rails
Category: Web


這裡將介紹如何使用 [Sidekiq](https://github.com/mperham/sidekiq)
透過 threads 同時處理多項工作;
例如我們將比較花費時間的動作放到背景處理，
以提升使用者的操作體驗。

### 安裝 Sidekiq

在 Gemfile 中加入
```
gem 'sidekiq'
```
然後執行 `bundle`。

### 安裝 redis

Sidekiq 執行時需要使用到 [redis](http://redis.io/)，
倘若開發環境是 Mac 的話，
可以使用 Homebrew 進行安裝
```
brew install redis
```

### 啟動 redis 和 sidekiq servers

* redis: 執行 `redis-server`
* sidekiq: 在 Rails 專案下，執行 `bundle exec sidekiq`


### 程式範例

假設我們有一個寄送信件的動作如下
```ruby
AppMailer.send_welcome_email(@user).deliver
```

只要使用 Sidekiq 的 [delay](https://github.com/mperham/sidekiq/wiki/Delayed-extensions) method 就可以很容易地將動作放到背景處理
```ruby
AppMailer.delay.send_welcome_email(@user)
```

### 在 Heroku 上設定 Redis 路徑

倘若您的網站架設在 Heroku 上，
並且使用 [Redis to Go](https://addons.heroku.com/redistogo)，
由於 Sidekiq 是以 `REDIS_PROVIDER` 環境變數來設定 Redis 的路徑，
然而 Heroku 所提供的環境變數是 `REDISTOGO`;
所以我們可以執行下面的指令來連接這兩個環境變數

```
heroku config:set REDIS_PROVIDER=REDISTOGO
```

之後，
可以執行 `heroku config` 確認環境變數是否已設定成功，如下

```plain
$ heroku config
=== chlin-conifer Config Vars
RACK_ENV:                   production
RAILS_ENV:                  production
REDISTOGO_URL:              redis://redistogo:42528ab79e9e15ef9693733239b2d2c6@ray.redistogo.com:9795/
REDIS_PROVIDER:             REDISTOGO_URL
```
