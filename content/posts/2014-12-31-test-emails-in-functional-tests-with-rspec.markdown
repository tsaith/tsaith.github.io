Title: 使用 RSpec 在 Functional Tests 裡面測試郵件
Date: 2014-12-31
Tags: rails, testing
Category: Web


這篇文章將舉一些簡單的範例來說明如何使用
[RSpec](http://rspec.info/) 對郵件的寄送進行測試。

假設有一個 UsersController，
它的 create action 會寄送歡迎信給註冊的新使用者

app/controllers/users_controller.rb:

    :::ruby
    class UsersController < ApplicationController

      ... 其他程式碼 ...

      def create
        @user = User.new(user_params)

        if @user.save
          session[:user_id] = @user.id
          flash[:notice] = "Your are registered."
          # 寄送歡迎信
          AppMailer.send_welcome_email(@user).deliver
          redirect_to home_path
        else
          flash[:error] = "There's something wrong during registration."
          render :new
        end
      end

    end

如果想要測試 create action 裡面的信件寄送，
可以撰寫 functional tests 如下

spec/controllers/users_controller_spec.rb:

    :::ruby
    require "spec_helper"

    describe UsersController do

      describe "POST create" do

        context "sending emails" do

          # 在每個測試結束後，清除所有郵件
          after { ActionMailer::Base.deliveries.clear }

          # 若 inputs 有效，則寄出信件
          it "sends out email to the user with valid inputs" do
            post :create, user: { email: "alice@example.com", password: "password", full_name: "Alice Liddel" }
            expect(ActionMailer::Base.deliveries).not_to be_empty
          end

          # 檢查收件人是否正確
          it "sends out email to the right recipient" do
            post :create, user: { email: "alice@example.com", password: "password", full_name: "Alice Liddel" }
            message = ActionMailer::Base.deliveries.last
            expect(message.to).to eq ["alice@example.com"]
          end

          # 檢查信件內容是否包含使用者的名字
          it "sends out email containing the user's name with valid inputs" do
            post :create, user: { email: "alice@example.com", password: "password", full_name: "Alice Liddel" }
            message = ActionMailer::Base.deliveries.last
            expect(message.body).to include "Alice Liddel"
          end

          # 若 inputs 無效，則不寄出信件
          it "does not send out email with invalid inputs" do
            post :create, user: { email: "alice@example.com" }
            expect(ActionMailer::Base.deliveries).to be_empty
          end

        end
      end
    end

倘若不熟悉如何撰寫 functional tests 的話，
可以參考[這裡](/blog/2014/12/07/functional-testing-with-rspec)。
