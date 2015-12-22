Title: 快速啟動 rails: pow
Date: 2014-12-15
Tags: rails
Category: Web


許多 Rails 開發者應該都有這樣的經驗，
每次開發專案前總是得先在終端機執行 `rails server` 才能啟動網站，
這樣實在有點麻煩;
[Basecamp](https://basecamp.com/) 因此而開發了一個免費工具 [Pow](https://github.com/basecamp/pow) 可以簡單地為我們解決這個困擾。

### 安裝 Pow

在終端機下執行
```
$ curl get.pow.cx | sh
```

### 使用方法

進入 ~/.pow 目錄，然後創造一個專案的連結即可。
例如，假設我們有一個專案 ~/projects/myflix，
那麼可以執行下面的命令來創造對應的連結
```
$ cd ~/.pow
$ ln -s ~/projects/myflix
```

現在，
只要將瀏覽器連到 http://myflix.dev 就能看到運行的網站。

### 使用 RVM

因為 pow 預設只有支援 [rbenv](https://github.com/sstephenson/rbenv)，
所以 [rvm](https://rvm.io) 的使用者需要額外地在專案下新增 .powenv 並加入下面的內容，才能讓 pow 正常工作。

    :::bash
    if [ -z "${rvm_path:-}" ] && [ -x "${HOME:-}/.rvm/bin/rvm" ]
    then rvm_path="${HOME:-}/.rvm"
    fi
    if [ -z "${rvm_path:-}" ] && [ -x "/usr/local/rvm/bin/rvm" ]
    then rvm_path="/usr/local/rvm"
    fi

    # load environment of current project ruby
    if
      [ -n "${rvm_path:-}" ] &&
      [ -x "${rvm_path:-}/bin/rvm" ] &&
      rvm_project_environment=`"${rvm_path:-}/bin/rvm" . do rvm env --path 2>/dev/null` &&
      [ -n "${rvm_project_environment:-}" ] &&
      [ -s "${rvm_project_environment:-}" ]
    then
      echo "RVM loading: ${rvm_project_environment:-}"
      \. "${rvm_project_environment:-}"
    else
      echo "RVM project not found at: $PWD"
    fi

### 更方便地使用 Pow

[Powder](https://github.com/Rodreegez/powder) 可以讓 pow 的使用變得更加方便。

安裝套件
```
$ gem install powder
```

這裡列出一些常用的操作:

連結當前目錄到 ~/.pow/<當前目錄>
```
$ power link
```

在瀏覽器開啓專案
```
$ powder open
```

查看 .powenv 的內容
```
$ powder env
```

開啓 debug shell
```
$ power debug
```

重開 app
```
$ powder restart
```
