# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Video, Tag, VideoComment

models = (Video, Tag, VideoComment)
for model in models:
    admin.site.register(model)
