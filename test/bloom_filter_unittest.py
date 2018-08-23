# -*- coding: utf-8 –*-

"""
Created on 2018-05-30

@author: sm
"""

import unittest

from test.unit import sys_init

from models.bloom_filter import BloomFilter


class BloomFilterTest(unittest.TestCase):
    def setUp(self):
        self.bloom_filter = BloomFilter()

    def test_contains(self):
        device_mark = [
            '00000000-010c-053a-010c-053a00000000',
            '00000000-010c-053a-010c-053a00000001',
            '00000000-010c-053a-010c-053a00000002',
            '00000000-010c-053a-010c-053a00000003',
            '00000000-010c-053a-010c-053a00000004',
            'song',
            'ming',
            '1',
            '2',
        ]

        self.bloom_filter.redis.delete(self.bloom_filter.KEY)

        for i in device_mark:
            self.assertFalse(self.bloom_filter.is_contains(i))

        for i in device_mark:
            self.bloom_filter.insert(i)

        for i in device_mark:
            self.assertTrue(self.bloom_filter.is_contains(i))
