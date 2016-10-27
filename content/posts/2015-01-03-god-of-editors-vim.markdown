Title: 編輯器: Vim
Date: 2015-01-03
Tags: vim
Category: Misc

在編程領域中，
[編輯器之戰](http://zh.wikipedia.org/wiki/%E7%BC%96%E8%BE%91%E5%99%A8%E4%B9%8B%E6%88%98)的兩位主角
[Vi](http://zh.wikipedia.org/wiki/Vi) 和
[Emacs](http://zh.wikipedia.org/wiki/Emacs) 經歷幾十年的歲月後，
直到現在依然擁有許多信徒;
而隨著時間的過去，
Vi (Visual，[Bill Joy](http://zh.wikipedia.org/wiki/%E6%AF%94%E5%B0%94%C2%B7%E4%B9%94%E4%BC%8A) 於 1976 年發表 ) 的功能不斷地被增強，
最後演化出目前受歡迎的 [Vim](http://zh.wikipedia.org/wiki/Vim);
Vim 不管是可擴展性或高效的編輯速度，
都讓一般的編輯器難以望其項背，
也因此有了[編輯器之神](http://os.51cto.com/art/201101/242518.htm)的封號!
不過 GNU 計劃的創始人
[RMS](http://zh.wikipedia.org/wiki/%E7%90%86%E6%9F%A5%E5%BE%B7%C2%B7%E6%96%AF%E6%89%98%E6%9B%BC)
說它比較像魔鬼的編輯器
(因為 vi-vi-vi 是[獸名數目](http://zh.wikipedia.org/wiki/%E7%8D%B8%E5%90%8D%E6%95%B8%E7%9B%AE) XD )

關於 Vim 的詳細使用方法請查詢[官方文件](http://vimdoc.sourceforge.net/htmldoc/usr_toc.html)，
這裡只介紹我自己常用的一些操作。

### 環境設定

* ~/.vimrc 環境設定檔
* ~/.vim  Vim 專屬的資料夾

### 符號定義

為方便之後的說明，先在此定義兩個按鍵符號

* `C` 表示 Ctrl
* `M` 表示 Alt

### 常用模式

* command mode 按 `Esc`
* insert mode 在 command mode 中，按 `i` 或 `a`
* plain visual mode 在 command mode 中，按 `v`
* block visual mode 在 command mode 中，按 `C`+ `v`
* command line 在 command mode 中，按 `:`

### 存取檔案

- `vi file_name` 開啟檔案
- `:w` 存檔
- `:q` 離開
- `:q!` 強制離開(不須先存檔)
- `:e file_name` 編輯其它檔案

### 字元操作

- `i` 在游標所在處開始輸入
- `a` 從下個字元開始輸入
- `x` 刪除一個字元
- `o` 插入空白行並開始輸入

### 字元操作

- `d` `w` 刪除一個單字
- `d` `W` 刪除一個單字(忽略特殊字元)

### 拷貝和貼上

- `yy` 拷貝游標所在的那一行
- `3` `yy` 拷貝連續三行
- `dd` 剪下游標所在的那一行
- `3` `dd` 剪下連續三行
- `y` 將標記區域 yank 到剪貼簿
- `p` 將剪貼簿的資料貼上

### 段落操作

- `J` 連接下一行
- `d` `$` 從游標所在刪除到本行結尾
- `d` `^` 從游標所在刪除到本行開頭
- `D` 從游標所在刪除到本行結尾

### 暫存區操作

- `ma` `"c` `y` `'a` 將選擇區段拷貝到 register c
- `"c` `p` 將 register c 的資料貼上
- `ma` `"+` `y` `'a` 選擇區塊並拷貝到系統的剪貼板
- `3` `"+` `yy` 將連續三行 yank 到系統的剪貼板
- `:%y+` 將檔案內容 yank 到剪貼板

### 移動游標

- `gg` 第一行開頭
- `G` 最後一行的開頭
- `^` 移到游標所在行的開頭
- `$` 移到游標所在行的結尾
- `C`+`f` 下一頁
- `C`+`b` 上一頁
- `M`+`f` 往後移到一個單字
- `M`+`b` 往前移到一個單字
- `M`+`F` 往後移到一個單字並且標記
- `M`+`b` 往前移到一個單字並且標記

### 切換目錄

- `:cd %:h` 將工作目錄改變到編輯的檔案下
- `:lcd %:h` 僅將目前視窗的工作目錄改變到編輯的檔案下
- `autocmd BufEnter * silent! lcd %:p:h` 自動改變工作目錄到編輯的檔案下

### 切換檔案

- `gf` 跳到關聯檔 ( goto file )
- `C`+`^` 回到上一個檔案

### 分頁操作

- `:tab_new` 新分頁
- `:tabprevious` 上一個分頁
- `:tabnext` 下一個分頁
- `:ab tn tab_new` 將 tab_new 縮寫為 tn

### 視窗操作

- `:vs`       垂直分割
- `:sp`       水平分割
- `C`+`w` `v` 垂直分割
- `C`+`w` `s` 水平分割

- `C`+`w` `left[right] arrow` 左[右]切換視窗
- `C`+`w` `up[down] arrow`    上[下]切換視窗
- `C`+`w` `h[l]` 左[右]切換視窗
- `C`+`w` `k[j]` 上[下]切換視窗

### 其他操作

- `u`: 回到上一步
- `C`+`r`: 回到下一步

- `:set nu` 顯示行數
- `:set nonu` 不顯示行數
- `:syntax enable` 語法顏色
- `:set ai` 自動縮行

- `:!外部命令` 執行外部命令，例如 `:!ls`

- `C`+`r` `%` 在 insert mode 下貼上檔案路徑

### 自定按鍵

- `map <C-k> :tabprevious <CR>` 用 `C`+`k` 映射 `:tabpreview`
- `map <C-j> :tabnext <CR>` 用 `C`+`j` 映射 `:tabnext`

### 好用的 plugins

[rails.vim](http://www.vim.org/scripts/script.php?script_id=1567):
Rails 套件(語法顏色，快速切換檔案... 等)

* `:Rcd 目錄` 切換目錄(從專案目錄出發)

* `:Rmodel 檔案`      編輯 model 檔案

* `:Rview 檔案`       編輯 view 檔案

* `:Rcontroller 檔案` 編輯 controller 檔案

[snipMate](http://www.vim.org/scripts/script.php?script_id=2540): 加入程式片段

* `Tab` 加入程式片段

[ctrp](https://github.com/kien/ctrlp.vim): 模糊搜尋

* `C`+`p` 啟動模糊搜尋

[fencview.vim](http://www.vim.org/scripts/script.php?script_id=1708): 自動偵測多國編碼

* `:FencAutoDetect` 啟動偵測

[nerdtree.vim](http://www.vim.org/scripts/script.php?script_id=1658): 檔案瀏覽器

* `:e .` 瀏覽工作目錄

[supertab.vmb](http://www.vim.org/scripts/script.php?script_id=1643): 補全程式碼

* `Tab` 補全程式碼

雖然 Vim 對初學者而言需要投入多一些的時間來熟悉，
但只要上手後， 就會大幅提升你的編程效率。
