Title: 在 RSpec 中使用 shared examples
Date: 2014-12-22
Tags: rails
Category: Web


使用 RSpec 撰寫測試時，
我們可以使用 [shared examples](http://www.relishapp.com/rspec/rspec-core/v/3-1/docs/example-groups/shared-examples) 將
常用的測試範例封裝起來，方便隨時調用。


假設我們撰寫了一些測試，如下

```ruby
require "spec_helper"

describe VideosController do

  describe "GET index" do
    it "sets @categories for authenticated users" do
      set_current_user
      category = Fabricate(:category)
      get :index
      expect(assigns(:categories)).to eq [category]
    end

    it "redirects to the sign in page" do
      get :index
      expect(response).to redirect_to sign_in_path
    end

    it "sets the flash error message" do
      get :index
      expect(flash[:error]).to be_present
    end

  end

  describe "GET show" do
    it "sets @video for authenticated user" do
      set_current_user
      video = Fabricate(:video)
      get :show, id: video.slug
      expect(assigns(:video)).to eq video
    end

    it "redirects to the sign in page" do
      video = Fabricate(:video)
      get :show, id: video.slug
      expect(response).to redirect_to sign_in_path
    end

    it "sets the flash error message" do
      video = Fabricate(:video)
      get :show, id: video.slug
      expect(flash[:error]).to be_present
    end

  end

end
```

正如所見，`GET index` 和 `GET show` 裡面存在著類似的測試，
我們可以此部分放到 spec/support/shared_examples.rb 裡面

```ruby
shared_examples "requires sign in" do

  it "redirects to the sign in page" do
    action
    expect(response).to redirect_to sign_in_path
  end

  it "sets the flash error message" do
    action
    expect(flash[:error]).to be_present
  end

end
```

於是原先的測試程式就可以 refactor 成

```ruby
require "spec_helper"

describe VideosController do

  describe "GET index" do
    it "sets @categories for authenticated users" do
      set_current_user
      category = Fabricate(:category)
      get :index
      expect(assigns(:categories)).to eq [category]
    end

    it_behaves_like "requires sign in" do
      video = Fabricate(:video)
      let(:action) { get :index }
    end

  end

  describe "GET show" do
    it "sets @video for authenticated user" do
      set_current_user
      video = Fabricate(:video)
      get :show, id: video.slug
      expect(assigns(:video)).to eq video
    end

    it_behaves_like "requires sign in" do
      video = Fabricate(:video)
      let(:action) { get :show, id: video.slug }
    end

  end

end
```

除了程式碼變得簡潔之外，
日後我們也更容易對封裝的部分進行功能的擴充或修改。

