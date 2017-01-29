import TwitterAccount as TA
import TwitterUtilityMethods as TUM

pump_makers = ['@MDT_Diabetes', '@myomnipod', '@TandemDiabetes']
meter_makers = ['@OneTouch', '@accuchek_us', '@FreeStyleDiabet']
account_types = ['pump_maker', 'meter_maker']
all_accounts = []


# account object creation
for i in range(len(pump_makers)):
    current = TA.TwitterAccount(pump_makers[i], account_types[0])
    all_accounts.append(current)


for i in range(len(meter_makers)):
    current = TA.TwitterAccount(meter_makers[i], account_types[1])
    all_accounts.append(current)


# account object initialization
for i in range(len(all_accounts)):
    TUM.get_account_data(all_accounts[i])
    TUM.get_tweets_by_year_month(all_accounts[i], 2016, 11)
    file_name = '/Users/niraj/Desktop/' + all_accounts[i].handle + '.csv'
    TUM.tweets_to_csv(file_name, all_accounts[i])


# compute retweet/follower count and favorite/follower count
pump_maker_follower_ratios = TUM.compute_follower_ratios(all_accounts, 0, 3)
meter_maker_follower_ratios = TUM.compute_follower_ratios(all_accounts, 3, 3)


# plot follower metric graphs
TUM.plot_double_bar_graph(pump_maker_follower_ratios['favorite_ratio'], pump_maker_follower_ratios['retweet_ratio'], pump_makers, '/Users/niraj/Desktop/Pump_Makers_Follower_Metrics.jpg', 'Follower metrics for Pump makers')
TUM.plot_double_bar_graph(meter_maker_follower_ratios['favorite_ratio'], meter_maker_follower_ratios['retweet_ratio'], meter_makers, '/Users/niraj/Desktop/Meter_Makers_Follower_Metrics.jpg', 'Follower metrics for Meter makers')


# compute retweet/tweet count and favorite/tweet count
pump_maker_ratios = TUM.compute_ratios(all_accounts, 0, 3)
meter_maker_ratios = TUM.compute_ratios(all_accounts, 3, 3)


# make list of total tweet count
pump_maker_total_count = TUM.make_total_tweet_list(all_accounts, 0, 3)
meter_maker_total_count = TUM.make_total_tweet_list(all_accounts, 3, 3)


# plot campaign effectiveness graphs
TUM.plot_double_bar_line_graph(pump_maker_ratios['favorite_ratio'], pump_maker_ratios['retweet_ratio'], pump_maker_total_count, pump_makers, '/Users/niraj/Desktop/Pump_Maker_Campaign_Analysis.jpg', 'Campaign effectiveness for Pump makers')
TUM.plot_double_bar_line_graph(meter_maker_ratios['favorite_ratio'], meter_maker_ratios['retweet_ratio'], meter_maker_total_count, meter_makers, '/Users/niraj/Desktop/Meter_Maker_Campaign_Analysis.jpg', 'Campaign effectiveness for Meter makers')


# make polarity lists
pump_polarity_lists = TUM.make_polarity_list(all_accounts, 0, 3)
meter_polarity_lists = TUM.make_polarity_list(all_accounts, 3, 3)


# plot tweet polarity graphs
TUM.plot_triple_bar_graph(pump_polarity_lists['positive_list'], pump_polarity_lists['neutral_list'], pump_polarity_lists['negative_list'], pump_makers, '/Users/niraj/Desktop/pump_polarity.jpg', 'Tweet polarity for Pump makers')
TUM.plot_triple_bar_graph(meter_polarity_lists['positive_list'], meter_polarity_lists['neutral_list'], meter_polarity_lists['negative_list'], meter_makers, '/Users/niraj/Desktop/meter_polarity.jpg', 'Tweet polarity for Meter makers')

print 'Done!'