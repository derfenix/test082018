# Generated by Django 2.1 on 2018-08-15 07:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='object_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='root',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='root_children', to='main.Comment', verbose_name='root comment'),
        ),
        migrations.AlterField(
            model_name='commentshistory',
            name='action',
            field=models.CharField(choices=[('create', 'create'), ('update', 'update'), ('delete', 'delete'), ('restore', 'restore')], max_length=12, verbose_name='action'),
        ),
    ]
