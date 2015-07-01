# encoding: utf-8

from rdr.modules.users.actions.views import AddedFeedActionView


def make_views(actions):
    views = []
    for act in actions:
        views.append(resolve_action(act))
    return views


def resolve_action(action):
    if action.type == AddedFeedActionView.ACTION_TYPE:
        return AddedFeedActionView(action)