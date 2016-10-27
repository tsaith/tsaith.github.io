Title: 在測試中模擬物件行為
Date: 2015-01-27
Tags: rails, testing
Category: Web


當我們希望對某個開發中的功能進行測試，
而那個功能需要其他物件的支援才能工作的話，
此時可以使用 `double` 來[模擬](https://relishapp.com/rspec/rspec-mocks/v/2-99/docs/)
週邊物件並定義行為;
如此一來，
我們就能將精神完全投入在開發中的功能，
而不用同時兼顧其他地方。

假設我們現在想設計一個網站，
使用者在註冊時必須刷卡付費來使用內部服務。
倘若我們剛編寫了創造使用者的 `create` 方法，如下

users_controller.rb:

    :::ruby
    class UsersController < ApplicationController

      ... 程式碼省略 ...

      def create
        @user = User.new(user_params)

        if @user.valid?
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
            AppMailer.delay.send_welcome_email(@user)
            flash[:success] = "You are registered."
            redirect_to home_path
          else
            flash[:danger] = charge.error_message
            render :new
          end
        else
          flash[:danger] = "There's something wrong during registration."
          render :new
        end
      end

      ... 程式碼省略 ...

    end

這個方法裡面，
使用了信用卡服務來索取註冊費用;
而當編寫測試時，
我們會希望單純地測試 `create` 方法的邏輯是否正確，
這時候就可以考慮使用 `double` 來模擬信用卡交易的行為

users_controller_spec.rb:

    :::ruby
    require "spec_helper"

    describe UsersController do

      describe "POST create" do

        context "with valid personal info and valid card" do
          # 當交易成功時 successful? 方法將回傳 true
          let(:charge) { double(:charge, successful?: true ) }
          before do
            # 預期將會呼叫到 StripeWrapper::Charge.create 方法，並回傳 charge 物件
            StripeWrapper::Charge.should_receive(:create).and_return(charge)
          end
          after { ActionMailer::Base.deliveries.clear }

          it "creates the user" do
            post :create, user: Fabricate.attributes_for(:user), stripeToken: "123"
            expect(User.count).to eq 1
          end
          it "sets flash success message" do
            post :create, user: Fabricate.attributes_for(:user), stripeToken: "123"
            expect(flash[:success]).to be_present
          end
          it "redirects to the home page" do
            post :create, user: Fabricate.attributes_for(:user), stripeToken: "123"
            expect(response).to redirect_to home_path
          end
          it "sends out email to the user" do
            post :create, user: { email: "alice@example.com", password: "password", full_name: "Alice Liddel" }
            message = ActionMailer::Base.deliveries.last
            expect(message.to).to eq ["alice@example.com"]
          end

        end

        context "with valid personal info and declined card" do
          # 交易失敗時，successful? 方法回傳 false， error_message 回傳錯誤訊息
          let(:charge) { double(:charge, successful?: false, error_message: "Your card was declined." ) }
          before do
            # 預期將會呼叫到 StripeWrapper::Charge.create 方法，並回傳 charge 物件
            StripeWrapper::Charge.should_receive(:create).and_return(charge)
          end
          after { ActionMailer::Base.deliveries.clear }

          it "does not create the user" do
            post :create, user: Fabricate.attributes_for(:user), stripeToken: "123"
            expect(User.count).to eq 0
          end
          it "renders the :new template" do
            post :create, user: Fabricate.attributes_for(:user), stripeToken: "123"
            expect(response).to render_template :new

          end
          it "sets @user" do
            post :create, user: Fabricate.attributes_for(:user), stripeToken: "123"
            expect(assigns(:user)).to be_instance_of User
          end
          it "sets the flash danger message" do
            post :create, user: Fabricate.attributes_for(:user), stripeToken: "123"
            expect(flash[:danger]).to be_present
          end
          it "does not send out email" do
            post :create, user: Fabricate.attributes_for(:user), stripeToken: "123"
            expect(ActionMailer::Base.deliveries).to be_empty
          end
        end

        context "with invalid personal info" do
          after { ActionMailer::Base.deliveries.clear }

          it "does not create the user" do
            post :create, user: Fabricate.attributes_for(:user, password: "")
            expect(User.count).to eq 0
          end
          it "renders the :new template" do
            post :create, user: Fabricate.attributes_for(:user, password: "")
            expect(response).to render_template :new

          end
          it "sets @user" do
            post :create, user: Fabricate.attributes_for(:user, password: "")
            expect(assigns(:user)).to be_instance_of User
          end
          it "sets the flash danger message" do
            post :create, user: Fabricate.attributes_for(:user, password: "")
            expect(flash[:danger]).to be_present
          end
          it "does not send out email" do
            post :create, user: { email: "alice@example.com" }
            expect(ActionMailer::Base.deliveries).to be_empty
          end
        end
      end

    end

在測試中模擬物件的技巧，
一方面讓我們可以專心地測試正在開發的功能，
另一方面，也可以縮短呼叫物件時等候回應的時間，
以提升測試效率。

