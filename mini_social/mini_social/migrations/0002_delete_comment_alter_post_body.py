# Generated by Django 4.2.2 on 2023-07-02 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_social', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.CharField(default='', max_length=200),
        ),
    ]