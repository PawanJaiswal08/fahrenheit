# Generated by Django 3.1.7 on 2021-05-02 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20210424_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
