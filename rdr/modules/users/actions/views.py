# encoding: utf-8


class AbstractActionView(object):

    ACTION_TYPE = 'Unknown'

    def __init__(self, action):
        self.action = action

    def render(self):
        raise NotImplementedError


class AddedFeedActionView(AbstractActionView):

    ACTION_TYPE = 'AddedFeed'

    def render(self):
        return "%s added feed" % self.action.user.username