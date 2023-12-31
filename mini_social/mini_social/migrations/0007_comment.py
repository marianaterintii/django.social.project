# Generated by Django 4.2.2 on 2023-08-12 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mini_social', '0006_post_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(default='', max_length=200)),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini_social.customuser')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mini_social.post')),
            ],
        ),
    ]
