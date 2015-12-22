Title: Adding google analytics to octopress
Date: 2015-02-16
Tags: utils
Category: Web


Go to Google Analytics to get the tracking id.
Then, set the valud of `google_analytics_tracking_id` in the `_config.yml` of Octopress.

_config.yml:

```
# Google Analytics
google_analytics_tracking_id: UA-59891323-1
```

### 使用 Github Pages

In case you use Github Pages for Octopress,
please also add one line in the `source/_includes/google_analytics.html` as below.

source/_includes/google_analytics.html:

    :::html
    {% if site.google_analytics_tracking_id %}
      <script type="text/javascript">
        var _gaq = _gaq || [];
        _gaq.push(['_setAccount', '{{ site.google_analytics_tracking_id }}']);
        _gaq.push(['_setDomainName','github.io']); // add this line for Github Pages
        _gaq.push(['_trackPageview']);

        (function() {
          var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
          ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
          var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
        })();
      </script>
    {% endif %}

After publishing above settings, you are ready to view the traffic status in google analytics.
