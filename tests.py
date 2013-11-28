#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gestor Tests
"""

import doctest
import unittest

# Import modules to test
from core import helpers, urls

suite = unittest.TestSuite()

# Add doctests to unittest
suite.addTest(doctest.DocTestSuite(helpers))
suite.addTest(doctest.DocTestSuite(urls))

# Run unittest
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
