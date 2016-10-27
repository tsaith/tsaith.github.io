Title: 使用 RSpec 撰寫 Functional Tests
Date: 2014-12-07
Tags: rails, testing
Category: Web


在開發 Rails 專案時，我們可以撰寫 Functional Tests 來測試
controller 的功能是否正常工作;
例如，如果想測試使用者的登入與登出，
就可以在 spec/controllers/ 下面新增一個檔案
sessions_controller_spec.rb，內容如下

```ruby
require "spec_helper"

describe SessionsController do

  let(:user) { Fabricate(:user) }

  describe "GET new" do
    it "redirects to the home page for authenticated users" do
      session[:user_id] = user.id
      get :new
      expect(response).to redirect_to home_path
    end
  end

  describe "POST create" do
    context "with valid credentials" do
      before do
        post :create, email: user.email, password: user.password
      end

      it "puts the signed in user in the session" do
        expect(session[:user_id]).to eq user.id
      end
      it "redirects to the home page" do
        expect(response).to redirect_to home_path
      end
      it "sets the notice" do
        expect(flash[:notice]).not_to be_blank
      end
    end

    context "with invalid credentials" do
      before do
        post :create, email: user.email, password: user.password + "sadsafds"
      end

      it "does not put the signed in user in the session" do
        expect(session[:user_id]).to be_nil
      end
      it "redirects to the sign in page" do
        expect(response).to redirect_to sign_in_path
      end
      it "sets the error message" do
        expect(flash[:error]).not_to be_blank
      end
    end
  end

  describe "GET destroy" do
    before do
      session[:user_id] = user.id
      get :destroy
    end

    it "clears the session for the user" do
      expect(session[:user_id]).to be_nil
    end
    it "redirects to the home page" do
      expect(response).to redirect_to home_path
    end
    it "sets the notice" do
      expect(flash[:notice]).not_to be_blank
    end
  end

end
```
在上面的範例中，我們測試了 new 和 create 以及 destroy
三個動作，並使用 [Fabrication](http://www.fabricationgem.org/) 來簡化產生 User 物件的過程;
其對應的程式碼則位於 spec/fabricators/
下面的 user_fabricator.rb

```ruby
Fabricator(:user) do
  email { Faker:: Internet.email }
  password { Faker::Internet.password }
  full_name { Faker::Name.name }
end
```

在 user fabricator 裡面，進一步使用了
[Faker](https://github.com/stympy/faker)
來自動產生 email 或 password 欄位的值。

編寫好程式後，執行 `rspec` 就能看到測試結果。
