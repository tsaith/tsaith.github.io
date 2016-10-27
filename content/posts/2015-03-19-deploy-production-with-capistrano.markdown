Title: Deploy production with Capistrano
Date: 2015-03-19
Tags: rails
Category: Web


This article will describe how to deploy production with [Capistrano](https://github.com/capistrano/rails/).
The [official site](http://capistranorb.com/) provides useful explanations on the usage and structure of capistrano.

Here we assume that you are already able to login your production server with SSH key.

### Installation

Add the lines to Gemfile:

Gemfile:

    :::ruby
    gem 'capistrano-rails', '1.1.2'
    gem 'capistrano-rbenv', '2.0.3', require: false

Install and initialize capistrano:
```
bundle install
cap install
```

Add the followings lines to `Capfile`.

    :::ruby
    require 'capistrano/setup'
    require 'capistrano/deploy'
    require 'capistrano/rbenv'
    require 'capistrano/bundler'
    require 'capistrano/rails/migrations'
    require 'capistrano/rails/assets'

    Dir.glob('lib/capistrano/tasks/*.rake').each { |r| import r }

### Configuration

Set up global configuration in `config/deploy.rb` as following sample.

config/deploy.rb:

    :::ruby
    # config valid only for current version of Capistrano
    lock '3.4.0'

    set :application, 'YOUR_APP_Name'
    set :domain, "#{fetch(:application)}.com"
    set :user, "deployer"
    set :repo_url, "git@bitbucket.org:YOUR_ACCOUNT_NAME/#{fetch(:application)}.git"
    set :deploy_to, "/home/deployer/apps/#{fetch(:application)}"
    set :current_path, "#{fetch(:deploy_to)}/current"
    set :shared_path, "#{fetch(:deploy_to)}/shared"
    set :releases_path, "#{fetch(:deploy_to)}/releases"
    set :default_env, { path: "~/.rbenv/shims:~/.rbenv/bin:$PATH" }
    set :rbenv_ruby, '2.1.5'
    set :deploy_via, :remote_cache

    set :linked_files, fetch(:linked_files, []).push('config/application.yml', 'config/database.yml', 'config/secrets.yml')

    set :linked_dirs, fetch(:linked_dirs, []).push('log', 'tmp')

Next, set up the IP of your production server in `config/deploy/production.rb`:

config/deploy/production.rb:

    :::ruby
    server '162.233.120.172', user: 'deployer', roles: %w{web app db}

Be sure that `db` is added for database migration will be executed.


### Start to deploy

All you have to do is execute this command:
```
cap production deploy
```

### List all tasks

To view all available tasks in capistrano:
```
cap -T
```
### Define your own tasks

You can write your own tasks and put them under `lib/capistrano/tasks/`.

For example, assume we have wrote a task named `access_check.rake` with following content:

lib/capistrano/tasks/access_check.rake:

    :::ruby
    desc "Check that we can access everything"
    task :check_write_permissions do
      on roles(:all) do |host|
        if test("[ -w #{fetch(:deploy_to)} ]")
          info "#{fetch(:deploy_to)} is writable on #{host}"
        else
          error "#{fetch(:deploy_to)} is not writable on #{host}"
        end
      end
    end

Now, we can check if we have enough writing permissions on the production server by executing:
```
cap production check_write_permissions
```
