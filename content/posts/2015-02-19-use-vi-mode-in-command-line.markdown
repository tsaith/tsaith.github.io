Title: Vi-mode in command-line and Rails Console
Date: 2015-02-19
Tags: rails, vim, emacs
Category: Misc


Since both command-line and rails console treat characters with `readline`,
we can add the line below in `~/.inputrc`
```
set editing-mode vi
```
to switch from the default `emacs-mode` to `vi-mode`.
