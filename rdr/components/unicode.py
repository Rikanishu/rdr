# coding=utf-8

import pprint


class UnicodePrettyPrinter(pprint.PrettyPrinter):
    def format(self, object, context, maxlevels, level):
        ret = pprint.PrettyPrinter.format(self, object, context, maxlevels, level)
        if isinstance(object, unicode):
            ret = (object.encode('utf-8'), ret[1], ret[2])
        return ret


upp = UnicodePrettyPrinter()