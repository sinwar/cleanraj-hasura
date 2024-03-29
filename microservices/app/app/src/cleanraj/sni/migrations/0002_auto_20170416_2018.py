# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-04-16 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sni', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addthing',
            name='details',
            field=models.TextField(default=' '),
        ),
        migrations.AlterField(
            model_name='addthing',
            name='itemimage',
            field=models.ImageField(default=' ', upload_to='/home/sinwar/djcode/sni/sni/site_media/media/things/'),
        ),
        migrations.AlterField(
            model_name='addthing',
            name='itemname',
            field=models.CharField(default=' ', max_length=30),
        ),
        migrations.AlterField(
            model_name='addthing',
            name='rate',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='newnotice',
            name='message',
            field=models.TextField(default=' '),
        ),
        migrations.AlterField(
            model_name='newnotice',
            name='receiver',
            field=models.CharField(default=' ', max_length=30),
        ),
        migrations.AlterField(
            model_name='newnotice',
            name='type',
            field=models.CharField(default=' ', max_length=30),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.TextField(default=' '),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='facebook',
            field=models.TextField(default=' '),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='first_name',
            field=models.TextField(default=' '),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default=' ', upload_to='/home/sinwar/djcode/sni/sni/site_media/media'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_name',
            field=models.TextField(default=' '),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='mobile',
            field=models.TextField(default=' '),
        ),
    ]
