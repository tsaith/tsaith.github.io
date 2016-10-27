Title: 使用 Procfile 和 Foreman
Date: 2015-01-12
Tags: rails
Category: Web


架設在 Heroku 上面的 app，
會使用一個檔案 `Procfile` 來宣告有哪些命令將被 [dynos](https://devcenter.heroku.com/articles/dynos) 所執行。
`Procfile` 是位於專案下的一個文字檔，
在檔案的內容中，
左側指定 process type，而右側是要執行的命令，
如以下的範例

{% codeblock Procfile %}
web: bundle exec rails server -p $PORT
{% endcodeblock %}
在 Heroku 上 `$PORT` 的預設值是 `5000`。

### 使用 Foreman

在本地端開發或偵錯應用程式時，
應該與遠端採用同樣的執行步驟，
以避免因為步驟的不同而造成難以發現的錯誤。

[Heroku Toolbelt](https://toolbelt.heroku.com/) 提供了一個命令 `foreman`，
讓我們可以在本地端按照 `Procfile` 的內容來啟動 app。

假設我們使用的 `Profile` 內容為

```
web: bundle exec rails server -p $PORT
```

執行 `foreman start` 後，將可以看到訊息如下
```
$ foreman start
09:09:59 web.1  | started with pid 3111
```
這時候連到 `http://localhost:5000/` 就可以看到已啟動的服務。

