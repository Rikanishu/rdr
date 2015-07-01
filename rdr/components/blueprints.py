# encoding: utf-8

from flask import Blueprint, redirect


class RichBlueprint(Blueprint):

    def redirect(self, location, code=302):
        prefix = self.url_prefix or ''
        return redirect(prefix.rstrip('/') + '/' + location.lstrip('/'), code)