Title: Setting up logrotate for production server
Date: 2015-03-30
Tags: rails
Category: Web


This article will demonstrate how to use [logrotate](http://manpages.ubuntu.com/manpages/utopic/man8/logrotate.8.html) to maintain log files of rails.

- Switch to `root`
```
sudo su -l
```

- Define a file to maintain log files of rails

Assuming your app name is `myflix`,
create `/etc/logrotate.d/rails` with following content:

/etc/logrotate.d/rails:

    :::bash
    /home/deployer/apps/myflix/current/log/*.log {
      daily
      missingok
      rotate 7
      compress
      delaycompress
      notifempty
      copytruncate
      sharedscripts
      postrotate
        service sidekiq restart
        service unicorn restart
      endscript
    }

You may execute the command below for testing
```
logrotate -vf /etc/logrotate.conf
```
