# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
from kuma.wiki.constants import SPAM_EXEMPTED_FLAG


def create_trusted_writers(apps, schema_editor):
    # first create a new trusted writers user group
    Group = apps.get_model('auth', 'Group')
    group, created = Group.objects.get_or_create(name='Trusted writers')

    # then add that user group to the list of people exempted from spam checks
    Flag = apps.get_model('waffle', 'Flag')
    defaults = {
        'note': ('Used when deciding which user is exempted from spam checks. '
                 'Select "everyone" to disable spam checks entirely')
    }
    flag, created = Flag.objects.get_or_create(name=SPAM_EXEMPTED_FLAG,
                                               defaults=defaults)
    flag.groups.add(group)


def delete_trusted_writers(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name='Trusted writers').delete()

    Flag = apps.get_model('waffle', 'Flag')
    Flag.objects.filter(name=SPAM_EXEMPTED_FLAG).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('waffle', '0001_initial'),
        ('wiki', '0010_auto_20150915_1211'),
    ]

    operations = [
        migrations.RunPython(create_trusted_writers, delete_trusted_writers),
    ]
