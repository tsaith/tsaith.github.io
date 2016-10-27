Title: 在部落格中加入 Flickr 圖片
Date: 2014-10-29
Tags: octopress
Category: Web


編寫部落格時，適當地加入圖片可以吸引更多讀者，同時也提高了文章的可讀性。
隨著雲端相簿的流行，有許多人會傾向將圖片貯存位置和部落格平台獨立開來;
這樣的話，一方面可以集中圖片的管理，另一方面，如果日後想更換寫作平台，
就不需要去煩惱圖片的轉移工作。

[Flickr](https://www.flickr.com/) 是目前相當受歡迎的免費雲端相簿，
這篇文章將說明如何用它將圖片加入到你的部落格中。

* 首先，請先到 [Flickr](https://www.flickr.com/) 上面註冊，
然後在裡面新增一份相簿，接著上傳一張測試圖片並加入到新建立的相簿中。

* 先選擇圖片，接著點選 "Share this photo"，然後指定希望的圖片大小，
這時候會產生對應的 HTML code。

{% img https://farm8.staticflickr.com/7561/15652040191_aec65ccfbc_b.jpg  %}

* 在 HTML code 中 `<img src=` 後面的部分就是圖片的網址
```
<img src="https://farm8.staticflickr.com/7563/15655510442_e9803f8335_b.jpg" width="1024" height="768" alt="FF-12">
```

* 最後在你的部落格中使用圖片的網址;
舉例來說，
倘若你使用的是 [Octopress](http://octopress.org/) ，
請在文章中加入
```
{% img https://farm8.staticflickr.com/7563/15655510442_e9803f8335_b.jpg %}
```

然後就能看到被加入的圖片，如下

{% img https://farm8.staticflickr.com/7563/15655510442_e9803f8335_b.jpg  %}
