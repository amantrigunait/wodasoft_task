from django import forms
from django.contrib import admin
from django.conf import settings

from .models import Article, Blog, default_language_dict

"""
The below class JSONFieldWidgetModifier and JSONFieldModifier are used to create a custom widget for the JSONField.
These can be reused with any field with type JSONField to create a custom widget instead of default textfield.
"""

class JSONFieldModifierWidget(forms.Widget):
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
        self.widget = JSONFieldModifierWidget(json_field=default_json_field)


class JSONFieldMixin:
    """
    THis class extracts the initial value for the JSONField from the instance and passes it to the JSONFieldModifierWidget.
    The clean method is used to validate that the default language field is not empty. 
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        for field_name, field in self.fields.items():
            if isinstance(field, JSONFieldModifier):
                if instance:
                    # below line is used to create updated_json_field from instance. 
                    # This is to handle scenario wherein LANGUAGES in settings.py is changed (new language is added or removed) i.e. updated_json_field only contains keys for the languages in settings.LANGUAGES
                    # TODO : Make it more dynamic to auto detect the default used in models.py instead of hardcoding default_language_dict() below
                    default_json_field = default_language_dict()
                    updated_json_field = {key: getattr(instance, field_name).get(key, '') for key in default_json_field}
                    field.widget = JSONFieldModifierWidget(json_field=updated_json_field)

    def clean(self):
        cleaned_data = super().clean()
        for field_name, field in self.fields.items():
            if isinstance(field, JSONFieldModifier):
                field_data = cleaned_data.get(field_name)
                if field_data:
                    default_language = settings.DEFAULT_LANGUAGE
                    default_value = field_data.get(default_language)
                    if not default_value:
                        raise forms.ValidationError(f"The default_language - {default_language} field for {field_name} cannot be empty")
        return cleaned_data

class ArticleForm(JSONFieldMixin, forms.ModelForm):
    title = JSONFieldModifier(json_field=default_language_dict())
    
    class Meta:
        model = Article
        fields = ['title']

class BlogForm(JSONFieldMixin, forms.ModelForm):
    blog_title = JSONFieldModifier(json_field=default_language_dict())
    description = JSONFieldModifier(json_field=default_language_dict())

    class Meta:
        model = Blog
        fields = ['blog_title', 'description', 'author']

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm

class BlogAdmin(admin.ModelAdmin):
    form = BlogForm

admin.site.register(Article, ArticleAdmin)
admin.site.register(Blog, BlogAdmin)