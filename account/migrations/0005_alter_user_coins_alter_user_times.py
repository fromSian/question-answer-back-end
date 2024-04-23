# Generated by Django 4.1.13 on 2024-08-08 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='coins',
            field=models.PositiveIntegerField(default=0, verbose_name='金币数'),
        ),
        migrations.AlterField(
            model_name='user',
            name='times',
            field=models.PositiveIntegerField(default=2, verbose_name='可免费发布提问次数'),
        ),
    ]
