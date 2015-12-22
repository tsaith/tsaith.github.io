Title: 在 RSpec 中使用 Macros
Date: 2014-12-22
Tags: rails
Category: Web


撰寫測試時，常常會遇到不同地方需要做相同或類似的事，
這時候可以考慮將共用的邏輯抽出並寫成 macros，
避免讓相同的程式區塊散佈於各處，
以方便閱讀和日後的維護。

假設我們有份程式用來測試使用者的登入流程，如下

```ruby
require 'spec_helper'

feature "User signs in" do

  scenario "with valid email and password" do
    alice = Fabricate(:user)

    visit sign_in_path
    fill_in 'Email', :with => alice.email
    fill_in 'Password', :with => alice.password
    click_button 'Sign in'

    expect(page).to have_content alice.full_name
  end

end
```

中間部分的程式碼敘述了使用者的登入步驟;
這時候我們可以將此處抽出並在 spec/support/macros.rb
裡面定義一個新函數 sign_in

```ruby
def sign_in(a_user = nil)
  user = a_user || Fabricate(:user)
  visit sign_in_path
  fill_in 'Email', :with => user.email
  fill_in 'Password', :with => user.password
  click_button 'Sign in'
end
```

然後將原先的測試程式改寫如下

```ruby
require 'spec_helper'

feature "User signs in" do

  scenario "with valid email and password" do
    alice = Fabricate(:user)
    sign_in(alice)
    expect(page).to have_content alice.full_name
  end

end
```

除了程式碼的可讀性明顯提升之外，
日後編寫其他測試時若牽涉到使用者登入，
也只要簡單地引用 sign_in 這個 macro 即可。
