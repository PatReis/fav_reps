from django.forms import ModelForm, TextInput, CharField
from .models import Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'
        exclude = ["owner", "rating_mean", "rating_count"]
        # widgets = {
        #     'name': TextInput(attrs={
        #         'class': "form-control",
        #         'style': 'max-width: 300px;',
        #         'placeholder': 'Name'
        #     }),
        # }
