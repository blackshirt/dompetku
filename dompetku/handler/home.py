#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
# Licensed : see Python License

"""Module home inde."""

from dompetku.handler import base


class HomeHandler(base.BaseHandler):
    def get(self):
        self.render('home.html')
