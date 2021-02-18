""" test.py

Tests for this fine application.
"""

from __future__ import print_function

__author__ = "Christopher Wolfe"
__copyright__ = "Copyright 2018, Christopher Wolfe"
__license__ = "MIT"
__maintainer__ = "Christopher Wolfe"
__email__ = "noone234@gmail.com"
__status__ = "Development"

import pytest
from app import create_app


class TestClass:
    @classmethod
    def setup_class(cls):
        # Set up test environment.
        cls.app = create_app()
        cls.client = cls.app.test_client

    def test_connect(self):
        # Verify that we can connect to the home page.
        print("Hello world!")
        rv = self.client().get("/")
        assert rv.status_code == 200
