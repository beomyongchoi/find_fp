# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class WhereAreYou(models.Model):
    location = models.CharField(max_length=30)

    def __str__(self):
        return self.location
