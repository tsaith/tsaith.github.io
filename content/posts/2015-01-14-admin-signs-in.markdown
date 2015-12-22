Title: 管理者登入機制
Date: 2015-01-14
Tags: rails
Category: Web


後台管理系統是網站的一項重要功能，
使用者必須擁有管理者權限才可以在後台進行一些特定操作
(例如，新增商品、下架、查看交易記錄 ... 等);
這篇文章將敘述如何在使用者[驗證機制](/blog/2014/11/09/how-to-implement-user-authentication-in-rails)
中加入管理者權限，並在登入後可以訪問後台的工作頁面。

### 新增欄位

在 `users` table 加入 `admin` 欄位
```plain
$ rails g migration add_admin_to_users admin:boolean
$ rake db:migrate
```

查看 `admin` 欄位是否已成功加入

db/schema.rb:

    :::ruby
    create_table "users", force: true do |t|
      t.string   "full_name"
      t.string   "email"
      t.string   "password_digest"
      t.string   "slug"
      t.datetime "created_at"
      t.datetime "updated_at"
      t.string   "token"
      t.boolean  "admin" # 新增的欄位
    end

### 設定 routes

加入管理者新增影片的路徑

config/routes.rb:

    :::ruby
    ... 省略程式碼 ...

    namespace :admin do
      resources :videos, only: [:new, :create]
    end

### Controllers

在 app/controllers/admin 目錄下，
新增 `VideosController`

app/controllers/admin/videos_controller.rb:

    :::ruby
    class Admin::VideosController < AdminsController

      def new
        @video = Video.new
      end

      def create
        # ... 省略程式碼 ...
      end

    end

app/controllers/admin_controller.rb:

    :::ruby
    class AdminsController < AuthenticatedController
      before_action :require_admin
    end

app/controllers/authenticated_controller.rb:

    :::ruby
    class AuthenticatedController < ApplicationController
      before_action :require_user
    end

### Views

在網頁中加入連結，導向新增影片的頁面
app/views/shared/_header.html.haml:

    :::haml

    %li
      -# 新增影片
      = link_to "Add Video", new_admin_video_path if current_user.admin?
      = link_to "Invite a friend", new_invitation_path
      %a(href="#") Account
      %a(href="#") Plan and Billing
      %a(href="/sign_out") Sign Out

在 app/views/admin/videos/ 下面加入新增影片的頁面

{% img https://farm8.staticflickr.com/7544/16297530732_85cd796652_b.jpg %}

app/views/admin/videos/new.html.haml:

    :::haml
    %section.admin_add_video
      .container
        .row
          .col-md-10.col-md-offset-1
            = bootstrap_form_for [:admin, @video], layout: :horizontal, label_col: "col-sm-3", control_col: "col-sm-6"  do |f|
              %ul.nav.nav-tabs
                %li
                  %a(href="") Recent Payments
                %li.active
                  %a(href="") Add a New Video
              %br
              %fieldset
                = f.text_field :title, control_col: "col-sm-3"
                = f.select :category_id, options_from_collection_for_select(Category.all, :id, :name)
                = f.text_area :description, rows: 8
                .form-group
                  %label.control-label.col-sm-3 Large Cover
                  .col-sm-6
                    %col.btn.btn-file
                      %input.form-control(type="file")
                .form-group
                  %label.control-label.col-sm-3 Small Cover
                  .col-sm-6
                    %col.btn.btn-file
                      %input.form-control(type="file")
              %fieldset.actions.form-group
                .col-sm-6.col-md-offset-3
                  = f.submit "Add Video", class: "btn btn-default"
