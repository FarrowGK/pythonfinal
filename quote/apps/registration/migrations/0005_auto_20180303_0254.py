# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-03-03 02:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0004_product_joiners'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quotedby', models.CharField(max_length=255)),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='creator',
        ),
        migrations.RemoveField(
            model_name='product',
            name='joiners',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='hired',
            new_name='dob',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.AddField(
            model_name='quote',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adding', to='registration.User'),
        ),
        migrations.AddField(
            model_name='quote',
            name='quoters',
            field=models.ManyToManyField(related_name='quoter', to='registration.User'),
        ),
    ]
