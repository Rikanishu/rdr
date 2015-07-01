# encoding: utf-8


def nl2br(string):
    return string.replace('\n','<br />\n')


def nl2p(string):
    parts = string.split('\n')
    res = ''
    for p in parts:
        res += '<p>' + p + '</p>'
    return res
