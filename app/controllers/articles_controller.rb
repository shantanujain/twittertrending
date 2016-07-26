class ArticlesController < ApplicationController
    def new
        client = Twitter::REST::Client.new do |config|
            config.consumer_key    = "8yEM5tZHe1kgh6pRM8hYMtdsz"
            config.consumer_secret = "zaXl77mTujGJjeNS9lrjjaRcYo2okkMC4lB2F7gF12lQznlEEb"
        end
        #@locid = params[:param1]
        @latitude = params[:param1]
        @longitude = params[:param2]
        @closest = client.trends_closest(options = {:lat => @latitude, :long => @longitude})
        @locid1 = @closest[0].woeid
        @trends = client.trends(id = @locid1, opions = {})
        
    end
end
