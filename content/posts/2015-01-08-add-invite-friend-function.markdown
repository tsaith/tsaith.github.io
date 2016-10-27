Title: 在網站中加入 Invite 功能
Date: 2015-01-08
Tags: rails
Category: Web


這裡將介紹如何實作邀請朋友來網站註冊的功能。

### 操作流程

使用者可在邀請頁面填寫朋友的名字、郵件地址以及邀請訊息，
然後送出
{% img https://farm8.staticflickr.com/7550/16039561348_62a3888225_b.jpg %}

然後，被邀請者將會收到邀請信，
內附連結可導向網站的註冊頁面
{% img https://farm8.staticflickr.com/7567/16225203211_cbd263957b_b.jpg %}

被邀請者進行註冊，然後登入
{% img https://farm9.staticflickr.com/8608/16201176056_50250a830c_b.jpg %}

網站自動為邀請人與被邀請者設定互相跟隨的關係
(若想知道如何開發跟隨功能，請參考另一篇[文章](/blog/2014/12/31/implement-user-following))
{% img https://farm8.staticflickr.com/7544/15607220283_a001dc64ba_b.jpg %}

### 設定路徑

在 routes.rb 中加入

config/routes.rb:

    :::ruby
    ... 省略程式碼 ...

    get 'sign_up', to: 'users#new'
    get 'sign_up/:token', to: 'users#new_with_invitation_token',
                          as: 'sign_up_with_invitation_token'

    resources :invitations, only: [:new, :create]
    get 'expired_token', to: 'pages#expired_token'


### Database

在資料庫新增 invitaions table

db/schema.rb:

    :::ruby
    ... 省略程式碼 ...

    create_table "invitations", force: true do |t|
      t.integer  "inviter_id"
      t.string   "recipient_name"
      t.string   "recipient_email"
      t.text     "message"
      t.string   "token"
      t.datetime "created_at"
      t.datetime "updated_at"
    end


### Controllers

使用者可以藉由 invitation token 進行註冊

app/controllers/users_controller.rb:

    :::ruby
    class UsersController < ApplicationController
      ... 省略程式碼 ...

      def new
        @user = User.new
      end

      def new_with_invitation_token # 使用 invitation token 註冊
        invitation = Invitation.where(token: params[:token]).first
        if invitation
          @invitation_token = invitation.token
          @user = User.new(email: invitation.recipient_email)
          render :new
        else
          redirect_to expired_token_path
        end
      end

      def create
        @user = User.new(user_params)
        if @user.save
          session[:user_id] = @user.id
          handle_invitation # 自動設定邀請者與被邀請者互相跟隨的關係
          AppMailer.send_welcome_email(@user).deliver
          flash[:notice] = "Your are registered."
          redirect_to home_path
        else
          flash[:error] = "There's something wrong during registration."
          render :new
        end
      end

      private

      ... 省略程式碼 ...

      def handle_invitation
        invitation = Invitation.where(token: params[:invitation_token]).first
        if invitation
          @user.follow(invitation.inviter)
          invitation.inviter.follow(@user)
          invitation.clear_token
        end
      end
    end

處理邀請記錄

app/controllers/invitations_controller.rb:

    :::ruby
    class InvitationsController < ApplicationController

      before_action :require_user

      def new
        @invitation = Invitation.new
      end

      def create
        @invitation = current_user.invitations.build(invitation_params)
        if @invitation.save # 成功新增邀請
          AppMailer.send_invitation_email(@invitation).deliver
          flash[:success] = "You have successfully invited #{@invitation.recipient_name}."
          redirect_to new_invitation_path
        else
          @invitation = Invitation.new
          flash[:error] = "Failed to invite your friend."
          render :new
        end
      end

      private

      def invitation_params
        params.require(:invitation).permit(:recipient_name, :recipient_email, :message)
      end

    end

### Views

先在適當的頁面加入邀請連結

app/views/shared/_header.html.haml:

    ::haml
    ... 省略程式碼 ...

    %li
      = link_to "Invite a friend", new_invitation_path # 邀請連結
      %a(href="#") Account
      %a(href="#") Plan and Billing
      %a(href="/sign_out") Sign Out

新增邀請頁面

app/views/invitations/new.html.haml:

    :::haml
    %section.invite.container
      .row
        .col-sm-10.col-sm-offset-1
          = bootstrap_form_for @invitation do |f|
            %header
              %h1 Invite a friend to join MyFlix!
            %fieldset
              .row
                .col-sm-4
                  = f.text_field :recipient_name, label: "Friend's Name"
                  = f.email_field :recipient_email, label: "Friend's Email Address"
                  = f.text_area :message, label: "Message", value: "Please join this really cool site!", rows: 6
            = f.submit "Send Invitation"


在註冊頁面加入隱藏的 invitation token

app/views/users/new.html.haml:

    :::haml
    %section.register.container
      .row
        .col-sm-10.col-sm-offset-1
          -#%form.form-horizontal
          = bootstrap_form_for @user do |f|
            %header
              %h1 Register
            .row
              .col-sm-4
                = f.email_field :email, label: "Email Address"
                = f.password_field :password
                = f.text_field :full_name, label: "Full Name"
                -# 隱藏的 invitation token
                = hidden_field_tag :invitation_token, @invitation_token
            = f.submit "Sign up"

顯示連結過期的頁面

app/views/pages/expired_token.html.haml:

    :::haml
    %section.invalid_token.container
      .row
        .col-sm-10.col-sm-offset-1
          %p Your link is expired.

### Models

app/models/invitation.rb:

    :::ruby
    class Invitation < ActiveRecord::Base

      before_create :generate_token

      belongs_to :inviter, class_name:"User"
      validates_presence_of :recipient_name, :recipient_email, :message

      def generate_token
        self.token = SecureRandom.urlsafe_base64
      end

      def clear_token
        self.update_column(:token, nil)
      end

    end

app/models/user.rb:

    :::ruby
    class User < ActiveRecord::Base
      ... 省略程式碼 ...

      has_many :invitations, foreign_key: "inviter_id"

      def follow(another_user)
        following_relationships.create(leader: another_user) if can_follow?(another_user)
      end

      def follows?(another_user)
        following_relationships.map(&:leader).include?(another_user)
      end

      def can_follow?(another_user)
        !(self == another_user || self.follows?(another_user))
      end

    end

### Mailer

新增寄送邀請信的方法

app/mailers/app_mailer.rb:

    :::ruby
    class AppMailer < ActionMailer::Base
      default from: ENV['MYFLIX_SMTP_USER_NAME']

      ... 省略程式碼 ...

      def send_invitation_email(invitation)
        @invitation = invitation
        mail(to: @invitation.recipient_email, subject: "Invitation to join MyFlix!")
      end

    end

信件內容如下

app/views/app_mailer/send_invitation_email.html.haml:

    :::haml
    !!! 5
    %html(lang="en-US")
      %body
        %p You are invited by #{@invitation.inviter.full_name} to join MyFlix!
        %p #{@invitation.message}
        %p= link_to "Accept this invitation", sign_up_with_invitation_token_url(@invitation.token)

