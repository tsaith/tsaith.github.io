Title: 對 Octopress 進行客製化
Date: 2014-10-25
Tags: octopress
Category: Web


會選擇使用 Octopress 的使用者，
應該都是希望之後能夠修改自己的部落格，
可以增加需要的功能以及讓版面顯得與眾不同;
這篇文章將會介紹如何進行。

### 設定部落格標題

在 _config.yml 裡面可以設定部落格的標題和子標題，如下

    :::yaml
    url: http://tsaith.github.io
    title: TH's Notes
    subtitle: Ruby / Rails / Life
    author: TH
    simple_search: https://www.google.com/search
    description:

### 加入 About 頁面


在 `source/_includes/custom/navigation.html` 裡面加入
`About` 連結，如下


    :::html
    <ul class="main-navigation">
      <li><a href="{{ root_url }}/">Blog</a></li>
      <li><a href="{{ root_url }}/blog/archives">Archives</a></li>
      <li><a href="{{ root_url }}/about">About</a></li>
    </ul>

執行 `rake new_page['about']` 以產生
`source/about/index.markdown`，
在檔案內編寫您的自我介紹，如下

    :::ruby
    ### About me

    Say something ...

### 改變 Color Scheme

Octopress 預設採用 dark Solarized highlighting，
如果想改用 light style，
可在 sass/custom/_colors.scss 中 uncomment `//$solarized: light;`，如下

```
/* To use the light Solarized highlighting theme uncomment the following line */
$solarized: light;
```

如果需要更多進階設定，請參考[官方文件](http://octopress.org/docs/theme/styles/)。

### 搜尋功能

在檔案 `source/_includes/navigation.html` 裡面，將
```
<input type="hidden" name="q" value="site:{{ site.url | shorthand_url }}" />
```

修改為

```
<input type="hidden" name="sitesearch" value="{{ site.url | shorthand_url }}" />
```

然後存檔，即可透過 Google 進行關鍵字搜尋。

### 留言功能

倘若想開啟 Disqus 留言功能，請進行下面兩個步驟:

* 到官網[註冊](https://disqus.com)，登入後，
選擇 'Add Disqus to your site'，註冊你網站來得到對應的 "shortname"。

* 在 Octopress 專案下，編輯檔案 _config.yml，
在 `disqus_short_name:` 這一欄填入剛剛取得的 "shortname"。

### 連結內部文章

編輯文章時，常常會需要連結到之前的文章作為參考，
假設欲連結的文章檔名是 2014-10-22-install-rails-on-mac.markdown，那麼可以使用下列的語法

```plain
[link name]({% post_url 2014-10-22-install-rails-on-mac %})
```
倘若上面的語法出現語法解析錯誤，則可以嘗試使用

```plain
[link name]( /blog/2014/10/22/install-rails-on-mac )
```
