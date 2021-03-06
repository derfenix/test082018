# Generated by Django 2.1 on 2018-08-15 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('subscriptions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='object_id',
            field=models.IntegerField(db_index=True),
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together={('user_id', 'content_type', 'object_id')},
        ),
    ]
