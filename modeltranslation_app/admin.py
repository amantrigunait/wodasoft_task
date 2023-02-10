from django import forms
from django.contrib import admin
from django.conf import settings

from .models import Article, Blog, default_language_dict

"""
The below class JSONFieldWidgetModifier and JSONFieldModifier are used to create a custom widget for the JSONField.
These can be reused with any field with type JSONField to create a custom widget instead of default textfield.
"""

class JSONFieldWidgetModifier(forms.Widget):
    def __init__(self, attrs=None, json_field=None):
        super().__init__(attrs)
        self.json_field = json_field

    def render(self, name, value, attrs=None, renderer=None):
        output = '<div style="display: flex; flex-direction: column;">'
        for key in self.json_field:
            output += f'<div style="margin-bottom: 10px;"><label>{key}:</label><input type="text" name="{name}_{key}" value="{self.json_field[key]}" /></div>'
        output += '</div>'
        return output
    
    def value_from_datadict(self, data, files, name):
        return {key.replace(name + '_', ''): value for key, value in data.items() if key.startswith(name)}


class JSONFieldModifier(forms.Field):
    def __init__(self, *args, **kwargs):
        default_json_field = kwargs.pop('json_field', {})
        super().__init__(*args, **kwargs)
        self.widget = JSONFieldWidgetModifier(json_field=default_json_field)


class ArticleForm(forms.ModelForm):
    title = JSONFieldModifier(json_field=default_language_dict())
    
    class Meta:
        model = Article
        fields = ['title']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            # below line is used to create updated_json_field from instance. This is to handle scenario wherein 
            # LANGUAGES in settings.py is changed (new language is added or removed).
            default_json_field=default_language_dict()
            updated_json_field = {key: instance.title.get(key, '') for key in default_json_field}
            self.fields['title'].widget = JSONFieldWidgetModifier(json_field=updated_json_field)
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title:
            default_language = settings.DEFAULT_LANGUAGE
            default_value = title.get(default_language)
            if not default_value:
                raise forms.ValidationError("The default language field cannot be empty")


class BlogForm(forms.ModelForm):
    blog_title = JSONFieldModifier(json_field=default_language_dict())

    class Meta:
        model = Blog
        fields = ['blog_title']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            # below line is used to create updated_json_field from instance. This is to handle scenario wherein 
            # LANGUAGES in settings.py is changed (new language is added or removed).
            default_json_field=default_language_dict()
            updated_json_field = {key: instance.blog_title.get(key, '') for key in default_json_field}
            self.fields['blog_title'].widget = JSONFieldWidgetModifier(json_field=updated_json_field)
    
    def clean(self):
        cleaned_data = super().clean()
        blog_title = cleaned_data.get("blog_title")
        if blog_title:
            default_language = settings.DEFAULT_LANGUAGE
            default_value = blog_title.get(default_language)
            if not default_value:
                raise forms.ValidationError("The default language field cannot be empty")


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm

class BlogAdmin(admin.ModelAdmin):
    form = BlogForm

admin.site.register(Article, ArticleAdmin)
admin.site.register(Blog, BlogAdmin)