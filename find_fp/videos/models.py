# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from find_fp.users.models import User


@python_2_unicode_compatible
class Video(models.Model):
    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
    )
    URL = 'U'
    FILE = 'F'
    TYPE = (
        (URL, 'Url'),
        (FILE, 'File'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    video_type = models.CharField(max_length=1, choices=TYPE, default=FILE)
    video_file = models.FileField(null=True, blank=True, upload_to='videos/%Y/%m')
    youtube_url = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=5000)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    create_user = models.ForeignKey(User)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)
    update_user = models.ForeignKey(User, null=True, blank=True,
                                    related_name="+")

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")
        ordering = ("-create_date",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Video, self).save(*args, **kwargs)
        else:
            self.update_date = datetime.now()
        if not self.slug:
            slug_str = "%s %s" % (self.pk, self.title.lower())
            self.slug = slugify(slug_str)
        if self.video_type == 'F':
            pass
        elif "watch?v=" in self.youtube_url:
            self.youtube_url = self.youtube_url.split('=')[1]
        elif "youtu.be" in self.youtube_url:
            self.youtube_url = self.youtube_url.split('be/')[1]
        else:
            pass
        super(Video, self).save(*args, **kwargs)

    # def get_content_as_markdown(self):
    #     return markdown.markdown(self.content, safe_mode='escape')

    def get_next(self):
        next = Video.objects.filter(status=Video.PUBLISHED, pk__gt=self.pk).order_by('pk')
        if next:
            return next.first()
        return self

    def get_prev(self):
        prev = Video.objects.filter(status=Video.PUBLISHED, pk__lt=self.pk).order_by('-pk')
        if prev:
            return prev.first()
        return self

    @staticmethod
    def get_published():
        videos = Video.objects.filter(status=Video.PUBLISHED)
        return videos

    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(' ')
        for tag in tag_list:
            if tag:
                t, created = Tag.objects.get_or_create(tag=tag.lower(),
                                                       video=self)

    def get_tags(self):
        return Tag.objects.filter(video=self)

    def get_summary(self):
        if len(self.content) > 255:
            return u'{0}...'.format(self.content[:255])
        else:
            return self.content

    # def get_summary_as_markdown(self):
    #     return markdown.markdown(self.get_summary(), safe_mode='escape')

    def get_comments(self):
        return VideoComment.objects.filter(video=self).order_by('date')


@python_2_unicode_compatible
class Tag(models.Model):
    tag = models.CharField(max_length=50)
    video = models.ForeignKey(Video)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        unique_together = (('tag', 'video'),)
        index_together = [['tag', 'video'], ]

    def __str__(self):
        return self.tag

    @staticmethod
    def get_popular_tags():
        tags = Tag.objects.all()
        count = {}
        for tag in tags:
            if tag.video.status == Video.PUBLISHED:
                if tag.tag in count:
                    count[tag.tag] = count[tag.tag] + 1
                else:
                    count[tag.tag] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]


@python_2_unicode_compatible
class VideoComment(models.Model):
    video = models.ForeignKey(Video)
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    parent = models.ForeignKey('VideoComment', null=True, blank=True)

    class Meta:
        verbose_name = _("Video Comment")
        verbose_name_plural = _("Video Comments")
        ordering = ("date",)

    def __str__(self):
        return u'{0} - {1}'.format(self.user.username, self.video.title)
