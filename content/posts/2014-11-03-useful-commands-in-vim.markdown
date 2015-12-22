Title: Vim 的常用指令
Date: 2014-11-03
Tags: vim
Category: Misc


在編程領域中，
[編輯器之戰](http://zh.wikipedia.org/wiki/%E7%BC%96%E8%BE%91%E5%99%A8%E4%B9%8B%E6%88%98)的兩位主角 [Vi](http://zh.wikipedia.org/wiki/Vi) 和
[Emacs](http://zh.wikipedia.org/wiki/Emacs) 經歷幾十年的歲月後，
直到現在依然擁有許多信徒;
而隨著時間的過去，Vi 的功能不斷地被增強，最後演化出目前受歡迎的 [Vim](http://zh.wikipedia.org/wiki/Vim) ，
關於 Vim 的詳細手冊可查詢[官方文件](http://vimdoc.sourceforge.net/htmldoc/usr_toc.html)，這裡僅列出常用的一些指令。

### 環境設定

* ~/.vimrc: 環境設定檔
* ~/.vim: Vim 專屬的資料夾

### 內建指令

- `vi file_name` 開啟檔案
- `Ecs` 進入命令模式
- `:w` 存檔
- `:q` 離開
- `:q!` 強制離開(不須先存檔)
- `:e file_name` 編輯其它檔案
- `x` 刪除一個字元
- `i` 在游標所在處開始輸入文字
- `a` 從下個字元開始輸入文字
- `p` 將暫存區資料貼上
- `yy` 拷貝游標所在的那一行
- `3` `yy` 拷貝連續三行
- `dd` 剪下游標所在的那一行
- `3` `dd` 剪下連續三行
- `D` 刪除游標之後的部分
- `J` 連接下一行
- `:set nu` 顯示行數
- `:set nonu` 不顯示行數
- `ma` `"c` `y` `'a` 將選擇區段拷貝到 register c
- `"c` `p` 將 register c 的資料貼上
- `ma` `"+` `y` `'a` 選擇區塊並拷貝到系統的剪貼板
- `3` `"+` `yy` 將連續三行到系統的剪貼板
- `:set ai` 自動縮行
- `:tab_new` 新分頁
- `:ab tn tab_new` 將 tab_new 縮寫為 tn
- `:tabprevious` 上一個分頁
- `:tabnext` 下一個分頁
- `map <C-k> :tabprevious <CR>` 用 `Ctrl`+`k` 映射 `:tabpreview`
- `map <C-j> :tabnext <CR>` 用 `Ctrl`+`j` 映射 `:tabnext`
- `gg` 第一行開頭
- `G` 最後一行的開頭
- `:cd %:h` 將工作目錄改變到編輯的檔案下
- `:lcd %:h` 僅將目前視窗的工作目錄改變到編輯的檔案下
- `autocmd BufEnter * silent! lcd %:p:h` 自動改變工作目錄到編輯的檔案下
- `gf` 跳到關聯檔 ( goto file )
- `Ctrl`+`^` 回到上一個檔案
- `:!外部命令` 執行外部命令，例如 `:!ls`
- `:syntax enable` 語法顏色

### 視窗分割

- `:vs`       垂直分割
- `Ctrl`+`w` `v` 垂直分割
- `:sp`       水平分割
- `Ctrl`+`w` `s` 水平分割
- `Ctrl`+`w` `left[right] arrow` 左右切換視窗
- `Ctrl`+`w` `up[down] arrow`    上下切換視窗

### 好用的 plugin

* [rails.vim](http://www.vim.org/scripts/script.php?script_id=1567): Rails 套件(語法顏色，快速切換檔案... 等)

    * `Rcd 目錄` 切換目錄(從專案目錄出發)

    * `Rmodel 檔案`      編輯 model 檔案

    * `Rview 檔案`       編輯 view 檔案

    * `Rcontroller 檔案` 編輯 controller 檔案

* [snipMate](http://www.vim.org/scripts/script.php?script_id=2540): 加入程式片段

    * `Tab` 加入程式片段

* [ctrp](https://github.com/kien/ctrlp.vim): 模糊搜尋

    * `Ctrl`+`p` 啟動模糊搜尋
    * `Ctrl`+`v` 垂直分頁開啟檔案

* [fencview.vim](http://www.vim.org/scripts/script.php?script_id=1708): 自動偵測多國編碼

    * `:FencAutoDetect` 啟動偵測

* [nerdtree.vim](http://www.vim.org/scripts/script.php?script_id=1658): 檔案瀏覽器

    * `:e .` 瀏覽工作目錄

* [supertab.vmb](http://www.vim.org/scripts/script.php?script_id=1643): 使用 Tab 來補全程式碼

    * `Tab` 補全程式碼

雖然 Vim 對初學者而言需要投入多一些的時間來熟悉，但只要上手後，
就會大幅提升你的編程效率。
