Title: 使用 Service Objects 編寫註冊服務
Date: 2015-02-02
Tags: rails, design pattern
Category: Web


開發專案時，我們常常會遇到一種情況，
隨著功能不斷地加入，
Controller 也變得越來越肥胖;
例如，在下面的 `create` 方法中，
包含了使用者資料的檢驗、進行信用卡交易以及發送歡迎信件等動作。

app/controllers/users_controller.rb:

    :::ruby
    class UsersController < ApplicationController

      ... 程式碼省略 ...

      def create
        @user = User.new(user_params)

        if @user.valid? # 檢驗使用者資料
          # 信用卡交易
          charge = StripeWrapper::Charge.create(
            :amount => 999, # in cents
            :currency => "usd",
            :card => params[:stripeToken],
            :description => "Sign up for #{@user.email}"
          )
          if charge.successful?
            @user.save
            session[:user_id] = @user.id
            AppMailer.delay.send_welcome_email(@user) # 發送歡迎信件
            flash[:success] = "Thank you for registering with MyFlix."
            redirect_to home_path
          else
            flash[:danger] = charge.error_message
            render :new
          end
        else
          flash[:danger] = "Invalid user information. Please check the errors below."
          render :new
        end
      end

    end

因為描述物件之間交互作用的邏輯，
並不適合放進單一模型中，
此時可以考慮使用 [Service Objects](http://en.wikipedia.org/wiki/Service_Data_Objects) 為 Controller 瘦身。

### 編寫註冊服務

在 app/services 目錄下，
新增檔案 user_signup.rb，加入註冊相關的動作

app/services/user_signup.rb:

    :::ruby
    class UserSignup

      attr_reader :error_message

      def initialize(user)
        @user = user
      end

      def sign_up(stripe_token)
        if @user.valid? # 檢驗使用者資料
          # 信用卡交易
          charge = StripeWrapper::Charge.create(
            :amount => 999, # in cents
            :currency => "usd",
            :card => stripe_token,
            :description => "Sign up for #{@user.email}"
          )
          if charge.successful?
            @user.save
            AppMailer.delay.send_welcome_email(@user) # 發送歡迎信件
            @status = :success
            self
          else
            @status = :failed
            @error_message = charge.error_message
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

然後原先的 `create` 方法就可以進行重構，如下

app/controllers/users_controller.rb:

    :::ruby
    class UsersController < ApplicationController

      ... 程式碼省略 ...

      def create
        @user = User.new(user_params)

        # 使用者註冊
        result = UserSignup.new(@user).sign_up(params[:stripeToken])

        if result.successful?
          session[:user_id] = @user.id
          flash[:success] = "Thank you for registering with MyFlix."
          redirect_to home_path
        else
          flash[:danger] = result.error_message
          render :new
        end

      end

    end

如此一來，除了 Controller 變得簡潔，
也更容易對 `create` 和 `UserSignup` 編寫測試。
