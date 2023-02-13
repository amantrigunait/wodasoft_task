# Generated by Django 4.1.6 on 2023-02-13 01:17

from django.db import migrations, models
import modeltranslation_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('modeltranslation_app', '0003_article_author_article_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.JSONField(default=modeltranslation_app.models.default_language_dict, verbose_name='Article Description'),
        ),
    ]