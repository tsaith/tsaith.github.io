Title: 使用單一抽象層撰寫測試
Date: 2014-12-23
Tags: rails, testing
Category: Web


當撰寫測試時，使用單一抽象層的技巧可以讓程式更容易閱讀，
也避免開發者必須將思維在不同抽象層級中切換。


假設我們使用 [Capybara](https://github.com/jnicklas/capybara)
來測試網站的登入流程

```ruby
require 'spec_helper'

feature "User signs in" do

  scenario "with valid email and password" do

    alice = Fabricate(:user)

    # 使用者登入
    visit sign_in_path
    fill_in 'Email', :with => alice.email
    fill_in 'Password', :with => alice.password
    click_button 'Sign in'

    expect(page).to have_content alice.full_name
  end

end
```

在上述的範例中，開發者必須將思緒切換到底層考慮
Capybara 該如何處理欄位的填寫和按鈕，
然後再回到更高階層以預期使用者名稱將會出現在新的頁面。

但我們可以將底層的細節封裝起來，
讓每個步驟儘可能位於同一個抽象層面

```ruby

feature "User signs in" do

  scenario "with valid email and password" do
    alice = Fabricate(:user)

    # 使用者登入
    sign_in(alice)

    expect(page).to have_content alice.full_name
  end

  def sign_in(user)
    visit sign_in_path
    fill_in 'Email', :with => user.email
    fill_in 'Password', :with => user.password
    click_button 'Sign in'
  end

end
```

如此一來，開發者在閱讀程式時，就更能專注於思考整體的邏輯，
程式碼所顯示的內聚性也大幅提升;
更多的相關討論可參考[這裡](http://robots.thoughtbot.com/acceptance-tests-at-a-single-level-of-abstraction)。
