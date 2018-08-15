# Generated by Django 2.1 on 2018-08-11 16:38

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=0, verbose_name='comment level')),
                ('user_id', models.IntegerField(db_index=True, verbose_name="comment's author id")),
                ('object_id', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('deleted', models.DateTimeField(blank=True, db_index=True, default=None, null=True, verbose_name='deleted')),
                ('content', models.TextField(verbose_name='content')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='children', to='main.Comment', verbose_name='parent comment')),
                ('root', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='all_children', to='main.Comment', verbose_name='root comment')),
            ],
        ),
        migrations.CreateModel(
            name='CommentsHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='timestamp')),
                ('user_id', models.IntegerField(verbose_name='user id')),
                ('action', models.CharField(choices=[('create', 'create'), ('update', 'update'), ('delete', 'delete')], max_length=12, verbose_name='action')),
                ('diff', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None, verbose_name="content's diff")),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.Comment', verbose_name='comment')),
            ],
        ),
    ]
