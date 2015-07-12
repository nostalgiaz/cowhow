# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ch_coworking', '0007_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoworkingPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', editable=False, default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', editable=False, default=django.utils.timezone.now)),
                ('title', models.CharField(blank=True, verbose_name='Title', max_length=100)),
                ('caption', models.TextField(blank=True, verbose_name='Caption')),
                ('cover', models.BooleanField(verbose_name='Cover', default=False)),
                ('photo', models.ImageField(verbose_name='Photo', upload_to='coworkings')),
            ],
            options={
                'verbose_name': 'Coworking photo',
                'verbose_name_plural': 'Coworking photos',
                'ordering': ['-cover'],
            },
        ),
        migrations.AlterField(
            model_name='table',
            name='coworking',
            field=models.ForeignKey(to='ch_coworking.Coworking', related_name='tables'),
        ),
    ]
