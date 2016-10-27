Title: 使用 paratropper 自動化部署流程
Date: 2015-01-13
Tags: rails
Category: Web


假設我們已經在 Heroku 上面架設了 staging 和 production servers，
倘若每次修改完程式都要手動地處理部署的工作，
這不僅沒有效率，而且很容易發生錯誤;
所以這裡將介紹如何使用 [paratrooper](https://github.com/mattpolito/paratrooper)，將部署的流程自動化。


### 安裝套件

在 Gemfile 加入
```
gem 'paratrooper'
```
然後執行 `bundle install`。

### 設定流程

在 lib/tasks/ 裡面新增一個檔案 deploy.rake 內容如下

    :::ruby
    require 'paratrooper'

    namespace :deploy do
      desc 'Deploy app in staging environment'
      task :staging do
        deployment = Paratrooper::Deploy.new("amazing-staging-app", tag: 'staging')

        deployment.deploy
      end

      desc 'Deploy app in production environment'
      task :production do
        deployment = Paratrooper::Deploy.new("amazing-production-app") do |deploy|
          deploy.tag              = 'production'
          deploy.match_tag        = 'staging'
        end

        deployment.deploy
      end
    end

注意，上面程式中的 `amazing-staging-app` 和 `amazing-production-app`，需要修改成你的 staging 和 production 名稱。


現在，若要 deploy 到 staging 請執行 `rake deploy:staging`;
倘若想 deploy 到 production 則執行 `rake deploy:production`。

