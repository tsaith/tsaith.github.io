Title: 透過郵件允許使用者重設密碼
Date: 2014-12-31
Tags: rails
Category: Web


在許多網站的使用者登入頁面中，
通常會伴隨一個處理忘記密碼的連結，
點選後，將會寄出一封電子郵件讓使用者可以藉此重設個人密碼;
而這篇文章將介紹如何實做這項功能。

### 操作流程

讓我們先預覽一次整個操作流程，當訪問登入頁面時，
可以看到最下方有個 Forgot Password? 的連結

{% img https://farm9.staticflickr.com/8563/15549305854_4fc7a19b13_b.jpg %}

點選此連結後，會被導向新頁面，
在此可以寄送郵件到使用者的信箱

{% img https://farm9.staticflickr.com/8602/15985772059_f5beaccf89_b.jpg %}

按下寄信後，將顯示信件已寄出的提示

{% img  https://farm8.staticflickr.com/7524/15984997938_e127612ea6_b.jpg %}

接下來，使用者將會收到一封郵件，內含網頁連結，
點選後，將會被引導至變更密碼的頁面

{% img https://farm8.staticflickr.com/7466/16145868716_66b3c7b0db_b.jpg %}

最後，使用者可以在這個頁面中重新設定新的密碼

{% img  https://farm9.staticflickr.com/8575/15984342530_3d82f8865a_b.jpg %}

### Routes

新增以下 routes
config/routes.rb:

    :::ruby
    get 'forgot_password', to: 'forgot_passwords#new'
    resources :forgot_passwords, only: [:create]
    get 'forgot_password_confirmation', to: 'forgot_passwords#confirm'

    resources :password_resets, only: [:show, :create]

    get 'expired_token', to: 'password_resets#expired_token'

### Database

在 users table 裡面加入 token 欄位

db/schema.rb:

    :::ruby
    create_table "users", force: true do |t|
      t.string   "full_name"
      t.string   "email"
      t.string   "password_digest"
      t.string   "role"
      t.string   "slug"
      t.datetime "created_at"
      t.datetime "updated_at"
      t.string   "token"
    end

### Views

在登入頁面新增 Forgot Password? 連結

app/views/sessions/new.html.haml:

    :::haml
    %section.sign_in.container
      .row
        .col-sm-10.col-sm-offset-1
          = bootstrap_form_tag url: sign_in_path do |f|
            %header
              %h1 Sign in
            .row
              .col-sm-4
                = f.email_field :email, label: "Email Address", placeholder: 'user_name@example.com'
            .row
              .col-sm-4
                = f.password_field :password
            = f.submit "Sign in"
            = link_to "Forgot Password?", forgot_password_path # 加入這一行

新增寄信頁面

app/views/forgot_passwords/new.html.haml:

    :::haml
    %section.forgot_password.container
      .row
        .col-sm-10.col-bg-offset-1
          = bootstrap_form_tag url: forgot_passwords_path do |f|
            %header
              %h1 Forgot Password?
              %p We will send you an email with a link that you can use to reset your password.
            .row
              .col-sm-4
                = f.email_field :email, label: "Email Address"
            = f.submit "Send Email"

順便一提，這邊使用了 [rails-bootstrap-forms](https://github.com/bootstrap-ruby/rails-bootstrap-forms) 來快速建構具有
[twitter bootstrap-style](http://getbootstrap.com/) 的表格。


新增確認頁面

app/views/forgot_passwords/confirm.html.haml:

    :::haml
    %section.confirm_password_reset.container
      .row
        .col-sm-10.col-sm-offset-1
          %p We have sent an email with instruction to reset your password.

新增修改密碼頁面

app/views/password_resets/show.html.haml:

    :::haml
    %section.reset_password.container
      .row
        .col-sm-10.col-sm-offset-1
          = bootstrap_form_tag url: password_resets_path do |f|
            %header
              %h1 Reset Your Password
            .row
              .col-sm-4
                = f.password_field :password, label: "New Password"
                = f.hidden_field :token, value: @token
            = f.submit "Reset Password"

新增 token 已經過期的頁面

app/views/password_resets/expired_token.html.haml:

    :::haml
    %section.invalid_token.container
      .row
        .col-sm-10.col-sm-offset-1
          %p Your reset password link is expired.

### Controllers

新增 ForgotPasswordsController

app/controllers/forgot_passwords_controller.rb:

    :::ruby
    class ForgotPasswordsController < ApplicationController

      def new ; end

      def create
        user = User.where(email: params[:email]).first

        if user
          user.generate_token
          AppMailer.send_password_reset(user).deliver
          redirect_to forgot_password_confirmation_path
        else
          flash[:error] = params[:email].blank? ? "Email cannot be blank." : "There is no user with that email in the system."
          redirect_to forgot_password_path
        end

      end

      def confirm ; end

    end

新增 PasswordResetsController

app/controllers/password_resets_controller.rb:

    :::ruby
    class PasswordResetsController < ApplicationController

      def show
        user = User.where(token: params[:id]).first
        if user
          @token = params[:id]
        else
          redirect_to expired_token_path
        end
      end

      def create
        user = User.where(token: params[:token]).first
        if user
          user.password = params[:password]
          if user.save
            user.clear_token
            flash[:success] = "Your password has been changed. Please sign in."
          else
            flash[:error] = "Invalid new password. Password did not change."
          end
          redirect_to sign_in_path
        else
          redirect_to expired_token_path
        end
      end

      def expired_token ; end

    end

### Models

上面使用的 `generate_token` 和 `clear_token` methods
定義在 User class 裡面

app/models/user.rb:

    :::ruby
    class User < ActiveRecord::Base

      ... 其他程式碼 ...

      def generate_token
        self.update_column(:token, SecureRandom.urlsafe_base64)
      end

      def clear_token
        self.update_column(:token, nil)
      end

    end

### Mailer

在 development.rb 和 production.rb 裡面設定 :host 如下

config/environments/development.rb:

    :::ruby
    # Mailer host
    config.action_mailer.default_url_options = { :host => 'localhost:3000' }

config/environments/production.rb:

    :::ruby
    # Mailer host
    config.action_mailer.default_url_options = { :host => '你的主機' }

然後新增 AppMailer


app/mailers/app_mailer.rb:

    :::ruby
    class AppMailer < ActionMailer::Base
      default from: ENV['MYFLIX_SMTP_USER_NAME']

      def send_password_reset(user)
        @user = user
        mail(to: @user.email, subject: "Please reset your password")
      end

    end

MYFLIX_SMTP_USER_NAME 是我們自定的環境變數，
倘若不清楚如何使用環境變數來設定郵件的帳號或密碼，
可參考[這篇文章](/blog/2014/11/26/how-to-set-up-email-password-securely)。

最後，新增信件內容

app/views/app_mailer/send_password_reset.html.haml:

    :::haml
    !!! 5
    %html(lang="en-US")
      %body
        %p Please click on the link below to reset your password:
        %p= link_to "Reset My Password", password_reset_url(@user.token)
