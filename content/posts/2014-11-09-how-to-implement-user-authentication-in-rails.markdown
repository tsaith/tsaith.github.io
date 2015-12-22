Title: 在 Rails 實作驗證機制
Date: 2014-11-09
Tags: rails
Category: Web


在網路應用中，使用者驗證是一項常見的重要功能，
雖然使用現成的 gem
(例如 [Devise](https://github.com/plataformatec/devise))，
可以快速實現出功能原型，但是卻會因為對套件內部架構的不熟悉，
而無法輕易修改或擴充新功能;
所以，這裡將敘述如何單純地使用 Rails 的內建功能來實作驗證機制，
希望讓讀者對其中的工作原理有透徹的認識。

### 安裝 `bcrypt-ruby`

為了支援密碼驗證，我們先在 Gemfile 中加入
```
gem 'bcrypt-ruby', '3.0.1'
```
然後執行 bundle 進行套件安裝。

### 設定資料庫

假設我們的使用者資料表名稱為 users，
先在 users 中新增一個 password_digest 的字串欄位，
然後在 db/schema 確認如下
```ruby
  create_table "users", force: true do |t|
    t.string   "username"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.string   "password_digest"
  end
```

### 設定 routes

在 config/routes.rb 中加入 login 和 logout 的路徑，如下
```ruby
  get 'login', to: 'sessions#new'
  post 'login', to: 'sessions#create'
  get 'logout', to: 'sessions#destroy'
```

### 設定 model

編輯 User model，加入 `has_secure_password` 來提供密碼驗證的功能;
在這裡，我關掉 `has_secure_password` 預設的驗證機制，然後再手動地指定
使用者名稱和密碼的驗證，以確定所有行為都在我們的掌握中。

    :::ruby
    class User < ActiveRecord::Base
      has_secure_password validations: false
      validates :username, presence: true, uniqueness: true
      validates :password, presence: true, on: :create, length: {minimum: 5}
    end

### 設定 view

新增 app/views/sessions/new.html.erb ，內容如下
{% codeblock app/views/sessions/new.html.erb %}

    :::ruby
    <%= render 'shared/content_title', title: 'Please log in' %>

    <div class='well'>
      <%= form_tag '/login' do %>
        <div class='control-group'>
          <%= label_tag :username %>
          <%= text_field_tag :username, params[:username] || '' %>
        </div>
        <div>
          <%= label_tag :password %>
          <%= password_field_tag :password, params[:password] || '' %>
        </div>
        <%= submit_tag "Login", class: 'btn btn-success' %>
      <% end %>
    </div>

在這個登入表單中，使用者被要求輸入 username 和 password。

### 設定 controller

新增 app/controllers/sessions_controller.rb，內容如下

    :::ruby
    class SessionsController < ApplicationController

      def new
      end

      def create
        user = User.find_by(username: params[:username])

        if user && user.authenticate(params[:password])
          session[:user_id] = user.id
          flash[:notice] = "Your've logged in!"
          redirect_to root_path
        else
          flash[:error] = "There's something wrong with username or password"
          redirect_to register_path
        end
      end

      def destroy
        session[:user_id] = nil
        flash[:notice] = "You've logged out!"
        redirect_to root_path
      end

    end

在 create 中，
我們使用 `user.authenticate(params[:password])` 來驗證使用者密碼是否正確，
如果是，再透過 `session[:user_id]` 來貯存 user id;
而在 destroy 裡面，
則使用 `session[:user_id] = nil` 來清除 user id。

最後，我們可以在 app/controllers/application_controller.rb
加入三個常用的方法，方便隨時調用。

    :::ruby
    class ApplicationController < ActionController::Base
      # Prevent CSRF attacks by raising an exception.
      # For APIs, you may want to use :null_session instead.
      protect_from_forgery with: :exception

      helper_method :current_user, :logged_in?

      def current_user
        @current_user ||= User.find(session[:user_id]) if session[:user_id]
      end

      def logged_in?
        !!current_user
      end

      def require_user
        unless logged_in?
          flash[:error] = "Must be logged in to do that"
          redirect_to root_path
        end
      end

    end

- `current_user`: 回傳目前的使用者
- `logged_in?`: 是否已登入?
- `require_user`: 檢查是否已登入，如果沒有登入，則導向根路徑

倘若一切順利，我們已經從無到有實作了使用者驗證機制，
並可以此為基礎加入更多進階的功能。
