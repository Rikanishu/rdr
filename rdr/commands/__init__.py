# encoding: utf-8

from flask.ext.script import Command, Option


class CollectStaticCommand(Command):

    help = description = "Static build generation"

    def run(self):
        print ("Make static build...")
        import rdr.modules.home.static
        builders = [
            rdr.modules.home.static.builder
        ]
        for builder in builders:
            builder.clear(exclude=['.gitignore'])
            builder.make_build()
        print("Done")


class MockupCommand(Command):

    help = description = "Fill test info"

    def run(self):

        feeds = [
            'http://kanobu.ru',
            'http://vesti.ru',
            'http://lenta.ru',
            'http://ria.ru/',
            'http://www.segodnia.ru/',
            'http://habrahabr.ru',
            'http://geektimes.ru',
            'http://lifehacker.com/',
            'http://cnn.com',
            'http://www.nytimes.com/',
            'https://500px.com/popular',
            'http://www.theverge.com/',
            'http://www.vox.com/',
            'http://www.polygon.com/',
            'http://lifehacker.com/',
            'http://readwrite.com/',
            'http://techcrunch.com/',
            'http://appleinsider.ru/',
            'http://macradar.ru/',
            'http://www.typetoken.net/',
            'http://www.sovsport.ru/',
            'http://www.championat.com/',
            'http://tass.ru/',
            'http://www.gazeta.ru/',
            'http://www.interfax.ru/',
            'http://www.kp.ru/',
            'http://www.kommersant.ru/',
            'http://1prime.ru/',
            'http://www.forbes.ru/',
            'http://www.ng.ru/',
            'http://top.rbc.ru/',
            'http://www.sports.ru/',
            'http://news.sport-express.ru/',
            'http://news.sportbox.ru/',
            'http://www.ntv.ru/',
            'http://www.kommersant.ru/',
            'http://www.soccer.ru/',
            'http://informing.ru/',
            'http://russian.rt.com/',
            'http://www.dni.ru/',
            'http://www.vz.ru/',
            'http://echo.msk.ru/',
            'http://rusnovosti.ru/',
            'http://mir24.tv/',
            'http://www.rg.ru/',
            'https://xakep.ru'
        ]

        from rdr.modules.feeds.models import Feed, FeedAliasUrl
        from rdr.modules.feeds.packages.resolver import PackagesResolver

        overall_count = len(feeds)
        for (num, url) in enumerate(feeds):
            existed_feed = Feed.query.filter(Feed.url == url).first()
            if not existed_feed:
                alias = FeedAliasUrl.query.filter(FeedAliasUrl.url == url).first()
                if not alias:
                    print '[%d/%d] Fetching feed for %s' % (num+1, overall_count, url)
                    PackagesResolver(url, load_articles=True).run()
                    print 'Done'

        print("All feeds done")