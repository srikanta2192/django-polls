# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-06-26 05:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quora', '0010_auto_20190626_0541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='like',
            name='liked_by',
        ),
        migrations.RemoveField(
            model_name='like',
            name='post',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]