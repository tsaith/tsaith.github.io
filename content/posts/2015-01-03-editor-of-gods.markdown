Title: 編輯器: Emacs
Date: 2015-01-03
Tags: emacs
Category: Misc

GNU 計劃創始人 [Richard Stallman](http://zh.wikipedia.org/wiki/%E7%90%86%E6%9F%A5%E5%BE%B7%C2%B7%E6%96%AF%E6%89%98%E6%9B%BC) 和 [Guy Lewis Steele Jr.](http://zh.wikipedia.org/wiki/%E8%93%8B%E4%BC%8A%C2%B7%E5%8F%B2%E6%8F%90%E7%88%BE%E4%BA%8C%E4%B8%96) 在1975 年共同打造了 [Emacs](http://zh.wikipedia.org/wiki/Emacs) (Editor MACroS)，
Emacs 使用 [Lisp](http://zh.wikipedia.org/wiki/LISP) 作為功能擴充語言，
具有強大的擴展性，與可客製性，
還有各式各樣好用的套件，
所以也有人稱它是神的編輯器，或是偽裝成編輯器的作業系統 @_@;
如果想知道更多對於 Emcas 特性的敘述，
可以參考另一篇[文章](http://blog.csdn.net/redguardtoo/article/details/7222501#sec-13)。

### 安裝 Emacs

在 Mac 下可透過 Homebrew 進行安裝
```plain
brew install emacs
```

### 建議配置

Emacs 的目錄位於 ~/.emacs.d，
若希望自定個人的專屬配置，可在 ~/.emacs.d/init.el 裡面設定。

建議一開始可直接使用高手們的配置，
因為他們的配置都經過了多年的磨練，
在深思熟慮後才決定出最佳的按鍵定義並也解決了許多套件相容性問題;
我個人偏好 [Steve Purcell](http://www.sanityinc.com/) 的[配置](https://github.com/purcell/emacs.d)，
因為他是一位頂尖的 Rails 開發者，
所以使用他的配置可以大量減少自己打造 Rails 開發環境的時間。

### 符號與按鍵

為方便之後的說明，在這邊先定義一些符號和按鍵的對應關係

* `C`: 代表 Ctrl
* `M`: 代表 Alt
* `Ret`: 代表 Return

### 安裝 Packages

在 Emacs 最簡單安裝套件的兩個方式分別為

使用 package-install 命令

* `M`-`x` package-install `Ret` Package Name `Ret` : 安裝套件

透過 [Package Menu](https://www.gnu.org/software/emacs/manual/html_node/emacs/Package-Menu.html#Package-Menu)

* `M`-`x` list-packages : 進入套件安裝目錄
* `C`-`s`: 尋找套件名稱
* `i`: 標記為即將安裝的套件
* `u`: 解除標記
* `d`: 標記為刪除的套件
* `x`: 開始安裝/反安裝 以標記的套件
* `r`: 刷新列表

### 基本操作

* `C`-`x` `C`-`c`: 離開 Emacs
* `C`-`z`: 暫停 Emcas，並將它放到背景
* `C`-`h` `C`-`h`: Help for Help

### 存取檔案

* `C`-`x` `C`-`f`: 尋找檔案並開啟
* `C`-`x` `C`-`s`: 存檔

### 字元操作

* `C`-`d`: 向前刪除字元
* `Del`: 向後刪除字元

### 拷貝和貼上

* `M`-`w`: 拷貝游標所在行
* `C`-`u` `3` `M`-`w`: 拷貝連續三行
* `C`-`w`: 剪下游標所在行
* `C`-`u` `3` `C`-`w`: 剪下連續三行
* `C`-`y`: 貼上暫存區資料

### 暫存區操作

* `C`-`x` `r` `s` (#): 拷貝標記區域到數字暫存區
* `C`-`x` `r` `i` (#): 從數字暫存區將資料插入游標所在處

### Buffer 操作

* `C`-`x` `b`: 切換 buffer
* `C`-`x` `Left`: 切換到上一個 buffer
* `C`-`x` `Right`: 切換到下一個 buffer

### 區段操作

* `C`-`Space`: 開始標記區域
* `C`-`k`: 從游標所在刪除到本行結尾
* `M`-`0` `C`-`k`: 從游標所在刪除到本行開頭
* `C`-`x` `h`: 標記整個檔案內容

### 視窗操作

* `C`-`x` 1: 單一視窗
* `C`-`x` 2: 水平分割
* `C`-`x` 3: 垂直分割
* `C`-`x` 0: 關閉選擇的視窗
* `M`-`x` windmove-up: 向上切換視窗
* `M`-`x` windmove-down: 向下切換視窗
* `M`-`x` windmove-left: 向左切換視窗
* `M`-`x` windmove-right: 向右切換視窗

### 移動游標

* `C`-`a`: 移到游標所在行的開頭
* `C`-`e`: 移到游標所在行的結尾
* `M`-`a`: 移到段落開頭
* `M`-`e`: 移到段落結尾
* `M`-`g` `g`: 移到指定行數
* `Esc` `<`: 移到檔案開頭
* `Esc` `>`: 移到檔案結尾
* `C`-`v`: 移到下一頁
* `M`-`v`: 移到上一頁
* `C`-`x` `r` `Space` `a`: 記錄目前游標位置到 register a
* `C`-`x` `r` `j` `a`: 跳到 register a 所儲存的位置

### 字串取代

* `M`-`%` old_string `Ret` new_string `Ret`: 取代字串
* `M`-`x` replace-regexp `Ret` regexp `Ret` newstring `Ret`: 以正規表示法取代字串

### 程式碼操作

* `M`-`;`: 將程式碼加上註解符號
* `C`-`u` `M`-`;`: 移除程式碼前的註解符號
* `Tab`: 縮行對齊
* `M`-`x` linum-mode: 開啟/關閉 行號顯示

### 其他操作

* `C`-`_`: 回到上一步
* `M`-`_`: 回到下一步
* `C`-`g`: 取消目前操作
* `C`-`x` `z`: 重複上一次的操作
* `M`-`!`: 執行外部命令

### 好用的 Packages

[Dired](http://www.gnu.org/software/emacs/manual/html_node/emacs/Dired.html): 檔案管理

* `C`-`x` `d` 開啟目錄
* `c` 拷貝檔案
* `r` 將檔案重新命名
* `d` 刪除檔案
* `+` 新增目錄
* `z` 使用 gzip 進行壓縮/解壓縮
* `m` 標記檔案
* `u` 反標記檔案
* `U` 取消所有標記
* `g` 刷新列表
* `^` 到上一層目錄

[osx-cliboard](https://github.com/joddie/osx-clipboard-mode): 使用 OSX 的剪貼板

* `M`-`x` osx-clipboard-mode: 進入 osx-clipboard-mode

[Eshell](http://www.gnu.org/software/emacs/manual/html_mono/eshell.html): Emacs Shell

* `M`-`x` eshell: 啟動 eshell

[Rinari](https://github.com/eschulte/rinari/tree/master): Rails 的開發環境

* `C`-`c` `;` `f` `m` 尋找 model
* `C`-`c` `;` `f` `v` 尋找 view
* `C`-`c` `;` `f` `c` 尋找 controller
* `C`-`c` `;` `f` `r` 尋找 rspec
* `C`-`c` `;` `f` `M` 尋找 mailer
* `C`-`c` `;` `f` `i` 尋找 migration
* `C`-`c` `;` `f` `l` 尋找 lib
* `C`-`c` `;` `f` `j` 尋找 javascript
* `C`-`c` `;` `f` `o` 尋找 log
* `C`-`c` `;` `c` 啟動 console
* `C`-`c` `;` `w` 啟動 web-server
