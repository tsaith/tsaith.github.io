Title: 查看交易記錄的後台功能
Date: 2015-02-07
Tags: rails, stripe
Category: Web


這裡將以 [Stripe](/blog/2015/01/17/use-stripe-checkout-to-charge-credit-card) 金流服務為例，
介紹如何為網站後台新增查看交易記錄的功能。

### 安裝套件

在 Gemfile 裡面加入
```ruby
gem 'stripe_event'
```
然後執行 `bundle install`。

### 設定 routes

在 `routes.rb` 加入

config/routes.rb:

    :::ruby
    namespace :admin do
      resources :payments, only: [:index]
    end

    mount StripeEvent::Engine, at: '/stripe_events'

### 新增 payments table

在資料庫中新增 `payments` table 如下

db/schema.rb:

    :::ruby
    create_table "payments", force: true do |t|
      t.integer "user_id"
      t.integer "amount"
      t.string  "reference_id"
    end

### 設定 initializer

在 `config/initializers/stripe.rb` 裡面處理付款成功的事件

config/initializers/stripe.rb:

    :::ruby
    Stripe.api_key = ENV['STRIPE_SECRET_KEY']

    StripeEvent.configure do |events|

      # 付款成功
      events.subscribe 'charge.succeeded' do |event|
        user = User.where(customer_token: event.data.object.customer).first
        # 產生交易記錄
        Payment.create(user: user, amount: event.data.object.amount,
                       reference_id: event.data.object.id)
      end
    end

倘若不清楚如何使用 Stripe 提供交易機制，
可以參考[這裡](/blog/2015/02/06/create-subscriptions-in-stripe/)。

### 新增 Model/View/Controller

新增 `Payment` model

app/models/payment.rb:

    :::ruby
    class Payment < ActiveRecord::Base
      belongs_to :user
    end

新增 PaymentsController

app/controllers/admin/payments_controller.rb:

    :::ruby
    class Admin::PaymentsController < AdminsController

      def index
        @payments = Payment.all
      end

    end

新增 view 以查看交易記錄，如下

{% img https://farm8.staticflickr.com/7374/16463279546_8c9e4a86d2_b.jpg %}

app/views/admin/payments/index.html.haml:

    :::haml
    %section.admin_payments
      .container
        .row
          .col-sm-10.col-sm-offset-1
            %section.payment_history
              %ul.nav.nav-tabs
                %li.active
                  = link_to "Recent Payments", admin_payments_path
                %li
                  = link_to "Add a New Video", new_admin_video_path

              %table.table
                %thead
                  %tr
                    %th Name
                    %th Email
                    %th Amount
                    %th Reference ID
                %tbody
                  - @payments.each do |payment|
                    %tr
                      %td
                        = payment.user.full_name
                      %td
                        = payment.user.email
                      %td
                        = "$#{payment.amount/100.0}"
                      %td
                        = payment.reference_id

### 設定 Stripe Webhooks

最後，在 Stripe 的 [Webhook Settings](https://dashboard.stripe.com/account/webhooks) 裡面，
新增要接收 webhook requests 的 URL;
例如，倘若我們的網站位址是 th-myflix.herokuapp.com，
那麼新增的 URL 即為 `th-myflix.herokuapp.com/stripe_events`

{% img https://farm8.staticflickr.com/7324/15871057173_cc829aee26_b.jpg %}

在本機開發時，
可以使用免費的 [ngrok](https://ngrok.com/) 服務產生 public 位址，
以接收 webhook requests 進行測試。

