# Generated by Django 4.1.6 on 2023-02-13 01:31

from django.db import migrations, models
import modeltranslation_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('modeltranslation_app', '0004_alter_article_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.JSONField(blank=True, default=modeltranslation_app.models.default_language_dict, null=True, verbose_name='Article Description'),
        ),
    ]
