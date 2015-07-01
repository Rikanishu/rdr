# encoding: utf-8

from lxml import etree
from rdr.application.database import db
from rdr.modules.subscribes.models import Subscribe
from rdr.modules.users.session import user_session


class OPMLImporter(object):

    def __init__(self, text, user=None, parallel=True):
        self.text = text
        if user is None:
            if not user_session.is_auth:
                raise Exception('User is not authorised')
            user = user_session.identity
        self.user = user
        self.parallel = parallel
        self.awaits = []

    def run(self):
        tree = etree.XML(self.text)
        outlines = tree.xpath('/opml/body/outline')
        for outline_elem in outlines:
            if outline_elem.get('type') == 'rss':
                self._create_subscribe_for_elem(outline_elem)
            else:
                folder_title = outline_elem.get('title')
                folder_model = Subscribe.query.filter((Subscribe.user_id == self.user.id) &
                                                   (Subscribe.active == True) &
                                                   (Subscribe.type == Subscribe.TYPE_FOLDER) &
                                                   (Subscribe.name == folder_title)).first()
                if not folder_model:
                    folder_model = Subscribe(user_id=self.user.id, parent_id=0,
                                       name=folder_title, type=Subscribe.TYPE_FOLDER,
                                       order=10, active=True, feed_id=None)
                    db.session.add(folder_model)
                    db.session.flush()

                for rss_elem in outline_elem.getchildren():
                    if rss_elem.get('type') == 'rss':
                        self._create_subscribe_for_elem(rss_elem, folder=folder_model)

        for future in self.awaits:
            future.await()

        db.session.commit()

    def _create_subscribe_for_elem(self, rss_elem, folder=None):
        channel_url = rss_elem.get('xmlUrl')
        channel_title = rss_elem.get('title')
        if channel_url and channel_title:
            if not self.parallel:
                future = SubscribeFuture(self.user, channel_url, channel_title, folder=folder)
            else:
                future = SubscribeTaskFuture(self.user, channel_url, channel_title, folder=folder)

            future.run()
            self.awaits.append(future)


class SubscribeFuture(object):

    def __init__(self, user, url, title, folder=None):
        self.user = user
        self.url = url
        self.title = title
        self.folder = folder

    def run(self):
        from rdr.modules.feeds.packages.resolver import PackagesResolver
        resolver = PackagesResolver(self.url, is_channel_url=True)
        resolver.run()
        feeds = resolver.result_feeds()
        if feeds:
            selected = feeds[0]
            self._select_feed(selected.id)

    def await(self):
        pass

    def _select_feed(self, feed_id):
        subscribe_model = Subscribe.query.filter((Subscribe.user_id == self.user.id) &
                                                 (Subscribe.active == True) &
                                                 (Subscribe.type == Subscribe.TYPE_FEED) &
                                                 (Subscribe.feed_id == feed_id)).first()
        parent_id = self.folder.id if self.folder is not None else 0
        if subscribe_model:
            subscribe_model.parent_id = parent_id
        else:
            subscribe_model = Subscribe(user_id=self.user.id, parent_id=parent_id,
                                        name=self.title, type=Subscribe.TYPE_FEED,
                                        order=20, active=True, feed_id=feed_id)
            db.session.add(subscribe_model)
            db.session.flush()


class SubscribeTaskFuture(SubscribeFuture):

    def __init__(self, *args, **kwargs):
        super(SubscribeTaskFuture, self).__init__(*args, **kwargs)
        self.task = None

    def run(self):
        from rdr.tasks.jobs.feeds import resolve_package_channel
        self.task = resolve_package_channel.apply_async((self.url,), expires=120, retry=False)

    def await(self):
        ids = self.task.get()
        if ids:
            self._select_feed(ids[0])


class OPMLExporter(object):

    def __init__(self, user=None):
        if user is None:
            if not user_session.is_auth:
                raise Exception('User is not authorised')
            user = user_session.identity
        self.user = user

    def make_opml(self):
        opml = etree.Element('opml', version='1.0')
        head = etree.SubElement(opml, 'head')
        body = etree.SubElement(opml, 'body')
        title = etree.SubElement(head, 'title')
        title.text = '%s subscriptions in Reader' % self.user.username
        items, folders = self._fetch_subscriptions_hierarchy()
        for folder_sub, feeds in folders:
            folder_sub_elem = etree.SubElement(body, 'outline', text=folder_sub.name, title=folder_sub.name)
            for sub in feeds:
                self._make_rss_elem(folder_sub_elem, sub)
        for sub in items:
            self._make_rss_elem(body, sub)
        doc = etree.ElementTree(opml)
        return etree.tostring(doc, xml_declaration=True, encoding="UTF-8", pretty_print=True)


    def _make_rss_elem(self, parent, sub):
        if sub.feed:
            etree.SubElement(parent, 'outline', type='rss',
                                    text=sub.name, title=sub.name,
                                    htmlUrl=sub.feed.url, xmlUrl=sub.feed.channel_url)

    def _fetch_subscriptions_hierarchy(self):
        folders = {}
        items = []
        root_items = []
        subscribes = Subscribe.query.filter((Subscribe.user_id == self.user.id) &
                                                 (Subscribe.active == True))
        for sub in subscribes:
            if sub.type == Subscribe.TYPE_FOLDER:
                folders[sub.id] = (sub, [])
            elif sub.type == Subscribe.TYPE_FEED:
                items.append(sub)
        for sub in items:
            if sub.parent_id == 0:
                root_items.append(sub)
            if sub.parent_id in folders:
                folders[sub.parent_id][1].append(sub)
        return root_items, folders.values()
