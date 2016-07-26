class ArticlesController < ApplicationController
    def new
        client = Twitter::REST::Client.new do |config|
            config.consumer_key    = "8yEM5tZHe1kgh6pRM8hYMtdsz"
            config.consumer_secret = "zaXl77mTujGJjeNS9lrjjaRcYo2okkMC4lB2F7gF12lQznlEEb"
        end
        @trends = client.trends(id = 1, options = {})
        puts @trends
    end
end
