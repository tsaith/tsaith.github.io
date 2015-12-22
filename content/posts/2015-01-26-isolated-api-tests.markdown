Title: 獨立的 API 測試
Date: 2015-01-26
Tags: rails
Category: Web


撰寫測試時，
如果需要透過網路來呼叫外部服務的 API (例如信用卡的交易服務)，
因為 API 的回應通常需要一陣子，
這將大幅延長測試所需的等候時間;
此時可以考慮使用 [VCR](http://www.relishapp.com/vcr/vcr/v/2-9-3/docs/) (Video Cassette Recorder) 先將服務的回應記錄下來，
往後當呼叫到此服務的 API 時就自動播放，
以縮短測試時間。

### 安裝套件

在 Gemfile 中加入
```
group :test do
  gem 'vcr'
  gem 'webmock'
end
```
然後執行 `bundle install`

### 設定 VCR

在 `spec_helper.rb` 裡面設定 VCR 如下，
若想了解更多細節可參考 Relish 的[文件](https://www.relishapp.com/vcr/vcr/v/2-9-3/docs/test-frameworks/usage-with-rspec-metadata)。

spec/spec_helper.rb:

    :::ruby
    require 'vcr'

    VCR.configure do |c|
      c.cassette_library_dir = 'spec/cassettes'
      c.hook_into :webmock
      c.configure_rspec_metadata!
      c.ignore_localhost = true # 忽略本地端的 request
    end

    RSpec.configure do |config|

      # 在 RSpec 3 不再需要此行
      config.treat_symbols_as_metadata_keys_with_true_values = true
      ... 程式碼省略 ...
    end

### 加入 :vcr

現在，
只要在測試中加入 `:vcr` 就會自動記錄 API 的回應，
請參考下面的範例

stripe_wrapper_sepc.rb:

    :::ruby
    require 'spec_helper'

    describe StripeWrapper::Charge do

      let(:token) do
        Stripe::Token.create(
          :card => {
            :number => card_number,
            :exp_month => 1,
            :exp_year => 2016,
            :cvc => "314",
            :description => "some description"
          }
        ).id
      end

      context "with valid card" do
        let(:card_number) { '4242424242424242' }
        it "charges the card successfully", :vcr do # 加入 :vcr
          response = StripeWrapper::Charge.create(amount: 300, card: token)
          expect(response).to be_successful
        end
      end

      context "with invalid card" do
        let(:card_number) { '4000000000000002' }

        it "does not charge the card successfully", :vcr do # 加入 :vcr
          response = StripeWrapper::Charge.create(amount: 300, card: token)
          expect(response).not_to be_successful
        end
        it "contains an error message", :vcr do # 加入 :vcr
          response = StripeWrapper::Charge.create(amount: 300, card: token)
          expect(response.error_message).to be_present
        end
      end
    end

請注意，加入 `:vcr` 後的第一次測試，
仍會呼叫到外部服務，並記錄服務的回應;
之後的測試，才會直接使用先前的記錄。

在 `spec/cassettes` 裡面可以找到有哪些回應被記錄下來，如下

```
$ tree spec/cassettes
spec/cassettes
└── StripeWrapper_Charge
    ├── with_invalid_card
    │   ├── contains_an_error_message.yml
    │   └── does_not_charge_the_card_successfully.yml
    └── with_valid_card
        └── charges_the_card_successfully.yml

3 directories, 3 files
```
