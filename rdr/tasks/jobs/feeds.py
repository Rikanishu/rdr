# encoding: utf-8

from rdr.tasks import celery

ARTICLE_FETCH_TIMEOUT = 60

@celery.task()
def recalculate_categories():
    from rdr.modules.subscribes.models import Subscribe
    from rdr.modules.feeds.models import Feed
    from rdr.tasks.schedule.feeds import categories
    from rdr.application.database import db
    from math import ceil

    feed_ids = db.session.query(Subscribe.feed_id, db.func.count(Subscribe.id).label('total')) \
        .filter(Subscribe.type == Subscribe.TYPE_FEED) \
        .group_by(Subscribe.feed_id) \
        .order_by(db.desc('total'))
    feed_ids = [x[0] for x in feed_ids]
    count = len(feed_ids)
    offset = 0
    results = []
    for num in xrange(0, len(categories)):
        category = categories[num][0]
        percent = categories[num][1]
        if offset < count:
            if num != len(categories) - 1:
                percent_count = int(ceil(float(percent) / 100 * count))
                results.append((category, feed_ids[offset:offset+percent_count]))
                offset += percent_count
            else:
                results.append((category, feed_ids[offset:]))
    for res in results:
        if res[1]:
            q = db.update(Feed).values({'category': res[0]}) \
                .where(Feed.id.in_(res[1]))
            db.session.execute(q)
    db.session.commit()


@celery.task()
def fetch_category_articles(category):
    from rdr.modules.feeds.models import Feed
    from celery import group
    feeds = Feed.query.filter(Feed.category == category)
    subtasks = []
    for feed in feeds:
        subtasks.append(fetch_feed_articles.subtask((feed.id,), retry=False, expires=ARTICLE_FETCH_TIMEOUT + 20))
    subtasks_group = group(subtasks)
    subtasks_group()
    return len(subtasks)


@celery.task()
def fetch_feed_articles(feed_id):
    from rdr.modules.feeds.articles.sync import ArticlesSynchronizer
    from rdr.modules.feeds.models import Feed
    from rdr.application.cache import cache

    sync_count = 0
    cache_key = 'tasks.fetch_feed_articles.lock.' + str(feed_id)
    if not cache.get(cache_key):
        cache.set(cache_key, True, timeout=ARTICLE_FETCH_TIMEOUT)
        feed = Feed.query.filter(Feed.id == feed_id).first()
        if feed:
            synchronizer = ArticlesSynchronizer(feed)
            articles = synchronizer.sync()
            sync_count = len(articles)
        cache.delete(cache_key)
    return feed_id, sync_count


@celery.task()
def resolve_package_channel(url):
    from rdr.modules.feeds.packages.resolver import PackagesResolver
    resolver = PackagesResolver(url, is_channel_url=True)
    resolver.run()
    feeds = resolver.result_feeds()
    return [feed.id for feed in feeds]
