Title: 在 Emacs 中使用 Vim: Evil
Date: 2015-01-05
Tags: emacs
Category: Misc


過去十多年來，
Vim 一直都是筆者最喜愛的文字編輯器，
然而就像其他許多資深的 Vim 使用者，
我也總是對另一套神器 Emacs 感到好奇;
於是前陣子，
終於下定決心花些時間去了解 Emacs 的使用方式。
而在體驗之後只能說，果然盛名之下無虛士，
難怪有人會講，
Emacs 根本就是偽裝成編輯器的作業系統!

就我個人主觀的看法，
Vim 因為支援許多單鍵的編輯功能，
所以在文本編輯上比較快速，
而 Emacs 因為使用 Lisp 語言，
所以在擴展性上相對強大。

那我們最後應該使用哪一套工具呢?
因為 [Evil](https://gitorious.org/evil/pages/Home) 的出現，
我們現在可以直接在 Emacs 中使用 Vim，魚與熊掌兼得！

### 安裝 Evil

`M`-`x` package-install `Ret` evil `Ret`

### 設定配置

在 ~/.emacs/init.el 裡面加入
```
(require 'evil)
(evil-mode 1)
```

### 使用方法

`C`-`z`: 在 Emacs 和 Vim 之間切接

