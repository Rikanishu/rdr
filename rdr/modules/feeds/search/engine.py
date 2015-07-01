# encoding: utf-8

from . import (SEARCH_IN_TEXT,
               SEARCH_IN_ANNOUNCE,
               SEARCH_IN_TITLE)

from . import (FILTER_ALL,
               FILTER_READ_ONLY,
               FILTER_UNREAD,
               FILTER_FAV)


def _prepare_filters(ids, user, filter_criteria):
    if not ids:
        return ids
    ids = [int(i) for i in ids]
    if filter_criteria == FILTER_READ_ONLY or filter_criteria == FILTER_UNREAD:
        from rdr.modules.feeds.models import ArticleStatus
        criteria = ArticleStatus.STATUS_READ
        if not user:
            raise Exception("Can't filter articles without user model")
        models = ArticleStatus.query.filter((ArticleStatus.status == criteria) &
                                            (ArticleStatus.user_id == user.id) &
                                            (ArticleStatus.article_id.in_(ids)))
        read = []
        for m in models:
            read.append(int(m.article_id))
        if filter_criteria == FILTER_READ_ONLY:
            return read
        return list(set(ids) - set(read))
    if filter_criteria == FILTER_FAV:
        if not user:
            raise Exception("Can't filter articles without user model")
        from rdr.modules.feeds.models import ArticleFavorite
        models = ArticleFavorite.query.filter((ArticleFavorite.user_id == user.id) &
                                              (ArticleFavorite.article_id.in_(ids)))
        res = []
        for m in models:
            res.append(int(m.article_id))
        return res

    return ids


class BaseSearchEngine(object):

    def create_index(self, article):
        raise NotImplementedError

    def create_full_text_index(self, article, full_text):
        raise NotImplementedError

    def search(self, subject, user, where, feed_ids=None, filter_criteria=FILTER_ALL):
        raise NotImplementedError


class ElasticSearchEngine(BaseSearchEngine):

    index = 'articles'
    doc_type = 'article'

    def create_index(self, article):
        from rdr.application.search import es
        es.index(self.index, self.doc_type, {
            'title': article.title,
            'announce': article.preview_text,
            'feed_id': article.feed_id
        }, article.id)

    def create_full_text_index(self, article, full_text):
        from rdr.application.search import es, TransportError
        try:
            es.get(self.index, self.doc_type, article.id)
        except TransportError as e:
            if e.status_code == 404:
                self.create_index(article)
        es.update(self.index, self.doc_type, article.id, {
            'doc': {
                'text': full_text.text
            }
        })

    def search(self, subject, user, where, feed_ids=None, filter_criteria=FILTER_ALL):
        from rdr.application.search import es
        fields = []
        if SEARCH_IN_TEXT in where:
            fields.append('text')
        if SEARCH_IN_TITLE in where:
            fields.append('title')
        if SEARCH_IN_ANNOUNCE in where:
            fields.append('announce')

        if feed_ids:
            body = {
                'query': {
                    'filtered': {
                        'query': {
                            'multi_match': {
                                'query': subject,
                                'fields': fields
                            }
                        },
                        'filter': {
                            'terms': {
                                'feed_id': feed_ids
                            }
                        }
                    }
                }
            }
        else:
            body = {
                'query': {
                    'multi_match': {
                        'query': subject,
                        'fields': fields
                    }
                }
            }

        stats = es.search(self.index, self.doc_type, body)
        ids = []
        if 'hits' in stats:
            if 'hits' in stats['hits']:
                for s in stats['hits']['hits']:
                    ids.append(s['_id'])
        ids = _prepare_filters(ids, user, filter_criteria)
        return ids


class DatabaseSearchEngine(BaseSearchEngine):

    def create_index(self, article):
        pass

    def create_full_text_index(self, article, full_text):
        pass

    def search(self, subject, where, user=None, feed_ids=None, filter_criteria=FILTER_ALL):
        from rdr.modules.feeds.models import Article, ArticleFullText
        from rdr.application.database import db
        q = db.session.query(Article.id)
        cond = []
        if SEARCH_IN_TITLE in where:
            cond.append(Article.title.ilike('%' + subject + '%'))
        if SEARCH_IN_ANNOUNCE in where:
            cond.append(Article.preview_text.ilike('%' + subject + '%'))
        if SEARCH_IN_TEXT in where:
            q = q.outerjoin(Article.full_text)
            cond.append(ArticleFullText.text.ilike('%' + subject + '%'))
        if not cond:
            raise Exception('Empty search condition')
        q = q.filter(reduce(lambda x, y: x | y, cond[1:], cond[0]))
        if feed_ids:
            q = q.filter(Article.feed_id.in_(feed_ids))
        article_ids = []
        for res in q:
            article_ids.append(res[0])
        article_ids = _prepare_filters(article_ids, user, filter_criteria)
        return article_ids

