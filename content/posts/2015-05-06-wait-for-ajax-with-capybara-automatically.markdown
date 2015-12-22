Title: Wait for Ajax with Capybara Automatically
Date: 2015-05-06
Tags: rails
Category: Web


While writing feature tests involved in Ajax, we have to resolve race condition from time to time. Let's see the following code as an example.

spec/features/admin_deletes_product_spec.rb:

    :::ruby
    require 'spec_helper.rb'

    feature "Admin deletes product category", { js: true} do
      before { page.driver.allow_url("fonts.googleapis.com") }
      after { clear_email }

      scenario "when the action is successful" do
        category = Fabricate(:product_category)
        product = Fabricate(:product, category: category)
        cloud = Fabricate(:admin)

        sign_in(cloud)
        visit admin_products_path
        find("a[id='delete_product_#{product.id}']").click

        # Without this line, there will be a race condition between deleting product and database query
        wait_for_ajax

        expect(Product.count).to eq 0
      end

    end

where the function `wait_for_ajax` is used to make sure the product has been deleted before querying the count of products in database.

spec/support/wait_for_ajax.rb:

    :::ruby
    module WaitForAjax
      def wait_for_ajax
        Timeout.timeout(Capybara.default_wait_time) do
          loop until finished_all_ajax_requests?
        end
      end

      def finished_all_ajax_requests?
        page.evaluate_script('jQuery.active').zero?
      end
    end

More discussion about this issue can be found in Thoughtbot's [post](https://robots.thoughtbot.com/automatically-wait-for-ajax-with-capybara).
