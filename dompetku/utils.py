#!/usr/bin/env python
#
# Copyright @2014 blackshirtmuslim@yahoo.com
# Licensed: see Python license

"""Utility module"""

import json
import uuid
import hashlib

from decimal import Decimal
from datetime import date, datetime
from tornado import concurrent, ioloop
from concurrent.futures import ThreadPoolExecutor


def generate_hash(password, random_key=None):
    """Membuat password hash dengan random key 'random_key' menggunakan sha512 dari hashlib"""
    if not random_key:
        random_key = uuid.uuid4().hex
    hashed_pass = hashlib.sha512(str(password).encode() + random_key.encode()).hexdigest()
    return hashed_pass, random_key


def verify_password(password, hashed_password, key):
    """Verify password"""
    computed_hash, key = generate_hash(password, key)
    return computed_hash == hashed_password


# Some data types we want to check for.
def jsonify(data):
    # Get all that nasty Python cleaned up.
    data = json_clean(data)

    # Now we should be safe to dump to a string.
    try:
        data = json.dumps(data)
    except TypeError:
        # Go home, data. You're drunk.
        data = 'Wut'

    return data


def json_clean(data):
    # First things first: we need to do some simple cleanup of built-in
    # Python types.

    # Sets. JSON doesn't know how to enforce uniqueness, but since we're
    # probably done adding items here anyway, we should be safe turning
    # it into a list.
    if isinstance(data, set):
        data = list(data)

    # Lists and tuples themselves translate into JSON arrays just fine, but
    # the data they contain may not, so we have to recurse through it.
    if isinstance(data, list) or isinstance(data, tuple):
        # Make sure the data is mutable before we try making changes.
        data = list(data)
        for i in range(len(data)):
            data[i] = json_clean(data[i])
        return data

    # Same thing with dictionary values.
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = json_clean(v)
        return data

    # OK, now that we're beyond the sequences and dictionaries, we can get
    # into formatting special cases. We'll pair data types with cleaning
    # functions here.
    type_rules = {
        Decimal: clean_decimal,
        date: clean_date,
        datetime: clean_date,
    }

    # And run the data through the appropriate cleaner.
    for type_name, type_cleaner in type_rules.items():
        if isinstance(data, type_name):
            return type_cleaner(data)

    # At this point we don't know what sort of data this is. Return it
    # as-is and hope for the best.
    return data


# Turn a good precise decimal into a more JavaScript-friendly float.
def clean_decimal(data):
    return float(data)


# Use an isoformat string for dates and times.
def clean_date(data):
    return data.isoformat()


# # from http://nchls.com/post/serializing-complex-python-data-json/
class DBContainer(object):
    def __init__(self, model):
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.io_loop = ioloop.IOLoop.current()
        self.model = model

    @concurrent.run_on_executor
    def get(self, *args, **kwargs):
        return self.model.get(*args, **kwargs)

    @concurrent.run_on_executor
    def select(self, *args, **kwargs):
        return self.model.select(*args, **kwargs)

    @concurrent.run_on_executor
    def to_dicts(self, *args, **kwargs):
        return self.model.select(*args, **kwargs).dicts()

    def insert(self, **kwargs):
        return self.model.insert(**kwargs).execute()
