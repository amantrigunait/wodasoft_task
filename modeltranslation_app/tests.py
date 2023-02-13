from django.test import TestCase
from .models import Article
from .admin import ArticleAdmin, ArticleForm, JSONFieldModifier, JSONFieldModifierWidget
from django.conf import settings

class ArticleModelTestCase(TestCase):

    """
    Basic test case for the Article model
    """
    def setUp(self):
        self.title = {"en": "Test Title"}
        self.article = Article.objects.create(title=self.title)

    def test_str_representation(self):
        self.assertEqual(str(self.article), "Test Title")
        
    def test_title_field(self):
        self.assertEqual(self.article.title, self.title)


class ArticleFormTestCase(TestCase):
    def test_form_valid(self):
        """
        Test that the form is valid if the default language field is not empty
        """
        DEFAULT_LANGUAGE = settings.DEFAULT_LANGUAGE
        form_data = {f'title_{DEFAULT_LANGUAGE}': 'Test title in default language'}
        form = ArticleForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        """
        Test that the form is invalid if the default language field is empty
        """
        LANGUAGES = settings.LANGUAGES
        non_default_language = [lang[0] for lang in LANGUAGES if lang[0] != settings.DEFAULT_LANGUAGE][0]
        form_data = {f'title_{non_default_language}': 'Test title in non default language'}
        form = ArticleForm(data=form_data)
        self.assertFalse(form.is_valid())


class JSONFieldModifierWidgetTestCase(TestCase):
    def test_render(self):
        """
        Test that the widget renders multiple input fields for each language
        """
        widget = JSONFieldModifierWidget(json_field={'en': 'Test title in English', 'fr': 'Titre de test en français'})
        html = widget.render('title', None)
        self.assertInHTML('<input type="text" name="title_en" value="Test title in English">', html)
        self.assertInHTML('<input type="text" name="title_fr" value="Titre de test en français">', html)
    
    def test_value_from_datadict(self):
        widget = JSONFieldModifierWidget(json_field={'en': 'Test title in English'})
        data = {'title_en': 'Updated test title in English'}
        value = widget.value_from_datadict(data, None, 'title')
        self.assertEqual(value, {'en': 'Updated test title in English'})