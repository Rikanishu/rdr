# encoding: utf-8

from rdr.modules.feeds.models import Feed
from rdr.modules.subscribes.models import Subscribe
from rdr.application import app
from rdr.application.database import db
from rdr.application.cache import cache
from rdr.modules.users.session import user_session


class PopularPackagesGenerator(object):

    def __init__(self, user=None, packages_count=10, random_order=True, use_cache=True, cache_timeout=1200):
        self.packages_count = packages_count
        self.random_order = random_order
        if user is None:
            if not user_session.is_auth:
                raise Exception('User is not authorised')
            user = user_session.identity
        self.user = user
        self.use_cache = use_cache
        self.timeout = cache_timeout

    def fetch_packages(self):
        package_ids = None
        key = 'popular_packages.' + str(self.user.id)
        if self.use_cache:
            try:
                package_ids = cache.get(key)
            except Exception as e:
                app.logger.exception(e)
                app.logger.info("An exception catched, disable cache")
                self.use_cache = False
        if package_ids is None:
            packages = db.session.query(Subscribe.feed_id, db.func.count(Subscribe.id).label('total')) \
                .filter(Subscribe.type == Subscribe.TYPE_FEED) \
                .filter(Subscribe.feed_id.notin_(db.session.query(Subscribe.feed_id).filter(
                    (Subscribe.user_id == self.user.id) & (Subscribe.feed_id.isnot(None))
                ).group_by(Subscribe.feed_id))) \
                .group_by(Subscribe.feed_id) \
                .order_by(db.desc('total')) \
                .limit(500)
            package_ids = []
            for (feed_id, _count) in packages:
                package_ids.append(feed_id)
            if self.random_order:
                import random
                random.shuffle(package_ids)
            package_ids = package_ids[:self.packages_count]
            if self.use_cache:
                cache.set(key, package_ids, timeout=self.timeout)

        feeds = Feed.query.filter(Feed.id.in_(package_ids))
        return feeds