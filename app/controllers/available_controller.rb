class AvailableController < ApplicationController
    def index
        client = Twitter::REST::Client.new do |config|
            config.consumer_key    = "8yEM5tZHe1kgh6pRM8hYMtdsz"
            config.consumer_secret = "zaXl77mTujGJjeNS9lrjjaRcYo2okkMC4lB2F7gF12lQznlEEb"
        end
        @available = client.trends_available(options = {})
        @available.shift
    end
end
