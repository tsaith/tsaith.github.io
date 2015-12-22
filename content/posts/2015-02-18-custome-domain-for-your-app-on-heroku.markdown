Title: Custom domain for your app on Heroku
Date: 2015-02-18
Tags: rails, heroku
Category: Web


First of all, apply a domain from any DNS provider like [Godaddy](http://www.godaddy.com).

To add a domain to your app, please execute the following command under the project directory.
```
heroku domains:add www.example.com
```
To remove the domain from your app, please execute
```
heroku domains:remove www.example.com
```
