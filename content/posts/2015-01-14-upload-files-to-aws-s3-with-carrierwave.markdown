Title: 使用 CarrierWave 上傳檔案到 AWS S3
Date: 2015-01-14
Tags: rails, aws
Category: Web


在網路應用中，將檔案上傳到雲端儲存服務是個常見並且重要的功能，
這篇文章將示範如何在 Rails 專案中使用 [CarrierWave](https://github.com/carrierwaveuploader/carrierwave) 將檔案上傳到
[AWS S3](http://aws.amazon.com/s3/)的實作流程。


### 申請 AWS S3

先在 AWS 的官網進行[註冊](http://aws.amazon.com/)，
若是第一次使用 AWS，在登入帳號後，
需要先到 [IAM](https://console.aws.amazon.com/iam/home?region=ap-northeast-1#home) 新增使用者群組並選擇適當的權限(例如 Amazon S3 Full Access)，
然後再新增一位使用者，
將使用者加入到剛剛新增的群組中，
確保該使用者有存取 S3 的權限。
最後，再到 [S3](https://console.aws.amazon.com/s3/home?region=ap-northeast-1) 的服務下，
為專案新增 [buckets](http://docs.aws.amazon.com/AmazonS3/latest/dev/UsingBucket.html)。

### 安裝套件

因為 CarrierWave 需要使用到 [ImageMagic](http://www.imagemagick.org/)，
若您的開發環境是 Mac，可以使用 Homebrew 進行安裝

```
brew install imagemagick
```

接著在 Gemfile 中加入
```
gem 'carrierwave'
gem 'mini_magick'
gem 'fog'
```
然後執行 `bundle install`。

請注意，因為 `MiniMagick` 是 `ImageMagick` 的 Ruby 界面，
所以它的安裝順序需要在 `ImageMagick` 之後。

### 開發目標

假設我們現在希望為網站開發一個上傳影片的功能，
每部影片有兩種尺寸的封面圖片，以及影片的連結;
下面將敘述實作的流程。

### 新增欄位

先在資料庫的 `videos` table 裡面新增
`large_cover`、 `small_cover` 以及 `video_url` 三個欄位，如下

db/schema.rb:

    :::ruby
    create_table "videos", force: true do |t|
      t.string   "title"
      t.integer  "category_id"
      t.string   "large_cover" # 大尺寸的封面
      t.string   "small_cover" # 小尺寸的封面
      t.string   "video_url"   # 影片連結
      t.text     "description"
      t.string   "slug"
      t.datetime "created_at"
      t.datetime "updated_at"
    end

### 產生 uploader

在專案目錄下執行
```
rails generate uploader large_cover
rails generate uploader small_cover
```

然後編輯剛產生出來的兩個 uploader 檔案，內容如下

app/uploaders/large_cover.rb:

    :::ruby
    # encoding: utf-8

    class LargeCoverUploader < CarrierWave::Uploader::Base
      include CarrierWave::MiniMagick

      process :resize_to_fill => [665, 375] # 圖片大小

      # Override the directory where uploaded files will be stored.
      # This is a sensible default for uploaders that are meant to be mounted:
      def store_dir
        "uploads/#{model.class.to_s.underscore}/#{mounted_as}/#{model.id}"
      end
    end

app/uploaders/small_cover.rb:

    :::ruby
    # encoding: utf-8

    class SmallCoverUploader < CarrierWave::Uploader::Base
      include CarrierWave::MiniMagick

      process :resize_to_fill => [166, 236] # 圖片大小

      # Override the directory where uploaded files will be stored.
      # This is a sensible default for uploaders that are meant to be mounted:
      def store_dir
        "uploads/#{model.class.to_s.underscore}/#{mounted_as}/#{model.id}"
      end
    end

### 掛載 uploader

在 Video model 掛載上面產生的 uploaders，如下

app/models/video.rb:

    :::ruby
    class Video < ActiveRecord::Base

      mount_uploader :large_cover, LargeCoverUploader
      mount_uploader :small_cover, SmallCoverUploader

          ... 程式碼省略 ...

        end

    ### 設定雲端檔案服務

    在 `config/initializers` 目錄下新增檔案 `carrierwave.rb` 設定如下

    config/initializers/carrierwave.rb:

    :::ruby
    CarrierWave.configure do |config|
      if Rails.env.staging? || Rails.env.production?
        config.storage = :fog
        config.fog_credentials = {
          :provider               => 'AWS',
          :aws_access_key_id      => ENV['AWS_ACCESS_KEY_ID'],
          :aws_secret_access_key  => ENV['AWS_SECRET_ACCESS_KEY'],
          :region => ENV['S3_BUCKET_REGION']
        }
        config.fog_directory  = ENV['S3_BUCKET_NAME']
      else
        config.storage = :file
        config.enable_processing = Rails.env.development?
      end
    end

若在 `staging` 或 `production` 環境下，
將會透過 `fog` 上傳檔案到 AWS 的 bucket;
若是開發環境，
則會將檔案放在本地端的 `public` 目錄下。

設定 `:aws_access_key_id` 和 `:aws_secret_access_key` 時，
請使用 `IAM` 的使用者驗証資訊。

### View 與 Controller

最後再編寫上傳檔案的界面，如下

{% img https://farm8.staticflickr.com/7312/16175096728_04b1014aa4_b.jpg %}

新增影片時將會自動上傳封面圖片到遠端。
通常，我們不會直接上傳影片(因為檔案較大)到 S3，
而會使用專業的影片服務進行上傳，再儲存網址。
若是公開的影片，可以使用 [YouTube](https://www.youtube.com/);
不公開的影片，可以考慮 [Vimeo](https://vimeo.com/) 或 [Wistia](http://wistia.com/)。

以下是 view 的程式碼

app/views/admin/videos/new.html.haml:

    :::haml
    %section.admin_add_video
      .container
        .row
          .col-md-10.col-md-offset-1
            = bootstrap_form_for [:admin, @video], layout: :horizontal,
              label_col: "col-sm-3", control_col: "col-sm-6"  do |f|
              %ul.nav.nav-tabs
                %li
                  %a(href="") Recent Payments
                %li.active
                  = link_to "Add a New Video", new_admin_video_path
              %br
              %fieldset
                = f.text_field :title, control_col: "col-sm-3"
                = f.select :category_id,
                  options_from_collection_for_select(Category.all, :id, :name)
                = f.text_area :description, rows: 8
                = f.file_field :large_cover, class: "btn btn-default btn-file"
                = f.file_field :small_cover, class: "btn btn-default btn-file"
                = f.text_field :video_url, label: "Video URL"
              %fieldset.actions.form-group
                .col-sm-6.col-md-offset-3
                  = f.submit "Add Video", class: "btn btn-default"

對應的 controller 如下

app/controllers/admin/video_controller.rb:

    :::ruby
    class Admin::VideosController < AdminsController

      def new
        @video = Video.new
      end

      def create
        @video = Video.new(video_params)
        if @video.save
          flash[:success] = "You have successfully added the video '#{@video.title}'."
          redirect_to new_admin_video_path
        else
          flash[:danger] = "You cannot add this video. Please check the errors."
          render :new
        end

      end

      private

      def video_params
        params.require(:video).permit(:title, :category_id, :description,
                                      :large_cover, :small_cover, :video_url)
      end

    end
