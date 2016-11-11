from __future__ import unicode_literals

from django.apps import AppConfig


class WhatShouldIEatConfig(AppConfig):
    name = 'find_fp.whatshouldieat'
    verbose_name = "WhatSHouldIEat"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
