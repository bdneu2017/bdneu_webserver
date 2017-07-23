# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='����')),
                ('content', models.TextField(verbose_name='����')),
                ('email', models.CharField(max_length=25, verbose_name='����')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='����ʱ��')),
            ],
        ),
    ]
