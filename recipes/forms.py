from .models import RecipeToApprove
from django.forms import ModelForm


class AddNewRecipe(ModelForm):
    class Meta:
        model = RecipeToApprove
        fields = ['title', 'kcal', 'source_link', 'difficulty', 'time', 'image_url']
