Title: 好用的 Debug 工具: Pry
Date: 2014-12-15
Tags: rails
Category: Web


開發 Rails 或 Ruby 應用時，我們可以使用 [pry](https://github.com/pry/pry) 和 [pry-nav](https://github.com/nixme/pry-nav) 來大幅提高 debug 效率。

### 安裝套件

在 Gemfile 中加入
```
group :development, :test do
  gem 'pry'
  gem 'pry-nav'
end
```

然後執行 `bundle`

### 使用方法


在想要 debug 的地方加入 binding.pry，如下

```ruby
class SessionsController < ApplicationController

  def new
    redirect_to home_path if current_user
  end

  def create
    user = User.where(email: params[:email]).first
    if user && user.authenticate(params[:password])
      session[:user_id] = user.id

      binding.pry # 設定中斷點

      flash[:notice] = "Your've signed in, enjoy!"
      redirect_to home_path
    else
      flash[:error] = "Invalid email or password."
      redirect_to sign_in_path
    end
  end

  def destroy
    session[:user_id] = nil
    redirect_to home_path, notice: "You are signed out!"
  end

end
```

當 server 執行到 binding.pry 所在的地方，
將會暫停並且進入互動模式，這時後就可以開始進行偵錯

```ruby
From: /Users/tsaith/projects/myflix/app/controllers/sessions_controller.rb @ line 11 SessionsController#create:

     7: def create
     8:   user = User.where(email: params[:email]).first
     9:   if user && user.authenticate(params[:password])
    10:     session[:user_id] = user.id
 => 11:     binding.pry
    12:     flash[:notice] = "Your've signed in, enjoy!"
    13:     redirect_to home_path
    14:   else
    15:     flash[:error] = "Invalid email or password."
    16:     redirect_to sign_in_path
    17:   end
    18: end

[1] pry(#<SessionsController>)> params
=> {"utf8"=>"✓",
 "authenticity_token"=>"Is1jphXlmnK8fRfJT2YdJqMcBFTNxuzn1bIum1o9D3U=",
 "email"=>"user@gmail.com",
 "password"=>"user_password",
 "commit"=>"Sign in",
 "controller"=>"sessions",
 "action"=>"create"}
[2] pry(#<SessionsController>)> user.id
=> 1
[3] pry(#<SessionsController>)> next

From: /Users/tsaith/projects/myflix/app/controllers/sessions_controller.rb @ line 12 SessionsController#create:

     7: def create
     8:   user = User.where(email: params[:email]).first
     9:   if user && user.authenticate(params[:password])
    10:     session[:user_id] = user.id
    11:     binding.pry
 => 12:     flash[:notice] = "Your've signed in, enjoy!"
    13:     redirect_to home_path
    14:   else
    15:     flash[:error] = "Invalid email or password."
    16:     redirect_to sign_in_path
    17:   end
    18: end
[1] pry(#<SessionsController>)>
```

倘若希望離開偵錯模式，請執行 `Ctrl` + `d`。


最後，如果想對常用的命令新增 alias 可以在 ~/.pryrc 裡面定義

```ruby
Pry.commands.alias_command 'c', 'continue'
Pry.commands.alias_command 's', 'step'
Pry.commands.alias_command 'n', 'next'
```
