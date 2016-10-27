Title: Install rbenv and rails on ubuntu
Date: 2015-03-30
Tags: rails
Category: Web


This article will describe how to install [rbenv](https://github.com/sstephenson/rbenv), [rails](http://rubyonrails.org/) and some useful libraries on a production server of [ubuntu](http://www.ubuntu.com/).

Assuming that, on a fresh ubuntu, we have just built and logged in with a user account named `deployer`.

- Update apt-get
```
sudo apt-get update
```

- Install gcc, make and curl
```
sudo apt-get install gcc make curl
```

- Install git
```
sudo apt-get install git git-core
```

- Configure git
```
git config --global user.name "Your Name"
git config --global user.email "Your Email Address"
git config --global core.editor vi
git config --global color.ui true
git config --global color.branch auto
git config --global color.diff auto
git config --global color.status auto
```

- Install libraries required by rbenv
```
sudo apt-get install autoconf bison build-essential libssl-dev libyaml-dev libreadline6-dev zlib1g-dev libncurses5-dev libffi-dev libgdbm3 libgdbm-dev
```

- Install rbenv and the ruby versions builder
```
git clone git://github.com/sstephenson/rbenv.git .rbenv
echo 'export PATH="$HOME/.rbenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(rbenv init -)"' >> ~/.bashrc
git clone git://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build
echo 'export PATH="$HOME/.rbenv/plugins/ruby-build/bin:$PATH"' >> ~/.bashrc
git clone https://github.com/sstephenson/rbenv-gem-rehash.git ~/.rbenv/plugins/rbenv-gem-rehash
git clone https://github.com/ianheggie/rbenv-binstubs.git ~/.rbenv/plugins/rbenv-binstubs
```

- Add path for binstubs
```
echo 'PATH="./bin:$PATH"' >> ~/.bashrc
```

- Relogin the server
```
exit
ssh deployer@SERVER_IP
```

- Install Ruby version
```
rbenv install 2.1.5
rbenv global 2.1.5
```

- Install bundler
```
gem install bundler
```

- Install gems without documents
```
echo 'gem: --no-rdoc --no-ri' >> ~/.gemrc
```

- Install rails
```
gem install rails -v 4.1.1
```

- Install [Node.js](https://nodejs.org/) (javascript runtime) which is required to compile assests of rails
```
sudo apt-add-repository -y ppa:chris-lea/node.js
sudo apt-get -y update
sudo apt-get -y install nodejs
```

- Install qt lib for `capybara-webkit`[https://github.com/thoughtbot/capybara-webkit]
```
sudo apt-get install libqt4-dev
```

- Install [ImageMagick](http://www.imagemagick.org/)
```
sudo apt-get install imagemagick
```

- Install [PostgreSQL](http://www.postgresql.org/)
```
sudo apt-get install postgresql libpq-dev
```

- Execute the following command under project directory to make binstubs work
```
bundle install --binstubs .bundle/bin
```

- Set environment variables
```
sudo vi /etc/environment
```
and add the following lines:
```
RAILS_ENV=production
RACK_ENV=production
```

- Create a new user named `deployer` as superuser within PostgreSQL
```
sudo su -l postgres
createuser deployer --pwprompt
psql
ALTER USER deployer WITH SUPERUSER;
\q
exit
```
