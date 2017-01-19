# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields
from django.conf import settings
import paperclip.models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('attachment_file', models.FileField(upload_to=paperclip.models.attachment_upload, max_length=512, verbose_name='File', blank=True)),
                ('attachment_video', embed_video.fields.EmbedVideoField(verbose_name='URL', blank=True)),
                ('author', models.CharField(db_column=b'auteur', default=b'', max_length=128, blank=True, help_text='Original creator', verbose_name='Author')),
                ('title', models.CharField(db_column=b'titre', default=b'', max_length=128, blank=True, help_text='Renames the file', verbose_name='Filename')),
                ('legend', models.CharField(db_column=b'legende', default=b'', max_length=128, blank=True, help_text='Details displayed', verbose_name='Legend')),
                ('starred', models.BooleanField(default=False, help_text='Mark as starred', verbose_name='Starred', db_column=b'marque')),
                ('date_insert', models.DateTimeField(auto_now_add=True, verbose_name='Insertion date')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('creator', models.ForeignKey(related_name='created_attachments', verbose_name='Creator', to=settings.AUTH_USER_MODEL, help_text='User that uploaded')),
            ],
            options={
                'ordering': ['-date_insert'],
                'abstract': False,
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachments',
                'permissions': (('read_attachment', 'Can read attachments'), ('delete_attachment_others', "Can delete others' attachments")),
            },
        ),
        migrations.CreateModel(
            name='FileType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=128, verbose_name='File type')),
            ],
            options={
                'ordering': ['type'],
                'abstract': False,
                'verbose_name': 'File type',
                'verbose_name_plural': 'File types',
            },
        ),
        migrations.AddField(
            model_name='attachment',
            name='filetype',
            field=models.ForeignKey(verbose_name='File type', to='paperclip.FileType'),
        ),
    ]