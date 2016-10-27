Title: 使用 RSpec 寫 Feature Tests
Date: 2014-12-07
Tags: rails, testing
Category: Web


在開發 Rails 專案時，我們可使用 Feature Tests
來模擬使用者在應用程式中的操作流程;
這裡將介紹如何使用 [RSpec](https://github.com/rspec/rspec-rails)
搭配 [Capybara](https://github.com/jnicklas/capybara)
來撰寫這方面的測試。

### 安裝套件

在 Gemfile 加入 `gem 'capybara'`
然後執行 `bundle` 安裝 Capybara。

假使安裝套件時遇到 'An error occurred while installing nokogiri' 這樣的錯誤訊息

```
Gem::Ext::BuildError: ERROR: Failed to build gem native extension.

    /Users/tsaith/.rvm/rubies/ruby-2.1.1/bin/ruby -r ./siteconf20141220-15553-1vqn6mc.rb extconf.rb
checking if the C compiler accepts ... yes
checking if the C compiler accepts -Wno-error=unused-command-line-argument-hard-error-in-future... no
Building nokogiri using packaged libraries.
checking for iconv... yes
************************************************************************
IMPORTANT NOTICE:

Buidling Nokogiri with a packaged version of libxml2-2.9.2
with the following patches applied:
    - 0001-Revert-Missing-initialization-for-the-catalog-module.patch
    - 0002-Fix-missing-entities-after-CVE-2014-3660-fix.patch

Team Nokogiri will keep on doing their best to provide security
updates in a timely manner, but if this is a concern for you and want
to use the system library instead; abort this installation process and
reinstall nokogiri as follows:

    gem install nokogiri -- --use-system-libraries
        [--with-xml2-config=/path/to/xml2-config]
        [--with-xslt-config=/path/to/xslt-config]

If you are using Bundler, tell it to use the option:

    bundle config build.nokogiri --use-system-libraries
    bundle install

Note, however, that nokogiri is not fully compatible with arbitrary
versions of libxml2 provided by OS/package vendors.
************************************************************************
Extracting libxml2-2.9.2.tar.gz into tmp/x86_64-apple-darwin12.5.0/ports/libxml2/2.9.2... OK
Running patch with /Users/tsaith/.rvm/gems/ruby-2.1.1@myflix/gems/nokogiri-1.6.5/ports/patches/libxml2/0001-Revert-Missing-initialization-for-the-catalog-module.patch...
Running 'patch' for libxml2 2.9.2... OK
Running patch with /Users/tsaith/.rvm/gems/ruby-2.1.1@myflix/gems/nokogiri-1.6.5/ports/patches/libxml2/0002-Fix-missing-entities-after-CVE-2014-3660-fix.patch...
Running 'patch' for libxml2 2.9.2... OK
Running 'configure' for libxml2 2.9.2... ERROR, review '/Users/tsaith/.rvm/gems/ruby-2.1.1@myflix/gems/nokogiri-1.6.5/ext/nokogiri/tmp/x86_64-apple-darwin12.5.0/ports/libxml2/2.9.2/configure.log' to see what happened.
*** extconf.rb failed ***
Could not create Makefile due to some reason, probably lack of necessary
libraries and/or headers.  Check the mkmf.log file for more details.  You may
need configuration options.

Provided configuration options:
    --with-opt-dir
    --without-opt-dir
    --with-opt-include
    --without-opt-include=${opt-dir}/include
    --with-opt-lib
    --without-opt-lib=${opt-dir}/lib
    --with-make-prog
    --without-make-prog
    --srcdir=.
    --curdir
    --ruby=/Users/tsaith/.rvm/rubies/ruby-2.1.1/bin/ruby
    --help
    --clean
    --use-system-libraries
    --enable-static
    --disable-static
    --with-zlib-dir
    --without-zlib-dir
    --with-zlib-include
    --without-zlib-include=${zlib-dir}/include
    --with-zlib-lib
    --without-zlib-lib=${zlib-dir}/lib
    --enable-cross-build
    --disable-cross-build
/Users/tsaith/.rvm/gems/ruby-2.1.1@myflix/gems/mini_portile-0.6.1/lib/mini_portile.rb:279:in `block in execute': Failed to complete configure task (RuntimeError)
    from /Users/tsaith/.rvm/gems/ruby-2.1.1@myflix/gems/mini_portile-0.6.1/lib/mini_portile.rb:271:in `chdir'
    from /Users/tsaith/.rvm/gems/ruby-2.1.1@myflix/gems/mini_portile-0.6.1/lib/mini_portile.rb:271:in `execute'
    from /Users/tsaith/.rvm/gems/ruby-2.1.1@myflix/gems/mini_portile-0.6.1/lib/mini_portile.rb:66:in `configure'
    from /Users/tsaith/.rvm/gems/ruby-2.1.1@myflix/gems/mini_portile-0.6.1/lib/mini_portile.rb:109:in `cook'
    from extconf.rb:268:in `block in process_recipe'
    from extconf.rb:167:in `tap'
    from extconf.rb:167:in `process_recipe'
    from extconf.rb:455:in `<main>'

extconf failed, exit code 1

Gem files will remain installed in /Users/tsaith/.rvm/gems/ruby-2.1.1@myflix/gems/nokogiri-1.6.5 for inspection.
Results logged to /Users/tsaith/.rvm/gems/ruby-2.1.1@myflix/extensions/x86_64-darwin-12/2.1.0-static/nokogiri-1.6.5/gem_make.out
An error occurred while installing nokogiri (1.6.5), and Bundler cannot continue.
Make sure that `gem install nokogiri -v '1.6.5'` succeeds before bundling.
```

可以試著指定系統內建的函式庫來安裝 Nokogiri
```
bundle config build.nokogiri --use-system-libraries
```
然後再執行一次 `bundle`。

### 設定 spec_helper.rb

在 spec/spec_helper.rb 裡面加入 `require 'capybara/rails'`

```ruby
# This file is copied to spec/ when you run 'rails generate rspec:install'
ENV["RAILS_ENV"] ||= 'test'
require File.expand_path("../../config/environment", __FILE__)
require 'rspec/rails'
require 'capybara/rails'
```

### 編寫測試

假設我們現在想要模擬使用者的登入流程，
請新增檔案 spec/features/user_signs_in_spec.rb
並加入內容如下

```ruby
require 'spec_helper'

feature "User signs in" do

  scenario "with valid email and password" do
    alice = Fabricate(:user)                     # 宣告使用者
    visit sign_in_path                           # 訪問登入網頁
    fill_in 'Email', :with => alice.email        # 填寫 Email
    fill_in 'Password', :with => alice.password  # 填寫 Password
    click_button 'Sign in'                       # 按下 Sign in 按鈕
    expect(page).to have_content alice.full_name # 預期網頁的內容會出現使用者的名字
  end

end
```

上面的 `feature` 和 `scenario` 其意義等同於
RSpec 中的 `describe ..., :type => :feature` 和 `it`;
[Relish](https://www.relishapp.com/rspec/rspec-rails/docs/feature-specs/feature-spec) 提供了豐富的語法介紹。

最後，執行 `rspec` 即可看到測試結果。
