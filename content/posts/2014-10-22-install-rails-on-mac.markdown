Title: 在 Mac 上安裝 Rails
Date: 2014-10-22
Tags: rails
Category: Web


系統環境: OSX 10.9.x

這篇筆記僅記錄了本人安裝 Rails 的步驟，若需要更詳細的說明，請參考 [Install Rails](http://installrails.com)。

* 首先開啟 App Store 搜尋並安裝 Xcode (下載通常需要等候一段時間)

* 接著使用終端機安裝 Homebrew

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

* 然後檢查安裝是否成功

```
brew doctor
```

* 安裝 Git

```
brew install git
```
- 設定使用者姓名和郵件地址
```
git config --global user.name "你/妳的姓名"
git config --global user.email "郵件地址"
```

* 安裝 RVM
```
\curl -sSL https://get.rvm.io | bash
```

* 安裝 Ruby (這裡以版本 2.1.1 為範例)
```
rvm install 2.1.1
```

* 最後，開始安裝 Rails
```
gem install rails --no-ri --no-rdoc
```

若以上所有步驟都順利完成，那恭喜你/妳可以開始享受撰寫Rails的樂趣了。
