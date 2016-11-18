from __future__ import unicode_literals

from django.apps import AppConfig


class VideosConfig(AppConfig):
    name = 'find_fp.videos'
    verbose_name = "videos"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
