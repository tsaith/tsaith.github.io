Title: Setting up Nginx+Unicorn production server
Date: 2015-03-30
Tags: rails
Category: Web


This article will describe how to install and configure [Nginx](http://nginx.org/) with [Unicorn](http://unicorn.bogomips.org/) to build a concurrent rails server based on Ubuntu.

Assume that we have logged in with a user account named `deployer`.

- Install Unicorn

Adding the following line to your `Gemfile` and execute `bundle install`.
```
gem 'unicorn'
```

- Switch to `root`
```
sudo su -l
```

- Write a init script for Unicorn

Asuming the name of your app is `myflix`,
create `/etc/init.d/unicorn` with the following content:

/etc/init.d/unicorn:

    :::bash
    #!/bin/sh

    # File: /etc/init.d/unicorn

    ### BEGIN INIT INFO
    # Provides:          unicorn
    # Required-Start:    $local_fs $remote_fs $network $syslog
    # Required-Stop:     $local_fs $remote_fs $network $syslog
    # Default-Start:     2 3 4 5
    # Default-Stop:      0 1 6
    # Short-Description: starts the unicorn web server
    # Description:       starts unicorn
    ### END INIT INFO

    # Feel free to change any of the following variables for your app:

    # Set user
    USER=deployer
    # Set app name
    APP_NAME=myflix

    # Replace [PATH_TO_RAILS_ROOT_FOLDER] with your application's path.
    APP_ROOT=/home/$USER/apps/$APP_NAME/current
    # Set the environment. This can be changed to staging or development for staging
    # servers.
    RAILS_ENV=production
    # This should match the pid setting in $APP_ROOT/config/unicorn.rb.
    PID_FILE=$APP_ROOT/tmp/unicorn.pid
    # A simple description for service output.
    DESC="Unicorn app - $RAILS_ENV"
    # If you're using rbenv, you may need to use the following setup to get things
    # working properly:
    RBENV_RUBY_VERSION=`cat $APP_ROOT/.ruby-version`
    RBENV_ROOT="/home/$USER/.rbenv"
    RBENV="$RBENV_ROOT/bin/rbenv"
    PATH="$RBENV_ROOT/bin:$PATH"
    SET_PATH="cd $APP_ROOT && $RBENV rehash && $RBENV local $RBENV_RUBY_VERSION"

    # Unicorn can be run using `bundle exec unicorn` or `bin/unicorn`.
    UNICORN="$RBENV_ROOT/shims/unicorn"
    # Execute the unicorn executable as a daemon, with the appropriate configuration
    # and in the appropriate environment.
    UNICORN_OPTS="-c $APP_ROOT/config/unicorn.rb -E $RAILS_ENV -D"
    CMD="$UNICORN $UNICORN_OPTS"

    # Give your upgrade action a timeout of 60 seconds.
    TIMEOUT=60

    # Store the action that we should take from the service command's first
    # argument (e.g. start, stop, upgrade).
    action="$1"

    # Make sure the script exits if any variables are unset. This is short for
    # set -o nounset.
    set -u

    # Set the location of the old pid. The old pid is the process that is getting
    # replaced.
    old_pid="$PID_FILE.oldbin"

    # Make sure the APP_ROOT is actually a folder that exists. An error message from
    # the cd command will be displayed if it fails.
    cd $APP_ROOT || exit 1

    # A function to send a signal to the current unicorn master process.
    sig () {
      test -s "$PID_FILE" && kill -$1 `cat $PID_FILE`
    }

    # Send a signal to the old process.
    oldsig () {
      test -s $old_pid && kill -$1 `cat $old_pid`
    }

    # A switch for handling the possible actions to take on the unicorn process.
    case $action in
      # Start the process by testing if it's there (sig 0), failing if it is,
      # otherwise running the command as specified above.
      start)
        sig 0 && echo >&2 "$DESC is already running" && exit 0
        su - $USER -c "$CMD"
        ;;

      # Graceful shutdown. Send QUIT signal to the process. Requests will be
      # completed before the processes are terminated.
      stop)
        sig QUIT && echo "Stopping $DESC" exit 0
        echo >&2 "Not running"
        ;;

      # Quick shutdown - kills all workers immediately.
      force-stop)
        sig TERM && echo "Force-stopping $DESC" && exit 0
        echo >&2 "Not running"
        ;;

      # Graceful shutdown and then start.
      restart)
        sig QUIT && echo "Restarting $DESC" && sleep 2 \
          && su - $USER -c "$CMD" && exit 0
        echo >&2 "Couldn't restart."
        ;;

      # Reloads config file (unicorn.rb) and gracefully restarts all workers. This
      # command won't pick up application code changes if you have `preload_app
      # true` in your unicorn.rb config file.
      reload)
        sig HUP && echo "Reloading configuration for $DESC" && exit 0
        echo >&2 "Couldn't reload configuration."
        ;;

      # Re-execute the running binary, then gracefully shutdown old process. This
      # command allows you to have zero-downtime deployments. The application may
      # spin for a minute, but at least the user doesn't get a 500 error page or
      # the like. Unicorn interprets the USR2 signal as a request to start a new
      # master process and phase out the old worker processes. If the upgrade fails
      # for some reason, a new process is started.
      upgrade)
        if sig USR2 && echo "Upgrading $DESC" && sleep 10 \
          && sig 0 && oldsig QUIT
        then
          n=$TIMEOUT
          while test -s $old_pid && test $n -ge 0
          do
            printf '.' && sleep 1 && n=$(( $n - 1 ))
          done
          echo

          if test $n -lt 0 && test -s $old_pid
          then
            echo >&2 "$old_pid still exists after $TIMEOUT seconds"
            exit 1
          fi
          exit 0
        fi
        echo >&2 "Couldn't upgrade, starting 'su - $USER -c \"$CMD\"' instead"
        su - $USER -c "$CMD"
        ;;

      # A basic status checker. Just checks if the master process is responding to
      # the `kill` command.
      status)
        sig 0 && echo >&2 "$DESC is running." && exit 0
        echo >&2 "$DESC is not running."
        ;;

      # Reopen all logs owned by the master and all workers.
      reopen-logs)
        sig USR1
        ;;

      # Any other action gets the usage message.
      *)
        # Usage
        echo >&2 "Usage: $0 <start|stop|restart|reload|upgrade|force-stop|reopen-logs>"
        exit 1
        ;;
    esac


Then, execute
```
chmod +x /etc/init.d/unicorn
update-rc.d unicorn defaults
service unicorn restart
```

- Prepare the configuration file of Unicorn under project directory

Create `config/unicorn.rb` with content as

config/unicorn.rb:

    :::ruby
    # Set the current app's path for later reference. Rails.root isn't available at
    # this point, so we have to point up a directory.
    app_path = File.expand_path(File.dirname(__FILE__) + '/..')

    # The number of worker processes you have here should equal the number of CPU cores your server has.
    worker_processes (ENV['RAILS_ENV'] == 'production' ? 2 : 1)

    # You can listen on a port or a socket. Listening on a socket is good in a
    # production environment, but listening on a port can be useful for local
    # debugging purposes.
    listen app_path + '/tmp/unicorn.sock', backlog: 64

    # For development, you may want to listen on port 3000 so that you can make sure
    # your unicorn.rb file is soundly configured.
    listen(3000, backlog: 64) if ENV['RAILS_ENV'] == 'development'
    # After the timeout is exhausted, the unicorn worker will be killed and a new
    # one brought up in its place. Adjust this to your application's needs. The
    # default timeout is 60. Anything under 3 seconds won't work properly.
    timeout 60

    # Set the working directory of this unicorn instance.
    working_directory app_path

    # Set the location of the unicorn pid file. This should match what we put in the
    # unicorn init script later.
    pid app_path + '/tmp/unicorn.pid'

    # You should define your stderr and stdout here. If you don't, stderr defaults
    # to /dev/null and you'll lose any error logging when in daemon mode.
    stderr_path app_path + '/log/unicorn.log'
    stdout_path app_path + '/log/unicorn.log'

    # Load the app up before forking.
    preload_app true

    # Garbage collection settings.
    GC.respond_to?(:copy_on_write_friendly=) &&
      GC.copy_on_write_friendly = true

    # If using ActiveRecord, disconnect (from the database) before forking.
    before_fork do |server, worker|
      defined?(ActiveRecord::Base) &&
        ActiveRecord::Base.connection.disconnect!
    end

    # After forking, restore your ActiveRecord connection.
    after_fork do |server, worker|
      defined?(ActiveRecord::Base) &&
        ActiveRecord::Base.establish_connection
    end

- Install and configure Nginx
```
apt-get install nginx
```

Edit `/etc/nginx/nginx.conf` as below

/etc/nginx/nginx.conf:

    :::bash
    # Run nginx as www-data.
    user www-data;
    # One worker process per CPU core is a good guideline.
    worker_processes 1;

    pid /var/run/nginx.pid;

    # For a single core server, 1024 is a good starting point. Use `ulimit -n` to
    # determine if your server can handle more.
    events {
        worker_connections 1024;
    }

    http {

      ##
      # Basic Settings
      ##

      sendfile on;
      tcp_nopush on;
      tcp_nodelay off;
      keepalive_timeout 65;
      types_hash_max_size 2048;
      server_tokens off;

      include /etc/nginx/mime.types;
      default_type application/octet-stream;

      ##
      # Logging Settings
      ##

      access_log /var/log/nginx/access.log;
      error_log /var/log/nginx/error.log;

      ##
      # Gzip Settings
      ##

      gzip on;
      gzip_disable "msie6";
      gzip_http_version 1.1;
      gzip_proxied any;
      gzip_min_length 500;
      gzip_types text/plain text/xml text/css
        text/comma-separated-values text/javascript
        application/x-javascript application/atom+xml;

      ##
      # Unicorn Rails
      ##

      # The socket here must match the socket path that you set up in unicorn.rb.
      upstream unicorn {
        server unix:/home/deployer/apps/myflix/current/tmp/unicorn.sock fail_timeout=0;
      }

      ##
      # Virtual Host Configs
      ##

      include /etc/nginx/conf.d/*.conf;
      include /etc/nginx/sites-enabled/*;
    }

Create `/etc/nginx/sites-available/myflix` with content:

/etc/nginx/sites-available/myflix:

    :::bash
    server {
      listen 80;
      server_name myflix.com; # Set server name

      keepalive_timeout 300;

      client_max_body_size 4G;

      root /home/deployer/apps/myflix/current/public; # Set this to the public folder location of your Rails application.

      try_files $uri/index.html $uri.html $uri @unicorn;

      location @unicorn {
              proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
              proxy_set_header Host $http_host;
              proxy_set_header X-Forwarded_Proto $scheme;
              proxy_redirect off;
              # This passes requests to unicorn, as defined in /etc/nginx/nginx.conf
              proxy_pass http://unicorn;
              proxy_read_timeout 300s;
              proxy_send_timeout 300s;
      }

      # You can override error pages by redirecting the requests to a file in your
      # application's public folder, if you so desire:
      error_page 500 502 503 504 /500.html;
      location = /500.html {
              root /home/deployer/apps/myflix/current/public;
      }
    }

Finally, execute the following commands:
```
cd /etc/nginx/sites-enabled
rm default
ln -s ../sites-available/myflix myflix
service nginx restart
```
