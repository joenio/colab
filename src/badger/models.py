# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import ugettext_lazy as _
from PIL import Image
from linguo.models import MultilingualModel
from linguo.managers import MultilingualManager


class Badge(MultilingualModel):
    COMPARISON_CHOICES = (
        (u'gte', _(u'Greater than or equal')),
        (u'lte', _(u'less than or equal')),
        (u'equal', _(u'Equal')),
        (u'biggest', _(u'Biggest')),
    )
    TYPE_CHOICES = (
        (u'auto', _(u'Automatically')),
        (u'manual', _(u'Manual')),
    )
    USER_ATTR_CHOICES = (
        (u'messages', _(u'Messages')),
        (u'contributions', _(u'Contributions')),
        (u'wikis', _(u'Wikis')),
        (u'revisions', _(u'Revisions')),
        (u'tickets', _(u'Ticket')),
    )
    USER_ATTR_OPTS = {
        u'messages': u'message_count',
        u'revisions': u'changeset_count',
        u'tickets': u'ticket_count',
        u'wikis': u'wiki_count',
        u'contributions': u'contribution_count',
    }

    title = models.CharField(_(u'Title'), max_length=200, blank=True,
                             null=True)
    description = models.CharField(_(u'Description'), max_length=200,
                                   blank=True, null=True)
    image = models.ImageField(upload_to='badges')
    type = models.CharField(_(u'Type'), max_length=200, choices=TYPE_CHOICES)
    user_attr = models.CharField(
        _(u'User attribute'),max_length=100,
        choices=USER_ATTR_CHOICES,
        blank=True,
        null=True,
    )
    comparison = models.CharField(
        _(u'Comparison'),
        max_length=10,
        choices=COMPARISON_CHOICES,
        blank=True,
        null=True
    )
    value = models.PositiveSmallIntegerField(
        _(u'Value'),
        blank=True,
        null=True
    )
    awardees = models.ManyToManyField(
        get_user_model(),
        verbose_name=_(u'Awardees'),
        blank=True,
        null=True
    )

    objects = MultilingualManager()

    class Meta:
        verbose_name = _(u'Badge')
        verbose_name_plural = _(u'Badges')
        translate = ('title', 'description')

    def get_badge_url(self):
        return u'{}{}'.format(settings.MEDIA_URL, self.image)

    def save(self, *args, **kwargs):
        img = Image.open(self.image)
        (width, height) = img.size
        img = img.resize((50, 50), Image.ANTIALIAS)
        super(Badge, self).save(*args, **kwargs)
        img.save(self.image.path)

    def __unicode__(self):
        return u'{} ({}, {})'.format(
            self.title,
            self.get_user_attr_display(),
            self.get_type_display(),
        )
