Title: 從 rvm 遷移到 rbenv
Date: 2015-01-03
Tags: utils
Category: Web


之前一直使用 rvm 來管理 ruby 的版本切換，
但因為 rvm 還提供了 gem 的安裝，
而這部分與 bundler 的職務重疊，
於是我決定採用功能更單純的 [rbev](https://github.com/sstephenson/rbenv) 專職 ruby 版本的管理。

### 移除 rvm

先執行
```plain
$ rvm implode
Are you SURE you wish for rvm to implode?
This will recursively remove /Users/tsaith/.rvm and other rvm traces?
(anything other than 'yes' will cancel) > yes
```
然後再移除使用者目錄下的 .bashrc、.bash_profile、.profile 以及 .zshrc 裡面的這一行
```
PATH=$PATH:$HOME/.rvm/bin # Add RVM to PATH for scripting
```

### 安裝 rbenv

執行 `exec $SHELL -l` 以重新啟動 shell 環境

加入 `rbenv init -` 到 shell 以使用 [shims](https://github.com/sstephenson/rbenv#understanding-shims) 和自動完成命令的功能
```
echo 'eval "$(rbenv init -)"' >> ~/.bash_profile
source ~/.bash_profile
```

接著使用 Homebrew 安裝套件
```
brew update
brew install rbenv
brew install rbenv-gem-rehash
brew install ruby-build
```

### 安裝 ruby

先查詢有哪些版本的 ruby 可供安裝
```
rbenv install -l
```

接著安裝指定的套件，下面以 ruby 2.1.5 的版本為例
```
rbenv install 2.1.5
```

假設在安裝 ruby 時遇到下面的錯誤訊息
```
BUILD FAILED (OS X 10.9.5 using ruby-build 20141225)

Inspect or clean up the working tree at /var/folders/2v/wtshnx5x4294fvlxyrk9t8kh0000gn/T/ruby-build.20150111114536.6196
Results logged to /var/folders/2v/wtshnx5x4294fvlxyrk9t8kh0000gn/T/ruby-build.20150111114536.6196.log

Last 10 log lines:
checking whether we are using the GNU C compiler... yes
checking whether gcc accepts -g... yes
checking for gcc option to accept ISO C89... none needed
checking whether we are using the GNU C++ compiler... yes
checking whether g++ accepts -g... yes
checking how to run the C preprocessor... g++
configure: error: in `/var/folders/2v/wtshnx5x4294fvlxyrk9t8kh0000gn/T/ruby-build.20150111114536.6196/ruby-2.2.0':
configure: error: C preprocessor "g++" fails sanity check
See `config.log' for more details
make: *** No targets specified and no makefile found.  Stop.
```
執行 `xcode-select --install` 更新 Xcode;
若在 Maverick 10.9.x 上遇到 `Can't install the software because it is not currently available from the Software Update server.`
這樣的錯誤訊息，可以直接到 [Apple Developer](https://developer.apple.com/downloads/index.action?name=Command%20Line%20Tools) 下載。
