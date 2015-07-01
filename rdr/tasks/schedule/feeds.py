# encoding: utf-8

from datetime import timedelta

# feeds categories
# number, time in seconds, percents of global count
categories = [
    (1, 1, 300),
    (2, 2, 600),
    (3, 4, 900),
    (4, 7, 1800),
    (5, 10, 3600),
    (6, 14, 7200),
    (7, 22, 14400),
    (8, 40, 28800)
]

schedule = {}

for category in categories:
    category_num = category[0]
    seconds = category[2]
    key = 'feeds-fetch-articles-' + str(category_num)
    schedule[key] = {
        'task': 'rdr.tasks.jobs.feeds.fetch_category_articles',
        'schedule': timedelta(seconds=seconds),
        'args': (category_num,)
    }


schedule['feeds-recalculate-categories'] = {
    'task': 'rdr.tasks.jobs.feeds.recalculate_cagetories',
    'schedule': timedelta(hours=8)
}