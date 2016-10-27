Title: 依照簽署方案進行收費
Date: 2015-02-06
Tags: rails, stripe
Category: Web


假設我們現在想為網站開發收費機制，
使用者註冊後會立刻索取第一個月的服務費用，
之後每過一個月，
系統都會自動向客戶的信用卡帳戶請款。
下面將以 [Stripe](/blog/2015/01/17/use-stripe-checkout-to-charge-credit-card) 金流服務為例，
敘述如何在 Rails 中實作這項功能。

### 設定 Plans

請先在 [Stripe Plans](https://dashboard.stripe.com/test/plans)
新增一個 ID 為 `base` 的收費方案，如下

{% img https://farm8.staticflickr.com/7408/16301555708_62a8f3a01c_b.jpg %}

### 新增 customer_token

然後在 Rails 的 `users` table 裡面，
新增 `customer_token` 欄位，如下

db/schema.rb:

    :::ruby
    create_table "users", force: true do |t|
      t.string   "full_name"
      t.string   "email"
      t.string   "password_digest"
      t.string   "slug"
      t.string   "token"
      t.boolean  "admin"
      t.string   "customer_token"   # 新增 customer_token
      t.boolean  "active",          default: true
      t.datetime "created_at"
      t.datetime "updated_at"
    end

### 設定 Stripe API Key

在 config/initializers/stripe.rb，
裡面設定 Stripe 的 API Key

config/initializers/stripe.rb:

    :::ruby
    Stripe.api_key = ENV['STRIPE_SECRET_KEY']

### 產生 Stripe customer

在處理註冊的[服務](/blog/2015/02/02/write-a-sign-up-service-with-service-objects-pattern) 裡面，
產生 Stripe customer，
並將 customer token 儲存下來

app/services/user_signup.rb:


    :::ruby
    class UserSignup

      attr_reader :error_message

      def initialize(user)
        @user = user
      end

      def sign_up(stripe_token)
        if @user.valid?
          # 產生 Stripe customer
          customer = StripeWrapper::Customer.create(
            :user => @user,
            :card => stripe_token,
            :description => "Sign up for #{@user.email}"
          )
          if customer.successful?
            # 儲存 customer token
            @user.customer_token = customer.customer_token
            @user.save
            AppMailer.delay.send_welcome_email(@user)
            @status = :success
            self
          else
            @status = :failed
            @error_message = customer.error_message
            self
          end
        else
          @status = :failed
          @error_message = "Invalid user information. Please check the errors below."
          self
        end
      end

      def successful?
        @status == :success
      end

    end


    class UserSignup

      attr_reader :error_message

      def initialize(user)
        @user = user
      end

      def sign_up(stripe_token)
        if @user.valid?
          # 產生 Stripe customer
          customer = StripeWrapper::Customer.create(
            :user => @user,
            :card => stripe_token,
            :description => "Sign up for #{@user.email}"
          )
          if customer.successful?
            @user.save
            AppMailer.delay.send_welcome_email(@user)
            @status = :success
            self
          else
            @status = :failed
            @error_message = customer.error_message
            self
          end
        else
          @status = :failed
          @error_message = "Invalid user information. Please check the errors below."
          self
        end
      end

      def successful?
        @status == :success
      end

    end

`StripeWrapper` 定義了產生 Stripe customer 的動作，
並且將預設方案設為 `base`

app/models/stripe_wrapper.rb:

    :::ruby
    module StripeWrapper
      class Customer
        attr_reader :response, :error_message

        def initialize(options = {})
          @response = options[:response]
          @error_message= options[:error_message]
        end

        def self.create(options = {})
          begin
            response = Stripe::Customer.create(
              :card => options[:card],
              :plan => options[:plan] || "base", # 預設為 base 方案
              :email => options[:user].email
            )
            new(response: response)
          rescue Stripe::CardError => e
            new(error_message: e.message)
          end
        end

        def successful?
          response.present?
        end

        def customer_token
          response.id
        end
      end
    end
