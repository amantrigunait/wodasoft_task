# Generated by Django 4.1.6 on 2023-02-13 01:42

from django.db import migrations, models
import modeltranslation_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('modeltranslation_app', '0005_alter_article_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.RemoveField(
            model_name='article',
            name='description',
        ),
        migrations.AddField(
            model_name='blog',
            name='author',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Author'),
        ),
        migrations.AddField(
            model_name='blog',
            name='description',
            field=models.JSONField(blank=True, default=modeltranslation_app.models.default_language_dict, null=True, verbose_name='Article Description'),
        ),
    ]
