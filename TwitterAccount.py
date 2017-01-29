class TwitterAccount:
    favorited_count = -1
    retweet_count = -1
    follower_count = -1
    total_tweet_count = -1
    recent_tweet_count = -1
    handle = None
    type = None
    tweet_list = []
    polarity = []
    positive_count = -1
    neutral_count = -1
    negative_count = -1

    def __init__(self, handle, type):
        self.handle = handle
        self.type = type

    def initialize_account_data(self, follower_count, total_tweet_count):
        self.follower_count = follower_count
        self.total_tweet_count = total_tweet_count

    def initialize_tweet_data(self, tweet_list, favorited_count, retweet_count, polarity, positive_count, neutral_count, negative_count):
        self.favorited_count = favorited_count
        self.recent_tweet_count = len(tweet_list)
        self.retweet_count = retweet_count
        self.tweet_list = tweet_list
        self.polarity = polarity
        self.positive_count = positive_count
        self.neutral_count = neutral_count
        self.negative_count = negative_count
