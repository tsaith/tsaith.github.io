Title: Homebrew: Mac 專屬的套件管理者
Date: 2014-10-28
Tags: utils
Category: Misc


每一位軟體開發者肯定都需要安裝許多套件來打造所需的開發環境，
而各種套件的版本和相依性一直以來都是件讓人頭痛的問題;
為了讓 Mac 使用者不再總是為此煩惱， 
於是有了 [Homebrew](http://brew.sh/) 的產生。

### 安裝方式

使用 `ruby` and `curl` 進行安裝
```
ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go/install)"
```

然後接著執行 `brew doctor` 來檢查系統是否一切正常
```
brew doctor
```

如果一切順利，我們就可以開始使用 Homebrew 來進行之後的套件管理。

### 基本使用方法

如果要搜尋套件，請執行
```
brew search 套件的部分名稱
```

若想查詢套件資訊，則執行
```
brew info 套件名稱
```

使用 `install` 來安裝套件
```
brew install 套件名稱
```

使用 `uninstall` 來移除套件
```
brew uninstall 套件名稱
```

倘若想更新 Homebrew，請執行
```
brew update
```

如果需要更多相關資訊，可以參考[這裡](https://github.com/Homebrew/homebrew/tree/master/share/doc/homebrew)。
