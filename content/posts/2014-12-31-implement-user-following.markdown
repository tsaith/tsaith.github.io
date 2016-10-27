Title: 實作 Follow 社交功能
Date: 2014-12-31
Tags: rails
Category: Web


有使用過 Facebook 或 Twitter 的使用者們一定都不會對 Follow
這項功能感到陌生，
這裡將介紹如何實作這個機制。

### Routes

在 routes.rb 中加入下列路徑

app/config/routes.rb:

    :::ruby
    Myflix::Applation.routes.draw do
      ... 其他程式碼 ...

      resources :relationships, only: [:create, :destroy]
      get 'people', to: 'relationships#index'

    end

### Models

新增 Relationship 模型

app/models/relationship.rb:

    :::ruby
    class Relationship < ActiveRecord::Base
      belongs_to :leader, class_name: 'User'
      belongs_to :follower, class_name: 'User'
    end


User 透過 following_relationships 和 leading_relationships
來記錄跟隨的關係;並定義 follow? 和 can_follow? 方法。

app/models/user.rb:

    :::ruby
    class User < ActiveRecord::Base

      ... 其他程式碼 ...

      has_many :relationships
      has_many :following_relationships, class_name: 'Relationship', foreign_key: 'follower_id'
      has_many :leading_relationships, class_name: 'Relationship', foreign_key: 'leader_id'
      has_many :leaders, class_name: 'User', through: :relationships

      def follows?(another_user)
        following_relationships.map(&:leader).include?(another_user)
      end

      def can_follow?(another_user)
        !(self == another_user || self.follows?(another_user))
      end

    end

### Controllers

新增 RelationshipsController

app/controllers/relationships_controller.rb:

    :::ruby
    class RelationshipsController < ApplicationController

      before_action :require_user

      def index # 顯示所有 following 關係
        @relationships = current_user.following_relationships
      end

      def create # 建立 following 關係
        leader = User.find(params[:leader_id])
        Relationship.create(leader: leader, follower: current_user) if current_user.can_follow?(leader)
        redirect_to people_path
      end

      def destroy # 移除 following 關係
        relationship = Relationship.find(params[:id])
        relationship.destroy if relationship.follower == current_user
        redirect_to people_path
      end

    end

### Views

按下 Follow 連結可跟隨使用者

{% img https://farm9.staticflickr.com/8591/16181912915_c991d8d5ba_b.jpg %}

app/views/users/show.rb:

    :::haml
    %section.user.container
      .row
        .col-sm-10.col-sm-offset-1
          %article
            %header
              %img(src="http://www.gravatar.com/avatar/#{Digest::MD5.hexdigest(@user.email.downcase)}?s=40")
              %h2 #{@user.full_name}'s video collections (#{@user.queue_items.count})
              -# 顯示 Follow 連結
              - if current_user.can_follow?(@user)
                = link_to "Follow", relationships_path(leader_id: @user.id ), method: :post, class: 'btn btn-default'

            %table.table
              %thead
                %tr
                  %th(width="30%") Video Title
                  %th(width="15%") Genre
              %tbody
                - @user.queue_items.each do |queue_item|
                  %tr
                    %td
                      = link_to queue_item.video_title, queue_item.video
                    %td
                      = link_to queue_item.category_name, queue_item.category


顯示所有 Following 關係

{% img https://farm8.staticflickr.com/7513/15994591660_c722835f08_b.jpg %}

app/views/relationships/index.rb:

    :::haml
    %section.people
      %header
        %h2 People I Follow
      %table.table
        %thead
          %tr
            %th(width="30%")
            %th(width="20%") Videos in Queue
            %th(width="20%") Followers
            %th(width="30%") Unfollow
        %tbody
          - @relationships.each do |relationship| # following 關係
            %tr
              %td
                %img(src="http://www.gravatar.com/avatar/#{Digest::MD5.hexdigest(relationship.leader.email.downcase)}?s=40")
                = link_to relationship.leader.full_name, relationship.leader
              %td.extra-padding #{relationship.leader.queue_items.count}
              %td.extra-padding #{relationship.leader.leading_relationships.count}
              %td.extra-padding
                = link_to relationship, method: :delete do # 移除 following 關係
                  %i.glyphicon.glyphicon-remove
