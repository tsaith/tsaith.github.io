Title: 在 Rails 中處理信用卡付款失敗
Date: 2015-02-10
Tags: rails, stripe
Category: Web


這篇文章將以 [Stripe](/blog/2015/01/17/use-stripe-checkout-to-charge-credit-card) 金流服務為例，
示範當付款失敗時，如何暫停使用者帳號。

### 安裝套件

在 Gemfile 裡面加入
```ruby
gem 'stripe_event'
```
然後執行 `bundle install`。

### 新增 active 欄位

在 `users` table 中新增 `active` 欄位，
預設值為 `true`，如下

db/schema.rb:

    :::ruby
    create_table "users", force: true do |t|
      t.string   "full_name"
      t.string   "email"
      t.string   "password_digest"
      t.string   "slug"
      t.string   "token"
      t.boolean  "admin"
      t.string   "customer_token"
      t.datetime "created_at"
      t.datetime "updated_at"
      t.boolean  "active",          default: true # 新增此欄位
    end

### 設定 initializer

在 `config/initializers/stripe.rb` 裡面敘述付款失敗時將使帳號無效

config/initializers/stripe.rb:

    :::ruby
    Stripe.api_key = ENV['STRIPE_SECRET_KEY']

    StripeEvent.configure do |events|
      # 付款成功
      events.subscribe 'charge.succeeded' do |event|
        user = User.where(customer_token: event.data.object.customer).first
        Payment.create(user: user, amount: event.data.object.amount,
                       reference_id: event.data.object.id)
      end

      # 付款失敗
      events.subscribe 'charge.failed' do |event|
        user = User.where(customer_token: event.data.object.customer).first
        user.deactivate! # 使帳號無效
      end
    end

### 修改 Model 和 Controller

在 `User` model 裡面，新增 `deactivate!` 方法

app/models/user.rb:


    :::ruby
    class User < ActiveRecord::Base

      ... 省略程式碼 ...

      def deactivate!
        self.update_column(:active, false)
      end

    end

在處理登入的 `SessionController` 裡面，
判斷使用者帳號是否有效，如下

app/controllers/sessions_controller.rb:

    :::ruby
    class SessionsController < ApplicationController
    
      ... 省略程式碼 ...
    
      def create
        user = User.where(email: params[:email]).first
        if user && user.authenticate(params[:password])
          # 判斷帳號是否有效
          if user.active?
            session[:user_id] = user.id
            flash[:success] = "Your've signed in, enjoy!"
            redirect_to home_path
          else
            flash[:success] = "Your account has been suspended, please contact customer service."
            redirect_to sign_in_path
          end
        else
          flash[:danger] = "Invalid email or password."
          redirect_to sign_in_path
        end
      end
    end

### 設定 Stripe webhook requests

最後在 Stripe 的 [Webhook Settings](https://dashboard.stripe.com/account/webhooks) 新增欲接收 webhook requests 的 URL;
詳細的說明可以參考[先前的文章](/blog/2015/02/07/admin-views-payments)。

