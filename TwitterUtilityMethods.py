from __future__ import division
import tweepy
from tweepy import OAuthHandler
import Credentials
import requests
import json
import csv
import matplotlib.pyplot as plt
import numpy as np

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


auth = OAuthHandler(Credentials.c_key, Credentials.c_secret)
auth.set_access_token(Credentials.a_token, Credentials.a_secret)
api = tweepy.API(auth)


def get_account_data(account):
    user_data = api.get_user(account.handle)
    account.initialize_account_data(user_data.followers_count, user_data.statuses_count)
    print 'Initialized account data for: ' + account.handle


def compute_ratios(account_list, start_index, count):
    retweet_ratio = []
    favorite_ratio = []
    for i in range(count):
        r = (account_list[start_index + i].retweet_count / account_list[start_index + i].recent_tweet_count)
        f = (account_list[start_index + i].favorited_count / account_list[start_index + i].recent_tweet_count)
        retweet_ratio.append(r)
        favorite_ratio.append(f)
    print 'Computed tweet count ratios'
    return {'retweet_ratio':retweet_ratio, 'favorite_ratio':favorite_ratio}


def compute_follower_ratios(account_list, start_index, count):
    retweet_ratio = []
    favorite_ratio = []
    for i in range(count):
        retweet_to_follower = (account_list[start_index + i].retweet_count * 100)/account_list[start_index + i].follower_count
        favorite_to_follower = (account_list[start_index + i].favorited_count * 100)/ account_list[start_index + i].follower_count
        retweet_ratio.append(retweet_to_follower)
        favorite_ratio.append(favorite_to_follower)
    print 'Computed follower count ratios'
    return {'retweet_ratio': retweet_ratio, 'favorite_ratio': favorite_ratio}


def make_total_tweet_list(account_list, start_index, count):
    count_list = []
    for i in range(count):
        count_list.append(account_list[start_index + i].recent_tweet_count)
    return count_list


def make_polarity_list(account_list, start_index, count):
    positive_list = []
    neutral_list = []
    negative_list = []
    for i in range(count):
        current_positive = account_list[start_index + i].positive_count
        current_neutral = account_list[start_index + i].neutral_count
        current_negative = account_list[start_index + i].negative_count
        current_total = account_list[start_index + i].recent_tweet_count
        positive_list.append(current_positive * 100/current_total)
        neutral_list.append(current_neutral * 100/current_total)
        negative_list.append(current_negative * 100/current_total)
    print 'Made polarity lists'
    return {'positive_list': positive_list, 'neutral_list': neutral_list, 'negative_list': negative_list}


def get_tweets_by_year_month(account, year, month):
    def get_tweet_sentiment(text):
        url = "http://text-processing.com/api/sentiment/"
        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"text\"\r\n\r\n" + text + "\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        headers = {
            'content-type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW"
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        data = json.loads(response.text)
        return data["label"]

    tweet_list = []
    polarity = []
    favorite_count = 0
    retweet_count = 0
    positive_count = 0
    neutral_count = 0
    negative_count = 0
    for n in range(16):
        current_page = (api.user_timeline(account.handle, page = n))
        for status in current_page:
            if status.created_at.year == year and status.created_at.month == month:
                tweet_list.append(status)
                favorite_count += status.favorite_count
                retweet_count += status.retweet_count
                current_polarity = get_tweet_sentiment(status.text)
                polarity.append(current_polarity)
                if current_polarity == 'pos':
                    positive_count += 1
                else:
                    if current_polarity == 'neg':
                        negative_count += 1
                    else:
                        neutral_count += 1
    account.initialize_tweet_data(tweet_list, favorite_count, retweet_count, polarity, positive_count, neutral_count, negative_count)
    print 'Got tweet data for: ' + account.handle


def tweets_to_csv(path, account):
    file = open(path, 'wb')
    file_out = csv.writer(file, delimiter=',')
    file_out.writerow(['handle', 'tweet_id', 'created_at', 'retweet_count', 'favorite_count', 'text', 'polarity'])

    for i in range(len(account.tweet_list)):
        current_line = []
        current_line.append(account.handle)
        current_line.append(account.tweet_list[i].id)
        current_line.append(str(account.tweet_list[i].created_at))
        current_line.append(account.tweet_list[i].retweet_count)
        current_line.append(account.tweet_list[i].favorite_count)
        current_line.append(account.tweet_list[i].text)
        current_line.append(account.polarity[i])
        file_out.writerow(current_line)
    file.close()
    print 'Written tweet to csv for: ' + account.handle + "\n"


def plot_double_bar_graph(list1, list2, tick_label_list, file_name, plot_title):
    N = len(list1)
    tuple1 = tuple(list1)
    tuple2 = tuple(list2)
    tick_labels = tuple(tick_label_list)
    ind = np.arange(N)
    width = 0.25
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, tuple1, width, color='#66ffcc')
    rects2 = ax.bar(ind + width, tuple2, width, color='#4da6ff')
    ax.legend(('Favorited/Follower count %', 'Retweet/Follower count %'), bbox_to_anchor = (0.0, 1.02, 1.0, .102), loc = 3,
    ncol = 2, mode = "expand", borderaxespad = 0.)

    ax.set_ylabel('Percent')
    ax.set_title(plot_title, y = -0.1, color='blue', fontweight='bold')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(tick_labels)

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%.2f' % (height),
                    ha='center', va='bottom')
    autolabel(rects1)
    autolabel(rects2)
    plt.grid()
    fig.savefig(file_name)
    plt.close(fig)
    print 'Saved follower metric graph'


def plot_double_bar_line_graph(list1, list2, line_list, tick_label_list, file_name, plot_title):
    N = len(list1)
    tuple1 = tuple(list1)
    tuple2 = tuple(list2)
    tuple3 = tuple(line_list)
    tick_labels = tuple(tick_label_list)
    ind = np.arange(N)
    width = 0.25
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, tuple1, width, color='#66ffcc')
    rects2 = ax.bar(ind + width, tuple2, width, color='#4da6ff')
    ax.legend(('Favorited/Total tweets', 'Retweet/Total tweets'), bbox_to_anchor = (-0.03, 1.02, 0.83, .102), loc = 3,
    ncol = 2, mode = "expand", borderaxespad = 0.)

    ax.set_ylabel('Ratio')
    ax.set_title(plot_title, y = -0.1, color='blue', fontweight='bold')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(tick_labels)
    ax2 = ax.twinx()
    ax2.plot(ax.get_xticks(), tuple3, linestyle='-', marker='o', linewidth=2.0, color='red')
    ax2.legend(('Total tweets',), bbox_to_anchor=(0.8, 1.02, 0.95, .102), loc=3,
              ncol=2, mode="None", borderaxespad=0.)

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%.2f' % (height),
                    ha='center', va='bottom')
    autolabel(rects1)
    autolabel(rects2)
    plt.grid()
    fig.savefig(file_name)
    plt.close(fig)
    print 'Saved campaign effectiveness graph'


def plot_triple_bar_graph(list1, list2, list3, tick_label_list, file_name, plot_title):
    N = len(list1)
    tuple1 = tuple(list1)
    tuple2 = tuple(list2)
    tuple3 = tuple(list3)
    tick_labels = tuple(tick_label_list)
    ind = np.arange(N)
    width = 0.25
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, tuple1, width, color='#99ffbb')
    rects2 = ax.bar(ind + width, tuple2, width, color='#ffff80')
    rects3 = ax.bar(ind + width + width, tuple3, width, color='#ff8080')
    plt.legend(('Positive', 'Neutral', 'Negative'), bbox_to_anchor=(0.0, 1.02, 1.0, .102), loc=3,
               ncol=3, mode="expand", borderaxespad=0.)

    ax.set_ylabel('Percent of tweets')
    plt.title(plot_title, y=-0.1, color='blue', fontweight='bold')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(tick_labels)

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%.2f' % (height),
                    ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    fig.savefig(file_name)
    plt.close(fig)
    print 'Saved polarity graph'
