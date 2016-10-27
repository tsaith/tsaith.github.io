Title: 使用 Percol 進行模糊搜尋
Date: 2015-01-12
Tags: utils
Category: Misc



在開發專案時，我們常常需要在眾多資料夾下搜尋某個檔案，
可是往往卻無法記得完整的檔案名稱，或是找到檔案後，
希望能快速地將檔案路徑貼到其他應用程式上面。
針對以上的問題，
網路上有篇[文章](http://blog.binchen.org/posts/how-to-do-the-file-navigation-efficiently.html)提出了使用
[percol](https://github.com/mooz/percol)
結合 shell 命令的解決方案。
我稍微修改了一些流程，並記錄如下。

### 安裝 percol

因為 percol 是用 python 開發的工具，
所以我們需要先安裝 python 環境
```
brew install python
```
接著安裝 percol
```
pip install percol
```

### 設定 percol 快捷鍵

在 ~/.percol.d/rc.py 裡面定義常用的快捷鍵

    :::python
    # X / _ / X
    percol.view.PROMPT  = "<bold><yellow>X / _ / X</yellow></bold> %q"

    # Emacs like
    percol.import_keymap({
        "C-h" : lambda percol: percol.command.delete_backward_char(),
        "C-d" : lambda percol: percol.command.delete_forward_char(),
        "C-k" : lambda percol: percol.command.kill_end_of_line(),
        "C-y" : lambda percol: percol.command.yank(),
        "C-t" : lambda percol: percol.command.transpose_chars(),
        "C-a" : lambda percol: percol.command.beginning_of_line(),
        "C-e" : lambda percol: percol.command.end_of_line(),
        "C-b" : lambda percol: percol.command.backward_char(),
        "C-f" : lambda percol: percol.command.forward_char(),
        "M-f" : lambda percol: percol.command.forward_word(),
        "M-b" : lambda percol: percol.command.backward_word(),
        "M-d" : lambda percol: percol.command.delete_forward_word(),
        "M-h" : lambda percol: percol.command.delete_backward_word(),
        "C-n" : lambda percol: percol.command.select_next(),
        "C-p" : lambda percol: percol.command.select_previous(),
        "C-v" : lambda percol: percol.command.select_next_page(),
        "M-v" : lambda percol: percol.command.select_previous_page(),
        "M-<" : lambda percol: percol.command.select_top(),
        "M->" : lambda percol: percol.command.select_bottom(),
        "C-m" : lambda percol: percol.finish(),
        "C-j" : lambda percol: percol.finish(),
        "C-g" : lambda percol: percol.cancel(),
    })

### 定義 shell 命令

在 ~/.bash_profile 裡面自定常用的命令，如下

```
# file navigation with percol
[ $(uname -s | grep -c CYGWIN) -eq 1 ] && OS_NAME="CYGWIN" || OS_NAME=`uname -s`
function pclip() {
    if [ $OS_NAME == CYGWIN ]; then
        putclip $@;
    elif [ $OS_NAME == Darwin ]; then
        pbcopy $@;
    else
        if [ -x /usr/bin/xsel ]; then
            xsel -ib $@;
        else
            if [ -x /usr/bin/xclip ]; then
                xclip -selection c $@;
            else
                echo "Neither xsel or xclip is installed!"
            fi
        fi
    fi
}

function ff()
{
    local fullpath=$*
    local filename=${fullpath##*/} # remove "/" from the beginning
    filename=${filename##*./} # remove  ".../" from the beginning
    echo file=$filename
    #  only the filename without path is needed
    # filename should be reasonable
    local cli=`find $PWD -not -iwholename '*/target/*' -not -iwholename '*.svn*' -not -iwholename '*.git*' -not -iwholename '*.sass-cache*' -not -iwholename '*.hg*' -type f -iwholename '*'${filename}'*' -print | percol`
    echo ${cli}
    echo -n ${cli} |pclip;
}

function h () {
    # reverse history, pick up one line, remove new line characters and put it into clipboard
    if [ -z "$1" ]; then
        history | sed '1!G;h;$!d' | percol | sed -n 's/^ *[0-9][0-9]* *\(.*\)$/\1/p'| tr -d '\n' | pclip
    else
        history | grep "$1" | sed '1!G;h;$!d' | percol | sed -n 's/^ *[0-9][0-9]* *\(.*\)$/\1/p'| tr -d '\n' | pclip
    fi
}

function glsf () {
    local str=`git --no-pager log --oneline --stat $* |  percol`
    if [[ $str =~ ^[[:space:]]*([a-z0-9A-Z_.\/-]*).*$ ]]; then
        echo -n ${BASH_REMATCH[1]} | pclip;
        echo ${BASH_REMATCH[1]}
    fi
}

function ppgrep() {
    if [[ $1 == "" ]]; then
        PERCOL=percol
    else
        PERCOL="percol --query $1"
    fi
    ps aux | eval $PERCOL | awk '{ print $2 }'
}

function ppkill() {
    if [[ $1 =~ "^-" ]]; then
        QUERY=""            # options only
    else
        QUERY=$1            # with a query
        [[ $# > 0 ]] && shift
    fi
    ppgrep $QUERY | xargs kill $*
}
```

存檔後，若不想重開 terminal 可直接執行
`source ~/.bash_profile`
就可以立刻使用上面定義的命令。

### 使用範例

在專案下執行 `ff`，可以使用片段的檔名進行搜尋，
選擇檔案後按 `Return` 就會自動將檔名拷貝到系統的剪貼簿上。

{% img https://farm9.staticflickr.com/8659/16260930815_87c4d30484_b.jpg %}

直接執行 `h`，可搜尋並拷貝歷史命令。
{% img https://farm9.staticflickr.com/8644/15641025303_2ca6346fb7_b.jpg %}

如果想強制離開搜尋畫面，請按 `Ctrl`+ `c`。
